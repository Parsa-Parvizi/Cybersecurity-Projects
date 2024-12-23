from collections import deque

# You might need to install these libraries:
# pip install pycipher 

from pycipher import Caesar, Vigenere

def caesar_encrypt(text, shift):
    """
    Encrypts text using the Caesar Cipher.

    Args:
        text: The text to be encrypted.
        shift: The number of positions to shift the letters.

    Returns:
        The encrypted text.
    """
    return Caesar(shift).encipher(text)

def vigenere_encrypt(text, key):
    """
    Encrypts text using the Vigenere Cipher.

    Args:
        text: The text to be encrypted.
        key: The encryption key.

    Returns:
        The encrypted text.
    """
    return Vigenere(key).encipher(text)

def railfence_encrypt(text, rails):
    """
    Encrypts text using the Railfence Cipher.

    Args:
        text: The text to be encrypted.
        rails: The number of rails.

    Returns:
        The encrypted text.
    """
    rail = [[] for _ in range(rails)]
    direction = 1
    row = 0

    for i in range(len(text)):
        rail[row].append(text[i])
        row += direction

        if row == 0 or row == rails - 1:
            direction *= -1

    result = ""
    for row in rail:
        result += "".join(row)

    return result

def main():
    print("Welcome to the Text Encryption Tool!")
    while True:
        print("\nChoose an encryption method:")
        print("1. Caesar Cipher")
        print("2. Vigenere Cipher")
        print("3. Railfence Cipher")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            text = input("Enter the text to encrypt: ")
            shift = int(input("Enter the shift value: "))
            encrypted_text = caesar_encrypt(text, shift)
            print(f"Encrypted text: {encrypted_text}")

        elif choice == '2':
            text = input("Enter the text to encrypt: ")
            key = input("Enter the encryption key: ")
            encrypted_text = vigenere_encrypt(text, key)
            print(f"Encrypted text: {encrypted_text}")

        elif choice == '3':
            text = input("Enter the text to encrypt: ")
            rails = int(input("Enter the number of rails: "))
            encrypted_text = railfence_encrypt(text, rails)
            print(f"Encrypted text: {encrypted_text}")

        elif choice == '4':
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
