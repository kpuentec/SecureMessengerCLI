import os
import socket
import threading
import secrets
from hashlib import sha256
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from colorama import Fore, Style, init

HOST = "127.0.0.1"
PORT = 9999

def verify():
    print("\nTo begin, make sure HOST and PORT is properly configured in main.py")
    print("To exit the chat simpliy type in /quit.")
    choice = input("Enter 1 to continue: ").strip()

    if choice == "1":
        client, key, name, their_name, color, their_color = chat()
        threading.Thread(target=send, args=(client, key, name, color)).start()
        threading.Thread(target=receive, args=(client, key, their_name, their_color)).start()

        while True:
            pass

    else:
        print("Invalid Input. Exitting program.\n")
        main()

def chat():
    print("1. Host (start a server) ")
    print("2. Client (connect to a host) ")
    choice = input("Enter your choice: ").strip()
    username = input("Enter your username: ").strip()

    g = 14
    p = 292192301
    private_key = secrets.randbelow(p)
    public_key = pow(g, private_key, p)

    if choice == "1":
        color = Fore.GREEN
        their_color = Fore.BLUE
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((HOST, PORT))
        server.listen()
        client, _ = server.accept()
        # public key send
        client.sendall(str(public_key).encode())

        # recieve other public key
        client.sendall(username.encode())
        their_public = int(client.recv(1024).decode())
        their_name = client.recv(1024).decode()

    elif choice == "2":
        color = Fore.BLUE
        their_color = Fore.GREEN
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST, PORT)) 
        their_public = int(client.recv(1024).decode())
        their_name = client.recv(1024).decode()

        client.sendall(str(public_key).encode())
        client.sendall(username.encode())
    else:
        print("Invalid Input. Exitting program.")
        main()

    shared_secret = pow(their_public, private_key, p)
    key = sha256(str(shared_secret).encode()).digest()
    print(f"{Fore.YELLOW}Connection established! You can start chatting now.{Style.RESET_ALL}")
    return client, key, username, their_name, color, their_color

def send(c, k, name, color):
    while True:
        message = input("")
        # message = input(color + name + Style.RESET_ALL + " -- ")
        if message.lower() == "/quit":
            c.send(encrypt("__quit__", k))
            print("You ended the chat.")
            c.close()
            break
        encrypted = encrypt(message, k)
        c.send(encrypted)
        print('\033[F\033[K', end='')
        print()
        print(color + name + Style.RESET_ALL + " -- " + message)

def receive(c, k, their_name, their_color):
    while True:
        data = c.recv(2048)
        if data:
            decrypted = decrypt(data, k)
            if decrypted == "__quit__":
                print(f"\n Chat has been ended.")
                c.close()
                break
            print()
            print(their_color + their_name + Style.RESET_ALL + " -- " + decrypted)

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
    print("2. Quit")
    choice = input("Choose an option: ").strip()

    if choice == "1":
        verify()
    elif choice == "2":
        exit()
    else:
        print("Invalid choice. Try again.\n")
        main()


if __name__ == "__main__":
    init(autoreset=True)
    main()
