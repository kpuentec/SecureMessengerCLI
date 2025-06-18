import os
import socket
import threading
import secrets
from hashlib import sha256
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

HOST = "192.168.1.162"
PORT = 9999
USERNAME = "User"
OTHER_USER = "Friend"


def verify():
    print("To begin, make sure HOST and PORT is properly configured in main.py")
    choice = input("Enter 1 to continue: ").strip()

    if choice == "1":
        client, key = chat()
        threading.Thread(target=send, args=(client, key)).start()
        threading.Thread(target=receive, args=(client, key)).start()

        while True:
            pass
    else:
        print("Invalid Input. Exitting program.\n")
        main()

def chat():
    print("1. Host (start a server) ")
    print("2. Client (connect to a host) ")
    choice = input("Enter your choice: ").strip()

    g = 14
    p = 292192301
    private_key = secrets.randbelow(p)
    public_key = pow(g, private_key, p)

    if choice == "1":
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((HOST, PORT))
        server.listen()
        client, _ = server.accept()
        # public key send
        client.sendall(str(public_key).encode())

        # recieve other public key
        their_public = int(client.recv(2048).decode())

    elif choice == "2":
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST, PORT)) 
        their_public = int(client.recv(2048).decode())
        client.sendall(str(public_key).encode())
    else:
        print("Invalid Input. Exitting program.")
        main()

    shared_secret = pow(their_public, private_key, p)
    key = sha256(str(shared_secret).encode()).digest()

    return client, key

def send(c, k):
    while True:
        message = input("")
        encrypted = encrypt(message, k)
        c.send(encrypted)
        print(f"{USERNAME}: " + message)

def receive(c, k):
    while True:
        data = c.recv(2048)
        decrypted = decrypt(data, k)
        print(f"{OTHER_USER}: " + decrypted)

def encrypt(message, key):
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, message.encode(), None)
    return nonce + ciphertext

def decrypt(data, key):
    aesgcm = AESGCM(key)
    nonce = data[:12]
    ciphertext = data[12:]
    plaintext = aesgcm.decrypt(nonce, ciphertext, None)
    return plaintext.decode()



def main():
        print("\n")
        print("*===== Secure Messenger CLI =====*\n")
        print("Securely exchange messages\n")

        print("1. Begin Connection")
        print("2. Modify Usernames")
        print("3. Quit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            verify()
        elif choice == "2":
            print("1. Modify Username")
            print("2. Modify Friend Username")
            print("3. Main Menu")
            choice = input("Choose an option: ").strip()

            if choice == "1":
                USERNAME = input("Choose an option: ").strip()
                print("Username Changed.")
                main()
            elif choice == "2":
                OTHER_USER = input("Choose an option: ").strip()
                print("Username Changed.")
                main()
            elif choice == "3":
                main()
            else:
                print("Invalid choice. Try again.\n")
                main()
        elif choice == "3":
            exit()
        else:
            print("Invalid choice. Try again.\n")


if __name__ == "__main__":
    main()

# python3 main.py