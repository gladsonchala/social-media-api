# The SECRET_KEY should be long, random, and secret. 
# You can generate one with openssl rand -hex 32 on MacOS or Linux, or on Windows.
# Generated once!!!!!!!!
import secrets
import string

def generate_secret_key(length=32):
    characters = string.ascii_letters + string.digits + string.punctuation
    secret_key = ''.join(secrets.choice(characters) for _ in range(length))
    return secret_key

# Generate a secret key of length 32
secret_key = generate_secret_key()
print(secret_key)
