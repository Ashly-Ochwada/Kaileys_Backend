import string
import random
from django.db import DatabaseError

def generate_unique_code(length=8):
    """
    Generate a unique alphanumeric code for AccessCode model.
    
    Args:
        length (int): Length of the code to generate. Defaults to 8.

    Returns:
        str: A unique code consisting of uppercase letters and digits.

    Raises:
        ValueError: If a unique code cannot be generated after max attempts.
        DatabaseError: If there's an issue querying the database.
    """
    # Define the character set: uppercase letters (A-Z) and digits (0-9)
    characters = string.ascii_uppercase + string.digits

    # Import AccessCode here to avoid circular imports
    from .models import AccessCode

    # Set a maximum number of attempts to avoid infinite loops
    max_attempts = 10
    attempts = 0

    while attempts < max_attempts:
        # Generate a random code of the specified length
        code = ''.join(random.choices(characters, k=length))
        try:
            # Check if the code already exists in the database
            if not AccessCode.objects.filter(code=code).exists():
                return code
        except DatabaseError as e:
            # Handle potential database errors (e.g., connection issues)
            raise DatabaseError(f"Failed to check code uniqueness: {str(e)}")

        # Increment attempts and continue if code is not unique
        attempts += 1

    # Raise an error if a unique code couldn't be generated
    raise ValueError(f"Unable to generate a unique code after {max_attempts} attempts")