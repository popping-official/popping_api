import random
import string

def generate_auth_code(length=8):
    characters = string.ascii_letters + string.digits 
    code = ''.join(random.choice(characters) for _ in range(length))
    return code