import socket
from modules.diffie_hellman import generate_private_key, compute_public_key, compute_shared_key
from modules.gen_p_q import generate_p_g
from modules.encryption import encrypt

def client():
    # Establish connection
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 12345)
    client_socket.connect(server_address)

    # Input p and q from user
    bits = int(input("No of bits to generate prime and generator: "))
    p,q = generate_p_g(bits)
    print('Prime number (p): ', p)
    print('Generator (q): ', q)
    
    # Generate private key for Diffie-Hellman
    private_key = generate_private_key(p)
    print('Private key: ', private_key)
    
    # Compute public key
    public_key = compute_public_key(p, q, private_key)
    print('Public key: ', public_key)

    # Send p, q, and public key to server
    client_socket.sendall(p.to_bytes(32, 'big'))
    print('Sent p')
    client_socket.sendall(q.to_bytes(32, 'big'))
    print('Sent q')
    client_socket.sendall(public_key.to_bytes(32, 'big'))
    print('Sent public key')

    # Receive server's public key
    server_public_key = int.from_bytes(client_socket.recv(32), 'big')
    print('Received server\'s public key')

    # Input image name from user
    image_name = input("Enter the image name: ")

    # Compute shared key
    shared_key = compute_shared_key(private_key,server_public_key, p)

    # Encrypt image
    hmac_tag = encrypt(shared_key.hex(),str(image_name))
    print('Encrypted image')

    # Send HMAC tag to server
    client_socket.sendall(hmac_tag.encode())
    print('Sent HMAC tag')

    # Send image name to server
    client_socket.sendall(image_name.encode())
    print('Sent image name')

    # Close connection
    client_socket.close()

client()
