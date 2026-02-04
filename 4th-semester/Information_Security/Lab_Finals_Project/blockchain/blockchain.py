import json
import time
from dataclasses import dataclass, asdict
from typing import Dict, Any, List

from crypto.crypto_utils import hash_sha256


DIFFICULTY = 3

@dataclass
class Block:
    index: int
    timestamp: float
    previous_hash: str
    data: Dict[str, Any]
    nonce: int
    hash: str

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2)


class Blockchain:
    def __init__(self):
        self.chain: List[Block] = []
        self._create_genesis()


    def _create_genesis(self):
        data = {"type": "genesis", "message": "Secure Complaint System Blockchain"}
        genesis_block = self._mine_block(
            index=0,
            prev_hash="0" * 64,
            data=data
        )
        self.chain.append(genesis_block)


    def _compute_hash(self, index, timestamp, prev_hash, data, nonce):
        block_dict = {
            "index": index,
            "timestamp": timestamp,
            "previous_hash": prev_hash,
            "data": data,
            "nonce": nonce
        }
        encoded = json.dumps(block_dict, sort_keys=True).encode("utf-8")
        return hash_sha256(encoded)

    def _mine_block(self, index: int, prev_hash: str, data: Dict[str, Any]) -> Block:
        nonce = 0
        timestamp = time.time()

        while True:
            block_hash = self._compute_hash(index, timestamp, prev_hash, data, nonce)
            if block_hash.startswith("0" * DIFFICULTY):
                return Block(
                    index=index,
                    timestamp=timestamp,
                    previous_hash=prev_hash,
                    data=data,
                    nonce=nonce,
                    hash=block_hash,
                )
            nonce += 1


    def add_block(self, data: Dict[str, Any]) -> Block:
        last_block = self.chain[-1]
        new_index = last_block.index + 1
        new_block = self._mine_block(new_index, last_block.hash, data)
        self.chain.append(new_block)
        return new_block


    def is_valid(self) -> bool:
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            prev = self.chain[i - 1]

            if current.previous_hash != prev.hash:
                return False

            recalculated = self._compute_hash(
                current.index,
                current.timestamp,
                current.previous_hash,
                current.data,
                current.nonce,
            )
            if current.hash != recalculated:
                return False

            if not current.hash.startswith("0" * DIFFICULTY):
                return False

        return True


    def to_list(self) -> List[Dict[str, Any]]:
        return [asdict(block) for block in self.chain]
