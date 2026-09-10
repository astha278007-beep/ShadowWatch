import hashlib
import json
from datetime import datetime


# Simple in-memory blockchain
blockchain = []


def generate_file_hash(file_path):
    """Generate SHA-256 hash of an evidence file."""

    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        while True:
            data = file.read(4096)

            if not data:
                break

            sha256.update(data)

    return sha256.hexdigest()


def create_evidence_record(file_path, incident_reason):
    """Create a blockchain-style record for CCTV evidence."""

    evidence_hash = generate_file_hash(file_path)

    previous_hash = (
        blockchain[-1]["block_hash"]
        if blockchain
        else "GENESIS_BLOCK"
    )

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    block_data = {
        "index": len(blockchain) + 1,
        "timestamp": timestamp,
        "incident_reason": incident_reason,
        "evidence_file": file_path,
        "evidence_hash": evidence_hash,
        "previous_hash": previous_hash
    }

    # Convert block data into a consistent string
    block_string = json.dumps(
        block_data,
        sort_keys=True
    ).encode()

    block_hash = hashlib.sha256(block_string).hexdigest()

    block_data["block_hash"] = block_hash

    blockchain.append(block_data)

    return block_data


def verify_blockchain():
    """Verify that blockchain records have not been modified."""

    for i, current_block in enumerate(blockchain):

        # Recreate the original block data without block_hash
        block_data = {
            "index": current_block["index"],
            "timestamp": current_block["timestamp"],
            "incident_reason": current_block["incident_reason"],
            "evidence_file": current_block["evidence_file"],
            "evidence_hash": current_block["evidence_hash"],
            "previous_hash": current_block["previous_hash"]
        }

        # Recalculate the hash
        block_string = json.dumps(
            block_data,
            sort_keys=True
        ).encode()

        recalculated_hash = hashlib.sha256(
            block_string
        ).hexdigest()

        # Check whether block data was modified
        if recalculated_hash != current_block["block_hash"]:
            return False

        # Check connection with previous block
        if i > 0:
            previous_block = blockchain[i - 1]

            if current_block["previous_hash"] != previous_block["block_hash"]:
                return False

    return True


def verify_evidence_integrity(file_path, original_hash):
    """
    Recalculate the current file hash and compare it
    with the original evidence hash.
    """

    current_hash = generate_file_hash(file_path)

    return {
        "original_hash": original_hash,
        "current_hash": current_hash,
        "integrity_verified": current_hash == original_hash
    }


def simulate_blockchain_tampering():
    """Temporarily modify blockchain data for testing."""

    if blockchain:
        blockchain[0]["incident_reason"] = "Evidence record modified for testing"
        return True

    return False


def reset_blockchain():
    """Clear all blockchain records and restore initial state."""

    blockchain.clear()