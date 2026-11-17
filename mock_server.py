import socket
import sys
import threading
import time

HOST = "127.0.0.1"
PORT = 8080

def handle_client(client_socket, addr):
    print(f"[+] Active connection established from {addr}")
    try:
        client_socket.sendall(b"HTTP/1.1 200 OK\r\nContent-Length: 47\r\nConnection: close\r\n\r\nAuthorized Local Port Inspector Test Environment")
    except Exception as e:
        print(f"[-] Connection handling exception: {e}")
    finally:
        client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server.bind((HOST, PORT))
        server.listen(5)
        print(f"[*] Mock Service operational on http://{HOST}:{PORT}")
        print("[*] Press Ctrl+C to safely terminate this environment.")
        
        while True:
            client_sock, addr = server.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_sock, addr))
            client_thread.daemon = True
            client_thread.start()
    except KeyboardInterrupt:
        print("\n[*] Terminating mock service environment gracefully...")
    except Exception as e:
        print(f"[-] Operational failure: {e}")
    finally:
        server.close()

if __name__ == "__main__":
    start_server()
