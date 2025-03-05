from flask import Flask, request, render_template
import random

app = Flask(__name__)

# Function to find gcd
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

# Function to find modular inverse
def mod_inverse(e, phi):
    for d in range(2, phi):
        if (d * e) % phi == 1:
            return d
    return None

# RSA Key Generation
def generate_keys():
    p = 61  # Prime number 1
    q = 53  # Prime number 2
    n = p * q
    phi = (p - 1) * (q - 1)

    e = random.choice([3, 5, 17, 257, 65537])  # Public exponent
    while gcd(e, phi) != 1:
        e = random.choice([3, 5, 17, 257, 65537])

    d = mod_inverse(e, phi)

    return (e, n), (d, n)

public_key, private_key = generate_keys()

# RSA Encryption
def encrypt(text, key):
    e, n = key
    return [pow(ord(char), e, n) for char in text]

# RSA Decryption
def decrypt(cipher, key):
    d, n = key
    return ''.join([chr(pow(char, d, n)) for char in cipher])

@app.route("/", methods=["GET", "POST"])
def index():
    encrypted_text = decrypted_text = ""
    
    if request.method == "POST":
        message = request.form["message"]
        if "encrypt" in request.form:
            encrypted_text = encrypt(message, public_key)
        elif "decrypt" in request.form:
            encrypted_text = request.form["encrypted_text"]
            decrypted_text = decrypt(eval(encrypted_text), private_key)

    return render_template("index.html", encrypted_text=encrypted_text, decrypted_text=decrypted_text)

if __name__ == "__main__":
    app.run(debug=True)
