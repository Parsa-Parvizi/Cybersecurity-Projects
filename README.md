# Security-Algorithms

Overview
The Text Encryption Tool is a command-line application that provides various encryption methods to secure text data. This tool implements three classical encryption algorithms: Caesar Cipher, Vigenere Cipher, and Railfence Cipher. The application is designed to be user-friendly, allowing users to easily encrypt and decrypt messages using these algorithms.

Features
Caesar Cipher: A simple substitution cipher where each letter in the plaintext is shifted a fixed number of places down or up the alphabet. This method is easy to implement and understand, making it a great introduction to cryptography.

Vigenere Cipher: A method of encrypting alphabetic text by using a simple form of polyalphabetic substitution. The Vigenere Cipher uses a keyword to determine the shift for each letter, providing a more secure encryption compared to the Caesar Cipher.

Railfence Cipher: A transposition cipher that writes the plaintext in a zigzag pattern across multiple "rails" and then reads off each rail in order. This method is visually interesting and demonstrates the concept of transposition in cryptography.

Implementation
The tool is implemented in three programming languages:

Python: The Python version utilizes the pycipher library for the Caesar and Vigenere ciphers, while the Railfence cipher is implemented manually. The code is structured with clear functions for each cipher, making it easy to follow and modify.

JavaScript: The JavaScript version is designed to run in a Node.js environment. It provides similar functionality to the Python version, with functions for each cipher and a command-line interface for user interaction.

Go: The Go version is implemented with a focus on performance and simplicity. It uses Go's built-in features to handle string manipulation and user input, providing a clean and efficient implementation of the encryption algorithms.

Usage
To use the Text Encryption Tool, follow these steps:

Clone the Repository:

bash

Verify

Open In Editor
Run
Copy code
git clone https://github.com/yourusername/text-encryption-tool.git
cd text-encryption-tool
Run the Tool:

For Python:
bash

Verify

Open In Editor
Run
Copy code
python3 main.py
For JavaScript:
bash

Verify

Open In Editor
Run
Copy code
node main.js
For Go:
bash

Verify

Open In Editor
Run
Copy code
go run main.go
Select an Encryption Method: Choose from the available options (Caesar Cipher, Vigenere Cipher, Railfence Cipher) and follow the prompts to encrypt or decrypt your text.

Example
Here’s a quick example of how to use the tool:

Choose the Caesar Cipher.
Enter the text: Hello, World!
Choose to encrypt and enter a shift value of 3.
The output will be: Khoor, Zruog!
Contributing
Contributions are welcome! If you have suggestions for improvements or additional features, feel free to open an issue or submit a pull request.

License
This project is licensed under the MIT License - see the LICENSE file for details.
