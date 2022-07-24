import pickle
import hashlib

users = [
    {
        "name": "root",
        "password": hashlib.sha512(b"Password").digest(),
        "admin": True
    }
]

with open("users.dat", "ab") as f:
    pickle.dump(users, f)
