# Secure File Transfer System

## 🚀 Overview
The **Secure File Transfer System** is a Python-based application for transferring any type of files of any size securely over a local network. Using robust encryption (AES), the project ensures safe and efficient file transfer between a server and multiple clients.

## 📜 Features
- **End-to-End Encryption**: AES encryption with 256-bit keys for secure file transfer.
- **Authentication**: Unique connection code for client authentication.
- **Multi-File Support**: Handles file transfers of any size, including directories.
- **Cross-Platform Compatibility**: Works on any system with Python installed.
- **Multi-Threaded Server**: Handles multiple client connections simultaneously.

## 🛠️ Technologies Used
- **Python**: Main programming language.
- **Socket Library**: Allows TCP/IP communication between server and clients.
- **Threading**: Enables multi-threaded server for concurrent client handling.
- **Cryptography Library**: Provides AES encryption and decryption for secure data transfer.

## 🏗️ Project Structure
```plaintext
├── client.py    # Client-side script for connecting to the server and downloading files
├── server.py    # Server-side script for sharing files with authenticated clients
```

## ⚙️ How It Works
1. **Server**:
   - Starts a multi-threaded socket server and generates a unique connection code.
   - Serves files from a specified directory.
   - Encrypts file data using AES before transmission.

2. **Client**:
   - Connects to the server using the provided IP address and connection code.
   - Authenticates with the server.
   - Receives and decrypts files, saving them locally.

## 📂 Setup Instructions

### Prerequisites
- Python 3.11
- Required libraries (install via `requirements.txt`):
  ```plaintext
  pip install cryptography
  ```

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/secure-file-transfer.git
   cd secure-file-transfer
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure directories for server and client:
   - Update `SERVER_FOLDER` in `server.py` to specify the folder for files to be shared.
   - Update `DOWNLOAD_FOLDER` in `client.py` to set the folder for downloaded files.

### Running the Application
#### 1. Start the Server
   ```bash
   python server.py
   ```
   - Note the displayed connection code and server IP.

#### 2. Start the Client
   ```bash
   python client.py
   ```
   - Enter the server IP and connection code when prompted.

## 🔒 Security Highlights
- **AES Encryption**: All file data is encrypted using AES before transmission.
- **Authentication**: Only clients with the correct connection code can access the server.

## 🤝 Contributing
Contributions are welcome! Follow these steps to get started:
1. Fork this repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add new feature"
   ```
4. Push to the branch:
   ```bash
   git push origin feature-name
   ```
5. Submit a pull request.

## 📜 License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 📧 Contact
- Email: [your.email@example.com](mailto:your.email@example.com)
- GitHub: [yourusername](https://github.com/yourusername)
