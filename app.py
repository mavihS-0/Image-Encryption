from modules.encryption import encrypt
from modules.decryption import decrypt
from modules.diffie_hellman import generate_private_key, compute_public_key, compute_shared_key
from modules.gen_p_q import generate_p_g

p,g = 23,5

private_key_A = generate_private_key(p)
public_key_A = compute_public_key(private_key_A,p,g)

private_key_B= generate_private_key(p)
public_key_B= compute_public_key(private_key_B,p,g)

shared_key_A = compute_shared_key(private_key_A,public_key_B,p)
shared_key_B = compute_shared_key(private_key_B,public_key_A,p)

print("Shared key computed by party A:", shared_key_A.hex()[:10])
print("Shared key computed by party B:", shared_key_B.hex()[:10])
hmac_tag = encrypt(shared_key_A.hex(),'kekw.png')
decrypt(shared_key_B.hex(),hmac_tag,'kekw.png')
