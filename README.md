# BookFlow-API-Encryption

**BookFlow-API-Encryption** is a Django RESTful API for managing books, loans, reviews, and user profiles with built-in encryption for sensitive data such as ISBN numbers. The API ensures secure storage and handling of book information using Fernet symmetric encryption from the cryptography library.

---

## BookFlow API

A secure and feature-rich RESTful API for managing books, categories, users, loans, reviews, and wishlists built with Django REST Framework. The API includes AES encryption for sensitive data such as ISBN.

---

## Features

- User registration and authentication (token-based)
- Manage book categories and detailed book info
- AES encryption/decryption for sensitive data (e.g., ISBN)
- Book loans with copy availability tracking
- Reviews and ratings for books
- User-specific wishlists with add/remove functionality
- Filtering and searching books by author, title, ISBN, and categories

---

## Tech Stack

- Python 3.x  
- Django 4.x  
- Django REST Framework  
- Django Filter  
- Cryptography (Fernet AES encryption)  
- SQLite (default DB, can be changed)

---

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/Ainy07/bookflow-api.git
    cd bookflow-api
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python -m venv env
    # On Linux/Mac
    source env/bin/activate
    # On Windows
    env\Scripts\activate
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set your AES encryption key in Django settings (`settings.py`):**

    ```python
    AES_SECRET_KEY = b'your_32_byte_base64_encoded_key_here'  # Must be 32 bytes, base64 encoded for Fernet
    ```

    You can generate a key in Python:

    ```python
    from cryptography.fernet import Fernet
    print(Fernet.generate_key().decode())
    ```

5. **Run migrations:**

    ```bash
    python manage.py migrate
    ```

6. **Create a superuser (optional, for admin access):**

    ```bash
    python manage.py createsuperuser
    ```

7. **Start the server:**

    ```bash
    python manage.py runserver
    ```

---

## API Endpoints

| Endpoint                        | Method              | Description                          | Authentication  |
| -------------------------------|---------------------|------------------------------------|-----------------|
| `/users/`                      | GET, POST, PUT, DELETE | Manage users                       | Token Required  |
| `/categories/`                 | GET, POST, PUT, DELETE | Manage book categories             | Token Required  |
| `/books/`                     | GET, POST, PUT, DELETE | Manage books                      | Token Required  |
| `/books/encrypt/`             | POST                | Encrypt given text                  | No              |
| `/books/decrypt/`             | POST                | Decrypt given encrypted text       | No              |
| `/loans/`                     | GET, POST, PUT, DELETE | Manage book loans                  | Token Required  |
| `/loans/{id}/return_book/`    | POST                | Return a loaned book                | Token Required  |
| `/login/`                     | POST                | User login, returns authentication token | No          |
| `/books/{book_id}/reviews/`   | GET, POST           | List and add reviews for a book    | Token Required  |
| `/wishlists/`                 | GET, POST, PUT, DELETE | Manage user wishlists              | Token Required  |
| `/wishlists/add_book/`        | POST                | Add book to wishlist                | Token Required  |
| `/wishlists/remove_book/`     | POST                | Remove book from wishlist           | Token Required  |

---

## Encryption

Sensitive data such as ISBNs are encrypted using AES encryption via the cryptography package's Fernet symmetric encryption scheme. The encryption key is set via the Django settings (`AES_SECRET_KEY`). The API provides endpoints to encrypt and decrypt any arbitrary text.

---

## Usage Example

### Login

```bash
POST /login/
{
  "username": "user1",
  "password": "yourpassword"
}


Response:
{
  "token": "yourauthtoken"
}

Encrypt text
POST /books/encrypt/
{
  "text": "1234567890"
}

Response:
{
  "encrypted": "gAAAAABh..."
}

Decrypt text
POST /books/decrypt/
{
  "encrypted_text": "gAAAAABh..."
}

Response:
{
  "decrypted": "1234567890"
}

Contributing
Feel free to submit issues or pull requests for improvements and bug fixes.