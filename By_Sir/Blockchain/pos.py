import random

class ProofOfStake:
    def __init__(self):
        self.validators = {}
        self.total_stake = 0

    def add_validator(self, name, stake):
        """Add a validator with their stake"""
        self.validators[name] = stake
        self.total_stake += stake
        print(f"✓ {name} joined with stake: {stake} coins")

    def select_validator(self):
        """Select validator based on stake (weighted random)"""
        # Create a list where each validator appears proportional to stake
        selection_pool = []
        for validator, stake in self.validators.items():
            # Add validator multiple times based on stake
            selection_pool.extend([validator] * stake)

        # Randomly select from pool
        selected = random.choice(selection_pool)
        return selected

    def simulate_block_creation(self, num_blocks=10):
        """Simulate multiple block creations"""
        print(f"\n--- Simulating {num_blocks} block creations ---")
        selection_count = {v: 0 for v in self.validators}

        for i in range(num_blocks):
            validator = self.select_validator()
            selection_count[validator] += 1
            print(f"Block {i+1}: Selected {validator}")

        print("\n--- Selection Statistics ---")
        for validator, count in selection_count.items():
            percentage = (count / num_blocks) * 100
            stake_percentage = (self.validators[validator] / self.total_stake) * 100
            print(f"{validator}: {count} blocks ({percentage:.1f}%) | Stake: {stake_percentage:.1f}%")

# Example simulation
pos = ProofOfStake()
pos.add_validator("Alice", 100)
pos.add_validator("Bob", 200)
pos.add_validator("Carol", 50)
pos.add_validator("Dave", 150)

pos.simulate_block_creation(100)