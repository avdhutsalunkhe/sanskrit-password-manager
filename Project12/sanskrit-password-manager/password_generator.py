import random
import string
import secrets
from typing import Dict, List

class SanskritPasswordGenerator:
    def __init__(self):
        self.sanskrit_words = [
            'dharma', 'karma', 'moksha', 'ahimsa', 'satya', 'shanti', 'brahman',
            'atman', 'yoga', 'meditation', 'mantra', 'chakra', 'guru', 'ashram',
            'vedanta', 'samadhi', 'nirvana', 'samsara', 'tapas', 'seva'
        ]
        
        self.sanskrit_meanings = {
            'dharma': 'righteousness',
            'karma': 'action',
            'moksha': 'liberation',
            'ahimsa': 'non-violence',
            'satya': 'truth',
            'shanti': 'peace',
            'brahman': 'ultimate reality',
            'atman': 'soul',
            'yoga': 'union',
            'meditation': 'dhyana'
        }
    
    def generate_sanskrit_password(self, length=12, include_symbols=True, 
                                 include_numbers=True, include_uppercase=True, 
                                 include_lowercase=True, exclude_ambiguous=False,
                                 min_numbers=0, min_symbols=0, exclude_chars=''):
        
        base_word = random.choice(self.sanskrit_words)
        
        # Build character set
        chars = ""
        if include_lowercase:
            chars += string.ascii_lowercase
        if include_uppercase:
            chars += string.ascii_uppercase
        if include_numbers:
            chars += string.digits
        if include_symbols:
            chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        if exclude_ambiguous:
            ambiguous = "0O1lI"
            chars = ''.join(c for c in chars if c not in ambiguous)
        
        if exclude_chars:
            chars = ''.join(c for c in chars if c not in exclude_chars)
        
        # Generate password starting with Sanskrit word
        password = base_word.capitalize()
        remaining_length = length - len(password)
        
        if remaining_length > 0:
            # Ensure minimum requirements
            required_chars = []
            if min_numbers > 0 and include_numbers:
                required_chars.extend(secrets.choice(string.digits) for _ in range(min_numbers))
            if min_symbols > 0 and include_symbols:
                required_chars.extend(secrets.choice("!@#$%^&*") for _ in range(min_symbols))
            
            # Fill remaining with random characters
            remaining_after_requirements = remaining_length - len(required_chars)
            if remaining_after_requirements > 0:
                random_chars = [secrets.choice(chars) for _ in range(remaining_after_requirements)]
                required_chars.extend(random_chars)
            
            # Shuffle and append
            random.shuffle(required_chars)
            password += ''.join(required_chars[:remaining_length])
        
        return {
            'password': password,
            'sanskrit_word': base_word,
            'meaning': self.sanskrit_meanings.get(base_word, 'wisdom'),
            'character_types': self._get_character_types(password),
            'entropy': self._calculate_entropy(password)
        }
    
    def generate_phrase_password(self, word_count=4, separator='-', 
                               include_numbers=True, capitalize=True):
        words = random.sample(self.sanskrit_words, min(word_count, len(self.sanskrit_words)))
        
        if capitalize:
            words = [word.capitalize() for word in words]
        
        password = separator.join(words)
        
        if include_numbers:
            password += separator + str(random.randint(100, 999))
        
        return {
            'password': password,
            'words': words,
            'separator': separator,
            'character_types': self._get_character_types(password),
            'entropy': self._calculate_entropy(password)
        }
    
    def generate_pin(self, length=6):
        pin = ''.join(secrets.choice(string.digits) for _ in range(length))
        return {
            'password': pin,
            'type': 'pin',
            'character_types': ['digits'],
            'entropy': self._calculate_entropy(pin)
        }
    
    def generate_memorable_password(self, length=12, include_symbols=True, include_numbers=True):
        word = random.choice(self.sanskrit_words)
        password = word.capitalize()
        
        if include_numbers:
            password += str(random.randint(10, 99))
        
        if include_symbols:
            password += random.choice('!@#$%')
        
        # Pad to desired length
        while len(password) < length:
            password += secrets.choice(string.ascii_letters + string.digits)
        
        return {
            'password': password[:length],
            'base_word': word,
            'character_types': self._get_character_types(password),
            'entropy': self._calculate_entropy(password)
        }
    
    def _get_character_types(self, password):
        types = []
        if any(c.islower() for c in password):
            types.append('lowercase')
        if any(c.isupper() for c in password):
            types.append('uppercase')
        if any(c.isdigit() for c in password):
            types.append('digits')
        if any(not c.isalnum() for c in password):
            types.append('symbols')
        return types
    
    def _calculate_entropy(self, password):
        charset_size = 0
        if any(c.islower() for c in password):
            charset_size += 26
        if any(c.isupper() for c in password):
            charset_size += 26
        if any(c.isdigit() for c in password):
            charset_size += 10
        if any(not c.isalnum() for c in password):
            charset_size += 32
        
        import math
        return len(password) * math.log2(charset_size) if charset_size > 0 else 0
