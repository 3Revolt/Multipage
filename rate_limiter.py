# --- RATE LIMITER ZA KONTAKT FORMU ---
# Višeslojna zaštita od spama, bez vanjskih servisa:
#   1. Pauza između dvije poruke istog posjetioca (cooldown)
#   2. Dnevni limit po posjetiocu (IP adresa + sesija - oboje se broji)
#   3. Dnevni limit po email adresi pošiljaoca (ne pomaže promjena IP-a)
#   4. Blokada iste poruke poslane više puta
#   5. Blokada nakon previše pogrešnih captcha odgovora (brute force)
#   6. Globalni limit po satu i danu - štiti email nalog od blokade kod SMTP providera
#
# Podaci se čuvaju u memoriji i u JSON fajlu u temp folderu, pa preživljavaju i
# restart Streamlit skripte (ne i potpuno novi server/kontejner).

import hashlib
import ipaddress
import json
import os
import tempfile
import threading
import time

MINUTE = 60
HOUR = 3600
DAY = 86400

DEFAULT_RULES = {
    "cooldown": 60,                       # sekundi između dvije poruke istog posjetioca
    "per_client": (5, DAY),               # 5 poruka / 24h po posjetiocu
    "per_email": (3, DAY),                # 3 poruke / 24h sa iste email adrese
    "duplicate_window": DAY,              # ista poruka se ne može ponovo poslati 24h
    "captcha_failures": (5, 10 * MINUTE), # 5 pogrešnih captcha u 10 min...
    "captcha_lockout": 15 * MINUTE,       # ...zaključava formu na 15 min
    "global_hour": (20, HOUR),            # ukupno za sve posjetioce
    "global_day": (60, DAY),
}


def _hash(value):
    return hashlib.sha256(value.strip().lower().encode("utf-8")).hexdigest()[:32]


def is_public_ip(value):
    """True samo za javne IP adrese (lokalne/proxy adrese bi spojile sve posjetioce u jednog)."""
    try:
        return ipaddress.ip_address(value.strip()).is_global
    except (ValueError, AttributeError):
        return False


def client_keys(headers=None, ip_address=None, session_id=None):
    """
    Vraća listu ključeva koji identifikuju posjetioca.
    Javna IP adresa (ako postoji) + ID sesije - limit važi za oba, pa ga ne zaobilazi ni refresh ni promjena IP-a.
    """
    keys = []
    candidates = []
    if headers:
        forwarded = headers.get("X-Forwarded-For") or headers.get("x-forwarded-for") or ""
        candidates += [part.strip() for part in forwarded.split(",") if part.strip()]
        candidates.append(headers.get("X-Real-Ip") or headers.get("x-real-ip") or "")
    candidates.append(ip_address or "")
    public = next((c for c in candidates if is_public_ip(c)), None)
    if public:
        keys.append(f"ip:{public}")
    if session_id:
        keys.append(f"session:{session_id}")
    return keys


