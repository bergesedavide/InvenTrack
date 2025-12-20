import random

LENGTH = 12
NUMBERS = '0123456789'
CHARACTERS_LOW = 'abcdefghijklmnopqrstuvwxyz'
CHARACTERS_HIGH = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
CHARACTERS_SPECIAL = '!@#$%&*_-?'

def generate_password(length=LENGTH, use_numbers=True, use_lowercase=True, use_uppercase=True, use_special=True) -> str:
    # Costruisce il set di caratteri disponibili
    characters = ''
    required_chars = []
    
    if use_numbers:
        characters += NUMBERS
        required_chars.append(random.choice(NUMBERS))
    
    if use_lowercase:
        characters += CHARACTERS_LOW
        required_chars.append(random.choice(CHARACTERS_LOW))
    
    if use_uppercase:
        characters += CHARACTERS_HIGH
        required_chars.append(random.choice(CHARACTERS_HIGH))
    
    if use_special:
        characters += CHARACTERS_SPECIAL
        required_chars.append(random.choice(CHARACTERS_SPECIAL))
    
    # Verifica che ci sia almeno un tipo di carattere selezionato
    if not characters:
        raise ValueError("Devi selezionare almeno un tipo di carattere!")
    
    # Genera il resto della password
    remaining_length = length - len(required_chars)
    if remaining_length < 0:
        remaining_length = 0
    
    password_list = required_chars + [random.choice(characters) for _ in range(remaining_length)]
    
    # Mescola i caratteri per rendere la password più casuale
    random.shuffle(password_list)
    
    print(''.join(password_list))
    return ''.join(password_list)

def generate_multiple_passwords(count=5, length=LENGTH):
    return [generate_password(length) for _ in range(count)]

def check_password_strength(password):
    global NUMBERS

    score = 0
    feedback = []
    
    # Controlla lunghezza
    if len(password) >= 12:
        score += 2
        feedback.append("✓ Lunghezza adeguata")
    elif len(password) >= 8:
        score += 1
        feedback.append("⚠ Lunghezza accettabile, ma potrebbe essere più lunga")
    else:
        feedback.append("✗ Password troppo corta")
    
    # Controlla presenza di numeri
    if any(c in NUMBERS for c in password):
        score += 1
        feedback.append("✓ Contiene numeri")
    else:
        feedback.append("✗ Non contiene numeri")
    
    # Controlla lettere minuscole
    if any(c in CHARACTERS_LOW for c in password):
        score += 1
        feedback.append("✓ Contiene lettere minuscole")
    else:
        feedback.append("✗ Non contiene lettere minuscole")
    
    # Controlla lettere maiuscole
    if any(c in CHARACTERS_HIGH for c in password):
        score += 1
        feedback.append("✓ Contiene lettere maiuscole")
    else:
        feedback.append("✗ Non contiene lettere maiuscole")
    
    # Controlla caratteri speciali
    if any(c in CHARACTERS_SPECIAL for c in password):
        score += 1
        feedback.append("✓ Contiene caratteri speciali")
    else:
        feedback.append("✗ Non contiene caratteri speciali")
    
    # Determina il livello di sicurezza
    if score >= 5:
        strength = "FORTE"
    elif score >= 3:
        strength = "MEDIA"
    else:
        strength = "DEBOLE"
    
    print({
        'score': score,
        'max_score': 6,
        'strength': strength,
        'feedback': feedback
    })

    return {
        'score': score,
        'max_score': 6,
        'strength': strength,
        'feedback': feedback
    }

pwd = generate_password()
check_password_strength(pwd)