import hashlib
import datetime

# ---------------------------
# BLOCK CLASS
# ---------------------------
class Block:
    def __init__(self, index, timestamp, data, previous_hash, difficulty=3):
        self.index = index                # Block number
        self.timestamp = timestamp        # Time of creation
        self.data = data                  # Transaction or record data
        self.previous_hash = previous_hash  # Hash of previous block
        self.nonce = 0                    # Value changed to find valid hash
        self.hash = self.mine_block(difficulty)  # Start mining on creation

    # Function to calculate the hash of the block
    def calculate_hash(self):
        block_string = (
            str(self.index)
            + str(self.timestamp)
            + str(self.data)
            + str(self.previous_hash)
            + str(self.nonce)
        )
        return hashlib.sha256(block_string.encode()).hexdigest()

    # Mining process (Proof of Work)
    def mine_block(self, difficulty):
        prefix = "0" * difficulty  # Hash must start with N zeros
        while True:
            new_hash = self.calculate_hash()
            if new_hash.startswith(prefix):
                print(f"Block {self.index} mined with hash: {new_hash}")
                return new_hash
            else:
                self.nonce += 1  # Keep changing nonce until the correct hash is found


# ---------------------------
# BLOCKCHAIN CLASS
# ---------------------------
class Blockchain:
    def __init__(self, difficulty=3):
        self.chain = [self.create_genesis_block()]  # Start with Genesis block
        self.difficulty = difficulty

    # Create the very first block (Genesis block)
    @staticmethod
    def create_genesis_block():
        print("Creating Genesis Block...")
        return Block(0, str(datetime.datetime.now()), "Genesis Block", "0", difficulty=3)

    # Get the most recent block in the chain
    def get_latest_block(self):
        return self.chain[-1]

    # Add new block to the chain
    def add_block(self, data):
        print(f"\nAdding new block with data: {data}")
        latest_block = self.get_latest_block()
        new_block = Block(
            len(self.chain),
            str(datetime.datetime.now()),
            data,
            latest_block.hash,
            self.difficulty,
        )
        self.chain.append(new_block)

    # Validate the integrity of the blockchain
    def is_chain_valid(self):
        print("\nChecking Blockchain Integrity...")
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            # Check if the current block hash is still valid
            if current.hash != current.calculate_hash():
                print(f"Block {i} hash mismatch! Blockchain compromised.")
                return False

            # Check if the previous hash is correct
            if current.previous_hash != previous.hash:
                print(f"Block {i} previous hash mismatch! Blockchain broken.")
                return False

        print("Blockchain is valid and secure.")
        return True

    # Display the full blockchain
    def display_chain(self):
        print("\nBlockchain Contents:")
        for block in self.chain:
            print(f"Block {block.index}")
            print(f"Timestamp     : {block.timestamp}")
            print(f"Data          : {block.data}")
            print(f"Nonce         : {block.nonce}")
            print(f"Previous Hash : {block.previous_hash}")
            print(f"Hash          : {block.hash}\n")


# ---------------------------
# MAIN PROGRAM EXECUTION
# ---------------------------
if __name__ == "__main__":
    print("Starting Blockchain Simulation\n")

    # Initialize blockchain with difficulty level
    my_chain = Blockchain(difficulty=3)

    # Add sample transactions
    my_chain.add_block("Alice sends 2 BTC to Bob")
    my_chain.add_block("Bob sends 1 BTC to Charlie")
    my_chain.add_block("Charlie sends 0.5 BTC to David")

    # Display the entire blockchain
    my_chain.display_chain()

    # Validate blockchain
    my_chain.is_chain_valid()

    # Tampering example
    print("\n⚠️  Tampering with block data...")
    my_chain.chain[1].data = "Alice sends 200 BTC to Bob (Tampered)"
    my_chain.is_chain_valid()