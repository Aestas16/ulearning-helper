import hashlib
import base64
import time
import random
import string
import json

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def md5_encrypt(s: str) -> str:
    if s is None:
        return ""
    return hashlib.md5(s.encode('utf-8')).hexdigest()

def a1() -> str:
    return "ulearning"

def a3() -> str:
    return "331"

def a2() -> str:
    return "2021" + a3()

def get_login_string(str_val: str, str2: str) -> str:
    try:
        value_of = str(int(time.time() * 1000))
        
        md5_encrypt_1 = md5_encrypt(str_val)
        md5_encrypt_2 = md5_encrypt(value_of)
        md5_encrypt_3 = md5_encrypt("**Ulearning__Login##by$$project&&team@@")
        lower_case = str2.lower()
        
        concat_str = md5_encrypt_1 + lower_case + md5_encrypt_2 + md5_encrypt_3
        md5_encrypt_4 = md5_encrypt(concat_str)
        
        md5_encrypt_5 = md5_encrypt(value_of)
        substring_1 = md5_encrypt_5[:18]
        substring_2 = md5_encrypt_5[18:]

        return substring_1 + md5_encrypt_4 + substring_2

    except Exception as e:
        print(e)
        return ""

def is_empty(s: str) -> bool:
    return not s or len(s.strip()) == 0 or s.lower() == "null"

def encrypt(data_str: str, key_str: str) -> bytes:
    key = key_str.encode('utf-8')
    data = data_str.encode('utf-8')
    cipher = AES.new(key, AES.MODE_ECB)
    padded_data = pad(data, AES.block_size)
    return cipher.encrypt(padded_data)

def get_c_string(s: str) -> str:
    sb = []
    for i, char in enumerate(s):
        if len(sb) < 10:
            sb.append(random.choice(string.ascii_lowercase))
        sb.append(char)
    return "".join(sb)

def get_c_str(s: str) -> str:
    try:
        key = a1() + a2()
        encrypted_bytes = encrypt(s, key)
        base64_str = base64.b64encode(encrypted_bytes).decode('utf-8')
        return get_c_string(base64_str)
        
    except Exception as e:
        print(e)
        return ""

def decrypt(data_bytes: bytes, key_str: str) -> bytes:
    key = key_str.encode('utf-8')
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted_data = cipher.decrypt(data_bytes)
    return unpad(decrypted_data, AES.block_size)

def get_r_string(s: str) -> str:
    sb = []
    for i, char in enumerate(s):
        if i >= 10 or (i + 1) % 2 == 0:
            sb.append(char)
    return "".join(sb)

def get_r_str(s: str) -> str:
    try:
        key = a1() + a2()
        base64_str = get_r_string(s)
        decoded_bytes = base64.b64decode(base64_str)
        decrypted_bytes = decrypt(decoded_bytes, key)
        return decrypted_bytes.decode('utf-8')

    except Exception as e:
        print(e)
        return ""

def decode_result(s: str):
    s = s.replace("\n", "")
    return json.loads(get_r_str(s))