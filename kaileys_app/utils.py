import string
import random

def generate_unique_code(length=8):
    from .models import AccessCode  # <-- move import here
    characters = string.ascii_uppercase + string.digits
    while True:
        code = ''.join(random.choices(characters, k=length))
        if not AccessCode.objects.filter(code=code).exists():
            return code
