from modules.hmac_verify import calculate_hmac

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

def encrypt(shared_key,image_name):

    key_hex = shared_key[:32]  # First 128 bits
    hmac_key = shared_key[32:] # Last 128 bits

    # Convert image to hex string
    image_path = str(image_name)
    image_hex = image_to_hex(image_path)


    # Generate mask using a 128-bit hexadecimal key
    mask_hex = generate_mask(key_hex, len(image_hex))

    # XOR the image hex string with the mask
    encrypted_hex = xor_hex_strings(image_hex, mask_hex)

    # Calculate HMAC tag
    hmac_tag = calculate_hmac(hmac_key, encrypted_hex)

    # Convert encrypted hex string back to image
    output_image_path = 'images/encrypted_'+image_name
    hex_to_image(encrypted_hex, output_image_path)
    return hmac_tag