class RateLimiter:
    def __init__(self, rules=None, storage_path=None, clock=time.time):
        self.rules = {**DEFAULT_RULES, **(rules or {})}
        self.clock = clock
        self.lock = threading.Lock()
        self.storage_path = storage_path
        self.data = {"sent": {}, "emails": {}, "messages": {}, "captcha": {}, "locked": {}, "global": []}
        self._load()

    # --- Perzistencija ---
    def _load(self):
        if not self.storage_path:
            return
        try:
            with open(self.storage_path, "r", encoding="utf-8") as f:
                loaded = json.load(f)
            for key in self.data:
                if key in loaded:
                    self.data[key] = loaded[key]
        except (OSError, ValueError):
            pass

    def _save(self):
        if not self.storage_path:
            return
        try:
            tmp = f"{self.storage_path}.tmp"
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(self.data, f)
            os.replace(tmp, self.storage_path)
        except OSError:
            pass

    # --- Pomoćne ---
    def _prune(self, now):
        longest = max(DAY, self.rules["duplicate_window"])
        for bucket in ("sent", "emails", "messages", "captcha"):
            for key in list(self.data[bucket]):
                self.data[bucket][key] = [t for t in self.data[bucket][key] if now - t < longest]
                if not self.data[bucket][key]:
                    del self.data[bucket][key]
        for key in list(self.data["locked"]):
            if self.data["locked"][key] <= now:
                del self.data["locked"][key]
        self.data["global"] = [t for t in self.data["global"] if now - t < DAY]

    @staticmethod
    def _count(times, period, now):
        recent = [t for t in times if now - t < period]
        return len(recent), (min(recent) + period - now) if recent else 0

    # --- Javni API ---
    def check(self, keys, email=None, message=None):
        """
        Provjerava da li je slanje dozvoljeno.
        Vraća (dozvoljeno, razlog, sekundi_do_ponovnog_pokušaja).
        Razlozi: "locked", "cooldown", "client_limit", "email_limit", "duplicate", "global_limit"
        """
        with self.lock:
            now = self.clock()
            self._prune(now)

            for key in keys:
                until = self.data["locked"].get(key)
                if until and until > now:
                    return False, "locked", int(until - now) + 1

            limit, period = self.rules["per_client"]
            for key in keys:
                times = self.data["sent"].get(key, [])
                if times and now - max(times) < self.rules["cooldown"]:
                    return False, "cooldown", int(self.rules["cooldown"] - (now - max(times))) + 1
                count, retry = self._count(times, period, now)
                if count >= limit:
                    return False, "client_limit", int(retry) + 1

            if email:
                limit, period = self.rules["per_email"]
                count, retry = self._count(self.data["emails"].get(_hash(email), []), period, now)
                if count >= limit:
                    return False, "email_limit", int(retry) + 1

            if message:
                times = self.data["messages"].get(_hash(message), [])
                if any(now - t < self.rules["duplicate_window"] for t in times):
                    return False, "duplicate", 0

            for rule in ("global_hour", "global_day"):
                limit, period = self.rules[rule]
                count, retry = self._count(self.data["global"], period, now)
                if count >= limit:
                    return False, "global_limit", int(retry) + 1

            return True, None, 0

    def record_sent(self, keys, email=None, message=None):
        """Bilježi uspješno poslanu poruku."""
        with self.lock:
            now = self.clock()
            for key in keys:
                self.data["sent"].setdefault(key, []).append(now)
                self.data["captcha"].pop(key, None)
            if email:
                self.data["emails"].setdefault(_hash(email), []).append(now)
            if message:
                self.data["messages"].setdefault(_hash(message), []).append(now)
            self.data["global"].append(now)
            self._save()

    def record_captcha_failure(self, keys):
        """Bilježi pogrešan captcha odgovor. Vraća True ako je posjetilac sada zaključan."""
        with self.lock:
            now = self.clock()
            limit, period = self.rules["captcha_failures"]
            locked = False
            for key in keys:
                times = [t for t in self.data["captcha"].get(key, []) if now - t < period] + [now]
                self.data["captcha"][key] = times
                if len(times) >= limit:
                    self.data["locked"][key] = now + self.rules["captcha_lockout"]
                    self.data["captcha"][key] = []
                    locked = True
            self._save()
            return locked

    def remaining(self, keys):
        """Koliko još poruka posjetilac može poslati danas."""
        with self.lock:
            now = self.clock()
            limit, period = self.rules["per_client"]
            used = max((self._count(self.data["sent"].get(k, []), period, now)[0] for k in keys), default=0)
            return max(0, limit - used)


def default_storage_path():
    return os.path.join(tempfile.gettempdir(), "cv_contact_rate_limit.json")


def format_wait(seconds, lang):
    """120 -> '2 min', 7200 -> '2 h'"""
    if seconds < MINUTE:
        return {"bs": f"{seconds} s", "en": f"{seconds} s", "de": f"{seconds} s"}[lang]
    if seconds < HOUR:
        minutes = (seconds + 59) // 60
        return f"{minutes} min"
    hours = (seconds + HOUR - 1) // HOUR
    return {"bs": f"{hours} h", "en": f"{hours} h", "de": f"{hours} Std."}[lang]
