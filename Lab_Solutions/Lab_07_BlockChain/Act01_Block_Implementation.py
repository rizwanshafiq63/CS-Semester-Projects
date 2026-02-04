
import hashlib  # Importing the hashlib library to use the SHA 256 hashing function 
import time     # Importing the time module to get the current timestamp for each block 

# ------------------------------------------------
#  Lab Activity 1: Block Structure Implementation
# ------------------------------------------------

# Block class definition 
class Block: 
    def __init__(self, index, data, previous_hash): 
        """ 
        Constructor to initialize a block in the blockchain. 
        Parameters: 
        - index: The position of the block in the blockchain (starting with 0 for the genesis block). 
        - data: The transaction data or information to be stored in the block. 
        - previous_hash: The hash of the previous block in the chain, ensuring continuity and security. 
        """ 
        self.index = index                    # Index or position of the block in the chain 
        self.timestamp = time.time()          # Timestamp of block creation 
        self.data = data                      # Data stored in the block (e.g., transactions) 
        self.previous_hash = previous_hash    # Hash of the previous block, linking to it 
        self.hash = self.compute_hash()       # Hash of the current block, generated using compute_hash method 

    def compute_hash(self): 
        """ 
        Method to calculate the SHA-256 hash of the block's contents. 
        The hash is generated using the block's index, timestamp, data, and the previous block's hash. 
        """ 
        # Combine the block's properties into a single string 
        block_string = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}" 
        # Compute and return the SHA-256 hash of the block string 
        return hashlib.sha256(block_string.encode()).hexdigest() 

# Creating the genesis block (the first block in the blockchain) 
genesis_block = Block(0, "Genesis Block", "0") 
# Output the hash of the genesis block 
print(f"Genesis Block Hash: {genesis_block.hash}")


# ------------------------------------------
#  Lab Activity 2: Blockchain Construction 
# ------------------------------------------

# Blockchain class definition 
class Blockchain: 
    def __init__(self): 
        """ 
        Constructor to initialize the blockchain. 
        It starts with a list containing only the genesis block. 
        """ 
        # The blockchain starts with the genesis block 
        self.chain = [self.create_genesis_block()] 

    def create_genesis_block(self): 
        """ 
        Creates the first block in the blockchain (the genesis block). 
        The genesis block has an index of 0, default data "Genesis Block",  
        and a previous hash of "0" since it's the first block. 
        """ 
        return Block(0, "Genesis Block", "0") 

    def add_block(self, data): 
        """ 
        Adds a new block to the blockchain. 
        Parameters: 
        - data: The data to be stored in the new block. 
        The new block links to the previous block by including its hash. 
        """ 
        # Get the last block in the current chain (previous block) 
        last_block = self.chain[-1] 
        # Create a new block with the next index, the provided data, and the hash of the last block 
        new_block = Block(len(self.chain), data, last_block.hash) 
        # Append the new block to the blockchain 
        self.chain.append(new_block) 

    def print_blockchain(self): 
        """ 
        Prints out each block in the blockchain. 
        Displays the block's index, data, hash, and the hash of the previous block. 
        """ 
        # Iterate over all blocks in the chain and print their details 
        for block in self.chain: 
            print(f"Index: {block.index}, Data: {block.data}, Hash: {block.hash}, Previous Hash: {block.previous_hash}") 

# Example usage of the Blockchain class 
blockchain = Blockchain()               # Create a new blockchain with a genesis block 
blockchain.add_block("Block 1 Data")     # Add a block with data "Block 1 Data" 
blockchain.add_block("Block 2 Data")     # Add a block with data "Block 2 Data" 
blockchain.print_blockchain()            # Print the details of the blockchain 

