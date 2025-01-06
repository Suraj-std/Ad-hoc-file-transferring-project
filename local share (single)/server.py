import socket
import random
import threading
import os

# Generate a random connection code
connection_code = random.randint(1000, 9999)
print(f"Connection Code: {connection_code}")

# Folder to serve files from
SERVER_FOLDER = r"C:\Users\mvsur\Downloads\test12345"
if not os.path.exists(SERVER_FOLDER):
    os.makedirs(SERVER_FOLDER)

def get_server_ip():
    """Get the server's IP address."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"

def send_item(client_socket, item_path, relative_path):
    """Send a single file or folder."""
    if os.path.isfile(item_path):
        # Send file
        client_socket.send(b"FILE")
        client_socket.recv(1024)  # Wait for ACK
        client_socket.send(relative_path.encode())  # Send relative file path
        client_socket.recv(1024)  # Wait for ACK
        file_size = os.path.getsize(item_path)
        client_socket.send(str(file_size).encode())  # Send file size
        client_socket.recv(1024)  # Wait for ACK

        # Send the file in chunks
        with open(item_path, "rb") as f:
            while chunk := f.read(1024):
                client_socket.send(chunk)
        client_socket.recv(1024)  # Wait for final ACK
    elif os.path.isdir(item_path):
        # Send folder
        client_socket.send(b"DIR")
        client_socket.recv(1024)  # Wait for ACK
        client_socket.send(relative_path.encode())  # Send relative folder path
        client_socket.recv(1024)  # Wait for ACK
        # Recursively send the contents of the folder
        send_directory(client_socket, item_path, relative_path)

def send_directory(client_socket, folder_path, relative_path=""):
    """Send all files and folders from the folder_path."""
    items = os.listdir(folder_path)

    for item in items:
        item_path = os.path.join(folder_path, item)
        relative_item_path = os.path.join(relative_path, item)
        send_item(client_socket, item_path, relative_item_path)

def send_files(client_socket):
    """Send the contents of SERVER_FOLDER."""
    # Send the top-level folder name
    top_level_folder = os.path.basename(SERVER_FOLDER)
    client_socket.send(top_level_folder.encode())
    client_socket.recv(1024)  # Wait for ACK

    client_socket.send(b"START")  # Send start marker
    client_socket.recv(1024)  # Wait for ACK
    send_directory(client_socket, SERVER_FOLDER)
    client_socket.send(b"END")  # Send end marker
    client_socket.recv(1024)  # Wait for ACK
    print("All files and folders sent successfully.")

def handle_client(client_socket):
    try:
        client_socket.send(b"Enter the connection code: ")
        received_code = client_socket.recv(1024).decode().strip()
        if received_code == str(connection_code):
            client_socket.send(b"Authentication successful. Preparing files...")
            send_files(client_socket)
        else:
            client_socket.send(b"Authentication failed.")
    finally:
        client_socket.close()

def list_all_files_and_folders(folder_path, relative_path=""):
    """Recursively list all files and folders inside the given folder."""
    items = os.listdir(folder_path)
    for item in items:
        item_path = os.path.join(folder_path, item)
        relative_item_path = os.path.join(relative_path, item)
        
        if os.path.isfile(item_path):
            print(f"File: {relative_item_path}")
        elif os.path.isdir(item_path):
            print(f"Folder: {relative_item_path}")
            # Recursively list contents of the folder
            list_all_files_and_folders(item_path, relative_item_path)

def main():
    server_ip = get_server_ip()
    print(f"Server IP Address: {server_ip}")

    # Create a server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_ip, 9999))
    server_socket.listen(5)
    print("Server listening for connections...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    main()
