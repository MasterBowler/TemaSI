#server
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import socket

K = get_random_bytes(16)
Kp = b'3252579393322456'

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

#send K to node A
def handle_node_a(conn):
    cipher = AES.new(Kp, AES.MODE_ECB)
    conn.send(cipher.encrypt(K))
    conn.close()


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    conn, addr = server.accept()
    handle_node_a(conn)

if __name__ == '__main__':
    main()