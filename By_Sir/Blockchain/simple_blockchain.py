import hashlib
import datetime

# Define a block structure
class Block:
    def __init__(self, index, previous_hash, data):
        self.index = index
        self.timestamp = str(datetime.datetime.now())
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        # Hash combines index, timestamp, data, and previous hash
        block_string = str(self.index) + self.timestamp + self.data + self.previous_hash
        return hashlib.sha256(block_string.encode()).hexdigest()

# Create the first block - Genesis Block
genesis_block = Block(0, "0", "Genesis Block")
print("Genesis Block Hash:", genesis_block.hash)

# Create the next block
block1 = Block(1, genesis_block.hash, "Ali sends 2 BTC to Majid")
print("Block 1 Hash:", block1.hash)

# Create another block
block2 = Block(2, block1.hash, "Sajid sends 1 BTC to Fahad")
print("Block 2 Hash:", block2.hash)