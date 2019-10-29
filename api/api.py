from fastapi import FastAPI
import hashlib
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
)

@app.get("/{proof}")
def check_proof_against_block_hash(proof: str):
    if len(proof) < 65:
        return {'valid': False}

    root_hash = proof[-64:]
    proof = proof[:-64]

    # Position + 256 bits (65 chars)
    items = [proof[i:i + 65] for i in range(0, len(proof), 65)]

    start_index = 2
    if items[0][0] == 'l':
        current_hash = b2bsha3_256(items[0][1:] + items[1][1:])
    elif items[0][0] == 'r':
        current_hash = b2bsha3_256(items[1][1:] + items[0][1:])
    elif items[0][0] == 'o':
        current_hash = b2bsha3_256(items[0][1:])
        start_index = 1
    else:
        return {'valid': False}

    for i in range(start_index, len(items)):
        if items[i][0] == 'l':
            current_hash = b2bsha3_256(items[i][1:] + current_hash)
        elif items[i][0] == 'r':
            current_hash = b2bsha3_256(current_hash + items[i][1:])
        elif items[i][0] == 'o':
            current_hash = b2bsha3_256(current_hash)
        else:
            return {'valid': False}

    if current_hash == root_hash:
        return {'root_hash': root_hash, 'valid': True}
    return {'valid': False}


def b2bsha3_512(text: str):
    return _blake2b_512(_sha3_512(text) + text)


def b2bsha3_256(text: str):
    return _blake2b_256(_sha3_512(text) + text)


def _blake2b_512(text: str):
    return hashlib.blake2b(text.encode('utf-8'), digest_size=64).hexdigest()


def _blake2b_256(text: str):
    return hashlib.blake2b(text.encode('utf-8'), digest_size=32).hexdigest()


def _sha3_512(text: str):
    return hashlib.sha3_512(text.encode('utf-8')).hexdigest()
