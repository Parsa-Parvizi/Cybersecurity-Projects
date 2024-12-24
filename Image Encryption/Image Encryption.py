from PIL import Image
from cryptography.fernet import Fernet
import os
from base64 import b64encode, b64decode

def generate_key(key_size=32):
  """
  Generates a secure random key for encryption.

  Args:
      key_size (int, optional): The desired key size in bytes. Defaults to 32.

  Returns:
      bytes: The generated encryption key.
  """

  return Fernet.generate_key(key_size)

def save_key(key, key_file_path="image_encryption_key.key"):
  """
  Saves the encryption key to a file securely.

  Args:
      key (bytes): The encryption key to save.
      key_file_path (str, optional): The path to the file where the key will be saved.
          Defaults to "image_encryption_key.key".
  """

  if not os.path.exists(os.path.dirname(key_file_path)):
    os.makedirs(os.path.dirname(key_file_path))

  with open(key_file_path, 'wb') as key_file:
    key_file.write(b64encode(key))  # Base64 encode for better portability

def load_key(key_file_path="image_encryption_key.key"):
  """
  Loads the encryption key from a file.

  Args:
      key_file_path (str, optional): The path to the file containing the key.
          Defaults to "image_encryption_key.key".

  Returns:
      bytes: The loaded encryption key.

  Raises:
      FileNotFoundError: If the key file is not found.
  """

  if not os.path.exists(key_file_path):
    raise FileNotFoundError(f"Key file not found: {key_file_path}")

  with open(key_file_path, 'rb') as key_file:
    return b64decode(key_file.read())  # Base64 decode

def encrypt_image(image_path, key, output_dir="encrypted_images"):
  """
  Encrypts an image using Fernet encryption.

  Args:
      image_path (str): The path to the image file to encrypt.
      key (bytes): The encryption key.
      output_dir (str, optional): The directory to save the encrypted image.
          Defaults to "encrypted_images".

  Returns:
      str: The path to the encrypted image file.
  """

  if not os.path.exists(output_dir):
    os.makedirs(output_dir)

  image_name = os.path.basename(image_path)
  encrypted_image_path = os.path.join(output_dir, f"{image_name}.enc")

  with open(image_path, 'rb') as image_file:
    image_data = image_file.read()

  cipher_suite = Fernet(key)
  encrypted_data = cipher_suite.encrypt(image_data)

  with open(encrypted_image_path, 'wb') as encrypted_file:
    encrypted_file.write(encrypted_data)

  return encrypted_image_path

def decrypt_image(encrypted_image_path, key):
  """
  Decrypts an encrypted image using Fernet encryption.

  Args:
      encrypted_image_path (str): The path to the encrypted image file.
      key (bytes): The encryption key.

  Returns:
      str: The path to the decrypted image file.
  """

  image_name = os.path.splitext(os.path.basename(encrypted_image_path))[0]
  decrypted_image_path = os.path.join(os.path.dirname(encrypted_image_path), f"{image_name}.dec.jpg")

  with open(encrypted_image_path, 'rb') as encrypted_file:
    encrypted_data = encrypted_file.read()

  cipher_suite = Fernet(key)
  decrypted_data = cipher_suite.decrypt(encrypted_data)

  with open(decrypted_image_path, 'wb') as decrypted_file:
    decrypted_file.write(decrypted_data)

  return decrypted_image_path

if __name__ == "__main__":
  """
  This section handles user interaction and program execution.
  """

  # User choice: Generate or load key
  while True:
    choice = input("Do you want to generate a new key (g) or load an existing key (l)? ").lower()
    if choice in ("g", "l"):
      break
    else:
      print("Invalid choice. Please enter 'g' or 'l'.")

  # Generate or load key based on user choice
  if choice == "g":
    try:
      key = generate_key()
      print("New key generated successfully!")
    except Exception as e:
      print(f"Error generating key: {e}")
      exit(1)
  else:
    key_file_path = "image_encryption_key.key"
    try:
      key = load_key(key_file_path)
      print("Key loaded successfully from", key_file_path)
    except FileNotFoundError:
      print(f"Key file not found: {key_file_path}")
      print("Generating a new key...")
      key = generate_key()
      print("New key generated and saved to", key_file_path)

  # User choice: Encrypt or decrypt
  while True:
    choice = input("Do you want to encrypt (e) or decrypt (d) an image? ").lower()
    if choice in ("e", "d"):
      break
    else:
      print("Invalid choice. Please enter 'e' or 'd'.")

  # Get image path from user
  image_path = input("Enter the path to the image file: ")

  # Encrypt or decrypt image based on user choice
  if choice == "e":
    try:
      encrypted_image_path = encrypt_image(image_path, key)
      print("Image encrypted successfully! Encrypted image:", encrypted_image_path)
    except Exception as e:
      print(f"Error encrypting image: {e}")
  else:
    try:
      decrypted_image_path = decrypt_image(image_path, key)
      print("Image decrypted successfully! Decrypted image:", decrypted_image_path)
    except Exception as e:
      print(f"Error decrypting image: {e}")