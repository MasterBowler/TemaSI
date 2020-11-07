#client
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.strxor import strxor
import socket

Kp = b'3252579393322456'
Iv = b'1166107792856443'

PORT_KM = 5050
PORT_B = 5051
FORMAT = 'utf-8'
SERVER = socket.gethostbyname(socket.gethostname())
ADDR_KM = (SERVER, PORT_KM)
ADDR_B = (SERVER, PORT_B)

#get K from the Key Manager node
def get_K():
    key_manager = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    key_manager.connect(ADDR_KM)
    K = key_manager.recv(16)
    key_manager.close()
    return K

#send a file to node B chunk by chunk
def send_file_to_b(K, opperation_mode):
    node_b = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    node_b.connect(ADDR_B)
    node_b.send(opperation_mode.encode(FORMAT)) #send the mode of opperation to node B
    node_b.send(K) #send K to node B

    node_b.recv(5).decode(FORMAT) #receive the transfer start signal

    decipher = AES.new(Kp, AES.MODE_ECB)
    K = decipher.decrypt(K) # decrypt K key

    cipher = AES.new(K, AES.MODE_ECB)
    file_to_send = open(input('Choose file: '),'r')
    ciphertext = Iv

    #read one 16 bytes chunk at a time
    while chunk := file_to_send.read(16):
        chunk = chunk.encode()
        if len(chunk) < 16: #add padding if necessary
            chunk = pad(chunk,16)

        if opperation_mode == "ECB":
            node_b.send(cipher.encrypt(chunk)) #ECB mode
        else:
            ciphertext = strxor(cipher.encrypt(ciphertext), chunk) #CFB mode
            node_b.send(ciphertext)

    node_b.close()

def main():
    print('Type ECB or CFB.')
    opperation_mode = input()
    if opperation_mode != 'ECB' and opperation_mode != 'CFB':
        print('Invalid mode of opperation.')
    else:
        K = get_K()
        send_file_to_b(K, opperation_mode)

if __name__ == '__main__':
    main()