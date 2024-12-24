package main

import (
	"bufio"
	"crypto/rand"
	"encoding/base64"
	"errors"
	"fmt"
	"io/ioutil"
	"os"
	"github.com/google/go-crypto/fernet"
)

func generateKey(keySize int) ([]byte, error) {
	key := make([]byte, keySize)
	_, err := rand.Read(key)
	if err != nil {
		return nil, err
	}
	return key, nil
}

func saveKey(key []byte, keyFilePath string) error {
	encodedKey := base64.StdEncoding.EncodeToString(key)
	if err := ioutil.WriteFile(keyFilePath, []byte(encodedKey), 0600); err != nil {
		return fmt.Errorf("failed to save key to file: %w", err)
	}
	return nil
}

func loadKey(keyFilePath string) ([]byte, error) {
	data, err := ioutil.ReadFile(keyFilePath)
	if err != nil {
		return nil, fmt.Errorf("failed to read key file: %w", err)
	}
	decodedKey, err := base64.StdEncoding.DecodeString(string(data))
	if err != nil {
		return nil, fmt.Errorf("failed to decode key: %w", err)
	}
	return decodedKey, nil
}

func encryptImage(imagePath string, key []byte, outputDir string) (string, error) {
	data, err := ioutil.ReadFile(imagePath)
	if err != nil {
		return "", fmt.Errorf("failed to read image file: %w", err)
	}

	cipher := fernet.New(key)
	encryptedData, err := cipher.Encrypt(nil, data)
	if err != nil {
		return "", fmt.Errorf("failed to encrypt image: %w", err)
	}

	fileName := filepath.Base(imagePath)
	encryptedImagePath := filepath.Join(outputDir, fileName+".enc")

	if err := os.MkdirAll(outputDir, os.ModePerm(0755)); err != nil && !os.IsExist(err) {
		return "", fmt.Errorf("failed to create output directory: %w", err)
	}

	if err := ioutil.WriteFile(encryptedImagePath, encryptedData, 0644); err != nil {
		return "", fmt.Errorf("failed to write encrypted image: %w", err)
	}

	return encryptedImagePath, nil
}

func decryptImage(encryptedImagePath string, key []byte) (string, error) {
	data, err := ioutil.ReadFile(encryptedImagePath)
	if err != nil {
		return "", fmt.Errorf("failed to read encrypted image: %w", err)
	}

	cipher := fernet.New(key)
	decryptedData, err := cipher.Decrypt(nil, data)
	if err != nil {
		return "", fmt.Errorf("failed to decrypt image: %w", err)
	}

	fileName := filepath.Base(encryptedImagePath)
	decryptedImagePath := filepath.Join(filepath.Dir(encryptedImagePath), fileName+".dec.jpg")

	if err := ioutil.WriteFile(decryptedImagePath, decryptedData, 0644); err != nil {
		return "", fmt.Errorf("failed to write decrypted image: %w", err)
	}

	return decryptedImagePath, nil
}

func main() {
	reader := bufio.NewReader(os.Stdin)

	var key []byte
	var err error

	// Choose one of the options:
	// 1. Generate a new key
	fmt.Println("Do you want to generate a new key (g) or load an existing key (l)?")
	choice, err := reader.ReadString('\n')
	if err != nil {
			fmt.Println("Error reading input:", err)
			return
	}
	choice = strings.TrimSpace(choice)

	if choice == "g" {
			key, err = generateKey(32) // Adjust key size as needed
			if err != nil {
					fmt.Println("Error generating key:", err)
					return
			}

			// Save the key to a file (optional)
			keyFilePath := "my_encryption_key.key"
			if err := saveKey(key, keyFilePath); err != nil {
					fmt.Println("Error saving key:", err)
					return
			}
			fmt.Printf("New key generated and saved to %s\n", keyFilePath)
	} else if choice == "l" {
			keyFilePath := "my_encryption_key.key"
			key, err = loadKey(keyFilePath)
			if err != nil {
					if errors.Is(err, os.ErrNotExist) {
							fmt.Println("Key file not found. Generating a new key...")
							key, err = generateKey(32)
							if err != nil {
									fmt.Println("Error generating key:", err)
									return
							}
							if err := saveKey(key, keyFilePath); err != nil {
									fmt.Println("Error saving key:", err)
									return
							}
							fmt.Printf("New key generated and saved to %s\n", keyFilePath)
					} else {
							fmt.Println("Error loading key:", err)
							return
					}
			} else {
					fmt.Println("Key loaded successfully from", keyFilePath)
			}
	} else {
			fmt.Println("Invalid choice. Please enter 'g' or 'l'.")
			return
	}

	// User choice: Encrypt or decrypt
	fmt.Println("Do you want to encrypt (e) or decrypt (d) an image?")
	choice, err = reader.ReadString('\n')
	if err != nil {
			fmt.Println("Error reading input:", err)
			return
	}
	choice = strings.TrimSpace(choice)

	if choice == "e" {
			fmt.Print("Enter the path to the image file: ")
			imagePath, err := reader.ReadString('\n')
			if err != nil {
					fmt.Println("Error reading input:", err)
					return
			}
			imagePath = strings.TrimSpace(imagePath)

			encryptedImagePath, err := encryptImage(imagePath, key, "encrypted_images")
			if err != nil {
					fmt.Println("Error encrypting image:", err)
					return
			}
			fmt.Println("Image encrypted successfully! Encrypted image:", encryptedImagePath)
	} else if choice == "d" {
			fmt.Print("Enter the path to the encrypted image file: ")
			encryptedImagePath, err := reader.ReadString('\n')
			if err != nil {
					fmt.Println("Error reading input:", err)
					return
			}
			encryptedImagePath = strings.TrimSpace(encryptedImagePath)

			decryptedImagePath, err := decryptImage(encryptedImagePath, key)
			if err != nil {
					fmt.Println("Error decrypting image:", err)
					return
			}
			fmt.Println("Image decrypted successfully! Decrypted image:", decryptedImagePath)
	} else {
			fmt.Println("Invalid choice. Please enter 'e' or 'd'.")
	}
}