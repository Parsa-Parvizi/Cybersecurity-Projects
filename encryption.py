from collections import deque
from pycipher import Caesar, Vigenere

def caesar_encrypt(text, shift):
    """
    Encrypts text using the Caesar Cipher.

    Args:
        text (str): The text to be encrypted.
        shift (int): The number of positions to shift the letters.

    Returns:
        str: The encrypted text.
    """
    return Caesar(shift).encipher(text)

def caesar_decrypt(text, shift):
    """
    Decrypts text using the Caesar Cipher.

    Args:
        text (str): The text to be decrypted.
        shift (int): The number of positions to shift the letters.

    Returns:
        str: The decrypted text.
    """
    return Caesar(-shift).encipher(text)

def vigenere_encrypt(text, key):
    """
    Encrypts text using the Vigenere Cipher.

    Args:
        text (str): The text to be encrypted.
        key (str): The encryption key.

    Returns:
        str: The encrypted text.
    """
    return Vigenere(key).encipher(text)

def vigenere_decrypt(text, key):
    """
    Decrypts text using the Vigenere Cipher.

    Args:
        text (str): The text to be decrypted.
        key (str): The encryption key.

    Returns:
        str: The decrypted text.
    """
    return Vigenere(key).decipher(text)

def railfence_encrypt(text, rails):
    """
    Encrypts text using the Railfence Cipher.

    Args:
        text (str): The text to be encrypted.
        rails (int): The number of rails.

    Returns:
        str: The encrypted text.
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

def railfence_decrypt(text, rails):
    """
    Decrypts text using the Railfence Cipher.

    Args:
        text (str): The text to be decrypted.
        rails (int): The number of rails.

    Returns:
        str: The decrypted text.
    """
    n = len(text)
    rail = [['\n' for _ in range(n)] for _ in range(rails)]
    direction = None
    row, col = 0, 0

    for i in range(n):
        if row == 0:
            direction = 1
        if row == rails - 1:
            direction = -1

        rail[row][col] = '*'
        col += 1
        row += direction

    index = 0
    for i in range(rails):
        for j in range(n):
            if (rail[i][j] == '*' and index < n):
                rail[i][j] = text[index]
                index += 1

    result = []
    row, col = 0, 0
    for i in range(n):
        if row == 0:
            direction = 1
        if row == rails - 1:
            direction = -1

        if rail[row][col] != '*':
            result.append(rail[row][col])
            col += 1

        row += direction

    return ''.join(result)

def main():
    """
    Main function to run the Text Encryption Tool.
    Provides a user interface for selecting encryption methods and performing encryption/decryption.
    """
    print("Welcome to the Text Encryption Tool!")
    while True:
        print("\nChoose an option:")
        print("1. Caesar Cipher")
        print("2. Vigenere Cipher")
        print("3. Railfence Cipher")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            text = input("Enter the text to encrypt/decrypt: ")
            action = input("Do you want to (e)ncrypt or (d)ecrypt? ")
            shift = int(input("Enter the shift value: "))
            if action.lower() == 'e':
                encrypted_text = caesar_encrypt(text, shift)
                print(f"Encrypted text: {encrypted_text}")
            elif action.lower() == 'd':
                decrypted_text = caesar_decrypt(text, shift)
                print(f"Decrypted text: {decrypted_text}")
            else:
                print("Invalid action. Please choose 'e' or 'd'.")

        elif choice == '2':
            text = input("Enter the text to encrypt/decrypt: ")
            action = input("Do you want to (e)ncrypt or (d)ecrypt? ")
            key = input("Enter the encryption key: ")
            if action.lower() == 'e':
                encrypted_text = vigenere_encrypt(text, key)
                print(f"Encrypted text: {encrypted_text}")
            elif action.lower() == 'd':
                decrypted_text = vigenere_decrypt(text, key)
                print(f"Decrypted text: {decrypted_text}")
            else:
                print("Invalid action. Please choose 'e' or 'd'.")

        elif choice == '3':
            text = input("Enter the text to encrypt/decrypt: ")
            action = input("Do you want to (e)ncrypt or (d)ecrypt? ")
            rails = int(input("Enter the number of rails: "))
            if action.lower() == 'e':
                encrypted_text = railfence_encrypt(text, rails)
                print(f"Encrypted text: {encrypted_text}")
            elif action.lower() == 'd':
                decrypted_text = railfence_decrypt(text, rails)
                print(f"Decrypted text: {decrypted_text}")
            else:
                print("Invalid action. Please choose 'e' or 'd'.")

        elif choice == '4':
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
