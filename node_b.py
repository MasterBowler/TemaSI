#server
from Crypto.Cipher import AES
from Crypto.Util.strxor import strxor
import socket

Kp = b'3252579393322456'
Iv = b'1166107792856443'

PORT = 5051
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

#receive the file one chunk at a time from node A
def handle_node_a(conn):
    opperation_mode = conn.recv(3).decode(FORMAT)
    K = conn.recv(16) #receive the mode of operation
    decipher = AES.new(Kp, AES.MODE_ECB)
    K = decipher.decrypt(K) #decrypt K key
    conn.send('start'.encode(FORMAT)) #notify node A that the transfer can start

    cipher = AES.new(K, AES.MODE_ECB)
    ciphertext = Iv
    #receive one 16 bytes chunk at a time
    while chunk := conn.recv(16):
        print(chunk)
        if opperation_mode == 'ECB':
            chunk = cipher.decrypt(chunk) #ECB mode
            plaintext = chunk
        else:
            plaintext = strxor(cipher.encrypt(ciphertext), chunk) #CFB mode
            ciphertext = chunk
        print(plaintext.decode(FORMAT).rstrip(), end='')
    print()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    conn, addr = server.accept()
    handle_node_a(conn)

if __name__ == '__main__':
    main()