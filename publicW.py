import binascii
import hashlib
import base58

def generate_address(public_key):
    # Step 1: Hash the public key using SHA-256
    sha256_hash = hashlib.sha256(binascii.unhexlify(public_key)).digest()

    # Step 2: Hash the result of SHA-256 using RIPEMD-160
    ripemd160_hash = hashlib.new('ripemd160', sha256_hash).digest()

    # Rest of the code remains the same
    return base58.b58encode_check(b'\x00' + ripemd160_hash).decode()  # Encoding to Base58 address

# Read the input file containing public keys
file_path = 'public-keys.txt'

with open(file_path, 'r') as file:
    public_keys = file.readlines()

# Remove any leading/trailing whitespaces and newlines
public_keys = [key.strip() for key in public_keys]

# Generate addresses for each public key
addresses = []
for public_key in public_keys:
    if len(public_key) % 2 != 0:  # Skip lines with odd lengths
        continue

    compressed_address = generate_address(public_key)
    uncompressed_address = generate_address(public_key + '01')

    addresses.append((public_key, compressed_address, uncompressed_address))

# Write the results to output files
addresses_file = 'addresses.txt'
output_file = 'output.txt'

with open(addresses_file, 'w') as file:
    for _, compressed_address, uncompressed_address in addresses:
        file.write(f'{compressed_address}\n{uncompressed_address}\n')

with open(output_file, 'w') as file:
    for public_key, compressed_address, uncompressed_address in addresses:
        file.write(f'Public Key: {public_key}\nCompressed Address: {compressed_address}\nUncompressed Address: {uncompressed_address}\n\n')

print(f'Addresses saved to {addresses_file} and output saved to {output_file}.')
