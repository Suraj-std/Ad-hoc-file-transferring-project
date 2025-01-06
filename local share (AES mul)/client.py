import socket
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding


# Generate a random AES key (256-bit)
AES_KEY = os.urandom(32)  # 256-bit key
AES_IV = os.urandom(16)   # 128-bit IV

# Folder to save downloaded files+ 
DOWNLOAD_FOLDER = r"C:\Users\daoco\OneDrive\Documents\ad-hoc\storage"
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

def decrypt_data(encrypted_data):
    """Decrypt data using AES."""
    cipher = Cipher(algorithms.AES(AES_KEY), modes.CFB(AES_IV))
    decryptor = cipher.decryptor()
    return decryptor.update(encrypted_data) + decryptor.finalize()

def download_files(client_socket):
    """Download all files and folders sent by the server."""
    # Receive the top-level folder name
    top_level_folder = client_socket.recv(1024).decode()
    client_socket.send(b"ACK")  # Send ACK
    print(f"Top-Level Folder: {top_level_folder}")
    
    # Create the top-level folder locally
    top_level_path = os.path.join(DOWNLOAD_FOLDER, top_level_folder)
    os.makedirs(top_level_path, exist_ok=True)

    while True:
        marker = client_socket.recv(1024).decode()  # Receive marker (FILE, DIR, START, END)
        if marker == "START":
            client_socket.send(b"ACK")  # Send ACK
            print("Starting file transfer...")
        elif marker == "FILE":
            client_socket.send(b"ACK")  # Send ACK
            relative_path = client_socket.recv(1024).decode()  # Receive relative file path
            client_socket.send(b"ACK")  # Send ACK
            file_size = int(client_socket.recv(1024).decode())  # Receive file size
            client_socket.send(b"ACK")  # Send ACK

            # Create necessary directories
            file_path = os.path.join(top_level_path, relative_path)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            # Download the file in chunks and decrypt
            with open(file_path, "wb") as f:
                received_size = 0
                while received_size < file_size:
                    encrypted_chunk = client_socket.recv(1024)
                    decrypted_chunk = decrypt_data(encrypted_chunk)
                    f.write(decrypted_chunk)
                    received_size += len(decrypted_chunk)
            client_socket.send(b"ACK")  # Send final ACK
            print(f"Downloaded: {relative_path} ({file_size} bytes)")
        elif marker == "DIR":
            client_socket.send(b"ACK")  # Send ACK
            relative_path = client_socket.recv(1024).decode()  # Receive relative folder path
            client_socket.send(b"ACK")  # Send ACK

            # Create the directory
            folder_path = os.path.join(top_level_path, relative_path)
            os.makedirs(folder_path, exist_ok=True)
            print(f"Created folder: {relative_path}")
        elif marker == "END":
            client_socket.send(b"ACK")  # Send ACK
            print("File transfer complete.")
            break


def main():
    server_ip = input("Enter the server IP address: ")
    connection_code = input("Enter the connection code provided by the server: ")

    try:
        # Connect to the server
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_ip, 9999))
        
        # Receive prompt from server
        server_message = client_socket.recv(1024).decode()
        print(server_message)
        
        # Send the connection code
        client_socket.send(connection_code.encode())
        
        # Receive authentication result
        server_response = client_socket.recv(1024).decode()
        print(server_response)
        if "successful" in server_response:
            download_files(client_socket)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    main()
