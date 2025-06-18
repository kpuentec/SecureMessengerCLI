import socket
import threading


HOST = "192.168.1.162"
PORT = 9999


def verify():
    print("To begin, make sure HOST and PORT is properly configured in main.py")
    choice = input("Enter 1 to continue: ").strip()

    if choice == "1":
        client = chat()
        threading.Thread(target=send, args=(client,)).start()
        threading.Thread(target=receive, args=(client,)).start()

        while True:
            pass
    else:
        print("Invalid Input. Exitting program.\n")
        exit()

def chat():
    print("1. Host (start a server) ")
    print("2. Client (connect to a host) ")
    choice = input("Enter your choice: ").strip()

    if choice == "1":
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((HOST, PORT))
        server.listen()
        client, _ = server.accept()
        return client
    elif choice == "2":
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST, PORT)) 
        return client
    else:
        print("Invalid Input. Exitting program.")
        exit()

def send(c):
    while True:
        message = input("")
        c.send(message.encode())
        print("You: " + message)

def receive(c):
    while True:
        print("Friend: " + c.recv(1024).decode())

def main():

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


if __name__ == "__main__":
    main()

# python3 main.py