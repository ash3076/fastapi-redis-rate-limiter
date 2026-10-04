from pwdlib import PasswordHash

hash = PasswordHash.recommended()


def hash_password(password:str):
    return hash.hash(password)

def verify_password(password: str , db_password : str):
    return hash.verify(password , db_password)