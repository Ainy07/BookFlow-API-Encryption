
from builtins import print
from app.utils.encryption import encrypt_data 

def encrypt_isbn(isbn):
    encrypted_isbn = encrypt_data(isbn)
    return encrypted_isbn

if __name__ == "__main__":
    isbn_to_encrypt = "1234567890123"
    encrypted = encrypt_isbn(isbn_to_encrypt)
    print(f"Original ISBN: {isbn_to_encrypt}")
    print(f"Encrypted ISBN: {encrypted}")
