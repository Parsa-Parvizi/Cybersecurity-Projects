const readline = require('readline');

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

// Caesar Cipher Functions
function caesarEncrypt(text, shift) {
    let result = '';
    for (let char of text) {
        if (char >= 'A' && char <= 'Z') {
            result += String.fromCharCode((char.charCodeAt(0) + shift - 65) % 26 + 65);
        } else if (char >= 'a' && char <= 'z') {
            result += String.fromCharCode((char.charCodeAt(0) + shift - 97) % 26 + 97);
        } else {
            result += char; // Non-alphabetic characters remain unchanged
        }
    }
    return result;
}

function caesarDecrypt(text, shift) {
    return caesarEncrypt(text, -shift);
}

// Vigenere Cipher Functions
function vigenereEncrypt(text, key) {
    let result = '';
    let keyIndex = 0;
    for (let char of text) {
        if (char >= 'A' && char <= 'Z') {
            result += String.fromCharCode((char.charCodeAt(0) + key.charCodeAt(keyIndex % key.length) - 2 * 65) % 26 + 65);
            keyIndex++;
        } else if (char >= 'a' && char <= 'z') {
            result += String.fromCharCode((char.charCodeAt(0) + key.charCodeAt(keyIndex % key.length) - 2 * 97) % 26 + 97);
            keyIndex++;
        } else {
            result += char; // Non-alphabetic characters remain unchanged
        }
    }
    return result;
}

function vigenereDecrypt(text, key) {
    let result = '';
    let keyIndex = 0;
    for (let char of text) {
        if (char >= 'A' && char <= 'Z') {
            result += String.fromCharCode((char.charCodeAt(0) - key.charCodeAt(keyIndex % key.length) + 26) % 26 + 65);
            keyIndex++;
        } else if (char >= 'a' && char <= 'z') {
            result += String.fromCharCode((char.charCodeAt(0) - key.charCodeAt(keyIndex % key.length) + 26) % 26 + 97);
            keyIndex++;
        } else {
            result += char; // Non-alphabetic characters remain unchanged
        }
    }
    return result;
}

// Railfence Cipher Functions
function railfenceEncrypt(text, rails) {
    if (rails <= 0) throw new Error("Number of rails must be greater than 0.");
    if (!text) return "";

    const rail = Array.from({ length: rails }, () => '');
    let direction = 1; // 1 means moving down, -1 means moving up
    let row = 0; // Start at the first rail

    for (let char of text) {
        rail[row] += char;

        if (row === 0) {
            direction = 1; // Move down
        } else if (row === rails - 1) {
            direction = -1; // Move up
        }

        row += direction;
    }

    return rail.join('');
}

function railfenceDecrypt(text, rails) {
    const n = text.length;
    const rail = Array.from({ length: rails }, () => Array(n).fill('\n'));
    let direction = null;
    let row = 0;
    let col = 0;

    for (let i = 0; i < n; i++) {
        if (row === 0) {
            direction = 1;
        }
        if (row === rails - 1) {
            direction = -1;
        }

        rail[row][col] = '*';
        col++;
        row += direction;
    }

    let index = 0;
    for (let i = 0; i < rails; i++) {
        for (let j = 0; j < n; j++) {
            if (rail[i][j] === '*' && index < n) {
                rail[i][j] = text[index];
                index++;
            }
        }
    }

    const result = [];
    row = 0;
    col = 0;
    for (let i = 0; i < n; i++) {
        if (row === 0) {
            direction = 1;
        }
        if (row === rails -  1) {
            direction = -1;
        }

        if (rail[row][col] !== '*') {
            result.push(rail[row][col]);
            col++;
        }

        row += direction;
    }

    return result.join('');
}

// Main Function
function main() {
    console.log("Welcome to the Text Encryption Tool!");
    rl.on('line', (input) => {
        const choice = input.trim();
        if (choice === '1') {
            rl.question("Enter the text to encrypt/decrypt: ", (text) => {
                rl.question("Do you want to (e)ncrypt or (d)ecrypt? ", (action) => {
                    rl.question("Enter the shift value: ", (shift) => {
                        const shiftValue = parseInt(shift);
                        if (action.toLowerCase() === 'e') {
                            const encryptedText = caesarEncrypt(text, shiftValue);
                            console.log(`Encrypted text: ${encryptedText}`);
                        } else if (action.toLowerCase() === 'd') {
                            const decryptedText = caesarDecrypt(text, shiftValue);
                            console.log(`Decrypted text: ${decryptedText}`);
                        } else {
                            console.log("Invalid action. Please choose 'e' or 'd'.");
                        }
                        rl.prompt();
                    });
                });
            });
        } else if (choice === '2') {
            rl.question("Enter the text to encrypt/decrypt: ", (text) => {
                rl.question("Do you want to (e)ncrypt or (d)ecrypt? ", (action) => {
                    rl.question("Enter the encryption key: ", (key) => {
                        if (action.toLowerCase() === 'e') {
                            const encryptedText = vigenereEncrypt(text, key);
                            console.log(`Encrypted text: ${encryptedText}`);
                        } else if (action.toLowerCase() === 'd') {
                            const decryptedText = vigenereDecrypt(text, key);
                            console.log(`Decrypted text: ${decryptedText}`);
                        } else {
                            console.log("Invalid action. Please choose 'e' or 'd'.");
                        }
                        rl.prompt();
                    });
                });
            });
        } else if (choice === '3') {
            rl.question("Enter the text to encrypt/decrypt: ", (text) => {
                rl.question("Do you want to (e)ncrypt or (d)ecrypt? ", (action) => {
                    rl.question("Enter the number of rails: ", (rails) => {
                        const railsValue = parseInt(rails);
                        if (action.toLowerCase() === 'e') {
                            const encryptedText = railfenceEncrypt(text, railsValue);
                            console.log(`Encrypted text: ${encryptedText}`);
                        } else if (action.toLowerCase() === 'd') {
                            const decryptedText = railfenceDecrypt(text, railsValue);
                            console.log(`Decrypted text: ${decryptedText}`);
                        } else {
                            console.log("Invalid action. Please choose 'e' or 'd'.");
                        }
                        rl.prompt();
                    });
                });
            });
        } else if (choice === '4') {
            console.log("Exiting...");
            rl.close();
        } else {
            console.log("Invalid choice. Please select a valid option.");
            rl.prompt();
        }
    });

    rl.setPrompt("Choose an option:\n1. Caesar Cipher\n2. Vigenere Cipher\n3. Railfence Cipher\n4. Exit\nEnter your choice (1-4): ");
    rl.prompt();
}

main();
