def generate_response(messages):
    # Definiši ključne reči za različite jezike
    bosnian_keywords = [
        "radno iskustvo", "See Contact", "2014", "koje godine si radio u BH Telecom", "telecom", "Telinvest",
        "koje godine si radio u Telinvest", "2015", "koje godine si radio u logosoftu", "koje godine si radio u ataco",
        "ataco", "logosoft", "koje godine si radio u foreo", "koje godine si radio u logosoftu", "logosoft", "payten",
        "koje godine si radio u capital market solutions", "koje godine si radio u payten", "CMS", "foreo", "poslovi",
        "koji su tvoji budući planovi", "planovi", "gdje si radio", "radio", "sada", "kako da te kontaktiram", "kontakt",
        "kako se zoves", "ime", "Kako si?", "kako si ti?", "šta ima?", "šta radiš?", "gdje trenutno radiš"
    ]
    german_keywords = [
        "arbeitsplätze", "See Contact", "2014", "in welchem jahr haben sie bei BH Telecom gearbeitet", "telecom",
        "Telinvest", "in welchem jahr haben sie bei telinvest gearbeitet", "in welchem jahr haben sie bei payten gearbeitet",
        "in welchem jahr haben sie bei ataco gearbeitet", "ataco", "in welchem jahr haben sie bei capital markt solutions gearbeitet",
        "CMS", "payten", "logosoft", "in welchem jahr haben sie bei foreo gearbeitet", "in welchem jahr haben sie bei logosoft gearbeitet",
        "logosoft", "in welchem jahr haben sie bei capital market solutions gearbeitet", "CMS", "foreo", "arbeitserfahrung",
        "was sind deine zukunftspläne", "pläne", "arbeiten", "im augenblick", "wo hast du gearbeitet", "wie kann ich dich kontaktieren",
        "kontakt", "wie heißt du", "name", "Wie geht es dir?", "Was geht?", "was machst du gerade?", "wo sie derzeit arbeiten"
    ]
    english_keywords = [
        "where have you worked", "See Contact", "2014", "Telinvest", "what year did you work at BH Telecom", "telecom",
        "2015", "what year did you work at telinvest", "what year did you work at Ataco", "ataco", "what year did you work at payten",
        "payten", "what year did you work at foreo", "what year did you work at Logosoft", "what year did you work at capital market solutions",
        "logosoft", "foreo", "capital market solutions", "CMS", "right now", "what are your future plans", "plans",
        "where did you work", "how can i contact you", "contact", "what is your name", "name", "How are you?", "What's up?", "What are you doing?",
        "where are you currently working"
    ]

    # Prolazi kroz sve poruke
    for msg in messages:
        content = msg["content"].lower()
        
        # Identifikuj jezik pitanja
        if any(keyword in content for keyword in bosnian_keywords):
            language = 'bosnian'
        elif any(keyword in content for keyword in german_keywords):
            language = 'german'
        elif any(keyword in content for keyword in english_keywords):
            language = 'english'
        else:
            language = 'unknown'
        
        # Generiši odgovor na osnovu identifikovanog jezika
        if language == 'bosnian':
            if any(keyword in content for keyword in ["kako se zoves", "ime"]):
                return "Moje ime je Amar Helac"
            if any(keyword in content for keyword in ["koji su tvoji budući planovi", "planovi", "cilj"]):
                return "Imam veliki interes da se bavim konkretnije Devops dijelom te svi moji planovi vode ka tom cilju"
            for position, response in job_positions.items():
                if position in content:
                    return response[0]
        
        elif language == 'german':
            if any(keyword in content for keyword in ["wie heißt du", "name"]):
                return "Mein Name ist Amar Helac"
            if any(keyword in content for keyword in ["was sind deine zukunftspläne", "pläne", "ziel"]):
                return "Ich habe ein großes Interesse daran, mich konkreter mit dem Devops-Teil auseinanderzusetzen, und alle meine Pläne führen auf dieses Ziel hin"
            for position, response in job_positions.items():
                if position in content:
                    return response[1]
        
        elif language == 'english':
            if any(keyword in content for keyword in ["what is your name", "name"]):
                return "My name is Amar Helac"
            if any(keyword in content for keyword in ["what are your future plans", "plans", "goal"]):
                return "I have a great interest in dealing more specifically with the Devops part, and all my plans lead to that goal"
            for position, response in job_positions.items():
                if position in content:
                    return response[2]

    return "Sorry, I don't understand your request."
