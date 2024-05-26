def add_number_to_hex(hex_string, x):
    # Convert hex string to bytes
    bytes_data = bytes.fromhex(hex_string)
    print(bytes_data)
    
    # Initialize an empty byte array to store the modified bytes
    modified_bytes = bytearray()

    # Iterate through each byte in the bytes data
    for byte in bytes_data:
        # Add x to the byte and take modulo 16
        new_byte = (byte + x) % 256
        # Append the modified byte to the bytearray
        modified_bytes.append(new_byte)
    print(modified_bytes)

    # Convert the modified bytes back to hex string
    new_hex_string = modified_bytes.hex()

    return new_hex_string

# Example usage:
hex_string = "6fc9d567024243cc0df5c578575627ff"  # 32-character long hex string
x = 1
new_hex_string = add_number_to_hex(hex_string, x)
print("New Hex String:", new_hex_string)
