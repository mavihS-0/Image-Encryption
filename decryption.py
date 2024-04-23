from hmac_verify import calculate_hmac, verify_hmac
from queue import LifoQueue

def image_to_hex(image_path):
    with open(image_path, 'rb') as f:
        image_bytes = f.read()
        image_hex = image_bytes.hex()
    return image_hex

def hex_to_image(hex_string, output_path):
    image_bytes = bytes.fromhex(hex_string)
    with open(output_path, 'wb') as f:
        f.write(image_bytes)

def generate_mask(key_hex, length):
    key_bytes = bytes.fromhex(key_hex)
    mask = bytearray()
    key_length = len(key_bytes)
    for i in range(length):
        mask.append(key_bytes[i % key_length])
    # Truncate the mask to the desired length
    mask = mask.hex()[:length]
    return mask

def add_number_to_hex(hex_string, x):
    # Convert hex string to bytes
    bytes_data = bytes.fromhex(hex_string)
    
    # Initialize an empty byte array to store the modified bytes
    modified_bytes = bytearray()

    # Iterate through each byte in the bytes data
    for byte in bytes_data:
        # Add x to the byte and take modulo 16
        new_byte = (byte + x) % 256
        # Append the modified byte to the bytearray
        modified_bytes.append(new_byte)

    # Convert the modified bytes back to hex string
    new_hex_string = modified_bytes.hex()

    return new_hex_string

def hex_to_binary(hex_string):
    # Convert hexadecimal string to bytes
    byte_data = bytes.fromhex(hex_string)
    # Convert bytes to binary string
    binary_string = bin(int.from_bytes(byte_data, 'big'))[2:].zfill(len(hex_string) * 4)
    return binary_string

def binary_to_hex(binary_string):
    # Convert binary string to integer
    integer_value = int(binary_string, 2)
    # Convert integer to hexadecimal string
    hex_string = hex(integer_value)[2:].zfill(len(binary_string) // 4)
    return hex_string

def xor_hex_strings(hex_str1, hex_str2):
    # Convert hexadecimal strings to binary strings
    bin_str1 = hex_to_binary(hex_str1)
    bin_str2 = hex_to_binary(hex_str2)
    # Perform XOR operation
    xor_result = int(bin_str1, 2) ^ int(bin_str2, 2)

    # Convert result back to binary string and then to hexadecimal string
    xor_hex = binary_to_hex(bin(xor_result)[2:].zfill(len(bin_str1)))

    return xor_hex


def create_stack(key_hex):

    # Stack to store keys for 16 rounds
    stack = LifoQueue(maxsize=16)

    for i in range(0,32,2):
        # Convert the hexadecimal byte to an integer
        key_generator = int(key_hex[i:i+2], 16)

        # Add the integer to the key
        key_hex = add_number_to_hex(key_hex,key_generator)
        stack.put(key_hex)

    return stack

def decrypt(shared_key,hmac_tag,image_name):

    image_name = str(image_name)
    key_hex = shared_key[:32]  # First 128 bits
    hmac_key = shared_key[32:] # Last 128 bits

    # Convert image to hex string
    image_path = 'encrypted_'+image_name
    image_hex = image_to_hex(image_path)

    if not verify_hmac(image_hex, hmac_key, hmac_tag):
        print("HMAC verification failed. Image integrity compromised.")
        return
    else:
        print("HMAC verification successful. Image integrity maintained.")

    stack = create_stack(key_hex)

    decrypted_hex = image_hex

    # Decrypt the image using the keys from the stack
    while not stack.empty():
        key_hex = stack.get()

        # Generate mask using the same key as encryption
        mask_hex = generate_mask(key_hex, len(image_hex))  

        # Decrypt the image
        decrypted_hex = xor_hex_strings(decrypted_hex, mask_hex)

    # Convert decrypted hex string back to image
    output_image_path = 'decrypted_'+image_name
    hex_to_image(decrypted_hex, output_image_path)

