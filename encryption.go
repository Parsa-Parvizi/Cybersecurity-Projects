package main

import (
	"fmt"
	"strings"
)

// Caesar Cipher Functions
func caesarEncrypt(text string, shift int) string {
	result := ""
	for _, char := range text {
		if char >= 'A' && char <= 'Z' {
			result += string((int(char)+shift-65)%26 + 65)
		} else if char >= 'a' && char <= 'z' {
			result += string((int(char)+shift-97)%26 + 97)
		} else {
			result += string(char) // Non-alphabetic characters remain unchanged
		}
	}
	return result
}

func caesarDecrypt(text string, shift int) string {
	return caesarEncrypt(text, -shift)
}

// Vigenere Cipher Functions
func vigenereEncrypt(text, key string) string {
	result := ""
	keyIndex := 0
	for _, char := range text {
		if char >= 'A' && char <= 'Z' {
			result += string((int(char)+int(key[keyIndex%len(key)])-2*65)%26 + 65)
			keyIndex++
		} else if char >= 'a' && char <= 'z' {
			result += string((int(char)+int(key[keyIndex%len(key)])-2*97)%26 + 97)
			keyIndex++
		} else {
			result += string(char) // Non-alphabetic characters remain unchanged
		}
	}
	return result
}

func vigenereDecrypt(text, key string) string {
	result := ""
	keyIndex := 0
	for _, char := range text {
		if char >= 'A' && char <= 'Z' {
			result += string((int(char)-int(key[keyIndex%len(key)])+26)%26 + 65)
			keyIndex++
		} else if char >= 'a' && char <= 'z' {
			result += string((int(char)-int(key[keyIndex%len(key)])+26)%26 + 97)
			keyIndex++
		} else {
			result += string(char) // Non-alphabetic characters remain unchanged
		}
	}
	return result
}

// Railfence Cipher Functions
func railfenceEncrypt(text string, rails int) string {
	if rails <= 0 {
		panic("Number of rails must be greater than 0.")
	}
	if text == "" {
		return ""
	}

	rail := make([]string, rails)
	direction := 1 // 1 means moving down, -1 means moving up
	row := 0       // Start at the first rail

	for _, char := range text {
		rail[row] += string(char)

		if row == 0 {
			direction = 1 // Move down
		} else if row == rails-1 {
			direction = -1 // Move up
		}

		row += direction
	}

	return strings.Join(rail, "")
}

func railfenceDecrypt(text string, rails int) string {
	n := len(text)
	rail := make([][]rune, rails)
	for i := range rail {
		rail[i] = make([]rune, n)
		for j := range rail[i] {
			rail[i][j] = '\n'
		}
	}

	direction := 0
	row, col := 0, 0

	for i := 0; i < n; i++ {
		if row == 0 {
			direction = 1
		}
		if row == rails-1 {
			direction = -1
		}

		rail[row][col] = '*'
		col++
		row += direction
	}

	index := 0
	for i := 0; i < rails; i++ {
		for j := 0; j < n; j++ {
			if rail[i][j] == '*' && index < n {
				rail[i][j] = rune(text[index])
				index++
			}
		}
	}

	result := []rune{}
	row, col = 0, 0
	for i := 0; i < n; i++ {
		if row == 0 {
			direction = 1
		}
		if row == rails-1 {
			direction = -1
		}

		if rail[row][col] != '*' {
			result = append(result, rail[row][col])
			col++
		}

		row += direction
	}

	return string(result)
}

// Main Function
func main() {
	fmt.Println("Welcome to the Text Encryption Tool!")
	for {
		fmt.Println("\nChoose an option:")
		fmt.Println(" 1. Caesar Cipher")
		fmt.Println("2. Vigenere Cipher")
		fmt.Println("3. Railfence Cipher")
		fmt.Println("4. Exit")

		var choice int
		fmt.Print("Enter your choice (1-4): ")
		fmt.Scan(&choice)

		switch choice {
		case 1:
			var text string
			var action string
			var shift int
			fmt.Print("Enter the text to encrypt/decrypt: ")
			fmt.Scan(&text)
			fmt.Print("Do you want to (e)ncrypt or (d)ecrypt? ")
			fmt.Scan(&action)
			fmt.Print("Enter the shift value: ")
			fmt.Scan(&shift)

			if action == "e" {
				encryptedText := caesarEncrypt(text, shift)
				fmt.Printf("Encrypted text: %s\n", encryptedText)
			} else if action == "d" {
				decryptedText := caesarDecrypt(text, shift)
				fmt.Printf("Decrypted text: %s\n", decryptedText)
			} else {
				fmt.Println("Invalid action. Please choose 'e' or 'd'.")
			}

		case 2:
			var text string
			var action string
			var key string
			fmt.Print("Enter the text to encrypt/decrypt: ")
			fmt.Scan(&text)
			fmt.Print("Do you want to (e)ncrypt or (d)ecrypt? ")
			fmt.Scan(&action)
			fmt.Print("Enter the encryption key: ")
			fmt.Scan(&key)

			if action == "e" {
				encryptedText := vigenereEncrypt(text, key)
				fmt.Printf("Encrypted text: %s\n", encryptedText)
			} else if action == "d" {
				decryptedText := vigenereDecrypt(text, key)
				fmt.Printf("Decrypted text: %s\n", decryptedText)
			} else {
				fmt.Println("Invalid action. Please choose 'e' or 'd'.")
			}

		case 3:
			var text string
			var action string
			var rails int
			fmt.Print("Enter the text to encrypt/decrypt: ")
			fmt.Scan(&text)
			fmt.Print("Do you want to (e)ncrypt or (d)ecrypt? ")
			fmt.Scan(&action)
			fmt.Print("Enter the number of rails: ")
			fmt.Scan(&rails)

			if action == "e" {
				encryptedText := railfenceEncrypt(text, rails)
				fmt.Printf("Encrypted text: %s\n", encryptedText)
			} else if action == "d" {
				decryptedText := railfenceDecrypt(text, rails)
				fmt.Printf("Decrypted text: %s\n", decryptedText)
			} else {
				fmt.Println("Invalid action. Please choose 'e' or 'd'.")
			}

		case 4:
			fmt.Println("Exiting...")
			return

		default:
			fmt.Println("Invalid choice. Please select a valid option.")
		}
	}
}
