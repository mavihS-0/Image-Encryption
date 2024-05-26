import socket
from diffie_hellman import generate_private_key, compute_public_key, compute_shared_key
from decryption import decrypt

def server():
    # Establish connection
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 12345)
    server_socket.bind(server_address)
    server_socket.listen(1)

    print("Waiting for connection...")
    connection, client_address = server_socket.accept()

    # Receive p, q, and client's public key
    p = int.from_bytes(connection.recv(32), 'big')
    print('Received p')
    q = int.from_bytes(connection.recv(32), 'big')
    print('Received q')
    client_public_key = int.from_bytes(connection.recv(32), 'big')
    print('Received client\'s public key')

    # Generate private key for Diffie-Hellman
    private_key = generate_private_key(p)
    print('Private key: ', private_key)

    # Compute public key
    public_key = compute_public_key(private_key, p, q)
    print('Public key: ', public_key)

    # Send server's public key to client
    connection.sendall(public_key.to_bytes(32, 'big'))
    print('Sent server\'s public key')

    # Receive HMAC tag from client
    hmac_tag = connection.recv(64).decode()
    print('Received HMAC tag')

    # Receive image name from client
    image_name = connection.recv(1024).decode()
    print('Received image name '+str(image_name))


    # Compute shared key
    shared_key = compute_shared_key(private_key,client_public_key, p)
    print('Shared Key: '+shared_key.hex())

    # Decrypt image
    decrypt(shared_key.hex(),hmac_tag,str(image_name))
    print('Decrypted image')  

    # Close connection
    connection.close()

server()
