from encryption import encrypt
from decryption import decrypt
from diffie_hellman import generate_private_key, compute_public_key, compute_shared_key
from gen_p_q import generate_p_g



p,g = generate_p_g(128)

private_key_A = generate_private_key(p)
public_key_A = compute_public_key(private_key_A,p,g)

private_key_B= generate_private_key(p)
public_key_B= compute_public_key(private_key_B,p,g)

shared_key_A = compute_shared_key(private_key_A,public_key_B,p)
shared_key_B = compute_shared_key(private_key_B,public_key_A,p)



print("Shared key computed by party A:", shared_key_A.hex())
print("Shared key computed by party B:", shared_key_B.hex())
hmac_tag = encrypt(shared_key_A.hex(),'test32.jpg')
decrypt(shared_key_B.hex(),hmac_tag,'test32.jpg')
