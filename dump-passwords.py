import argparse
import sqlite3
import sys

from Crypto.Cipher import AES


def decrypt_password(data, key):
    iv = data[3:15]
    ciphertext = data[15:]
    
    cipher = AES.new(key, AES.MODE_GCM, iv)
    
    plaintext = cipher.decrypt(ciphertext)
    password = plaintext[:-16].decode()
    
    return password


def main(db, key):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    
    cursor.execute("SELECT signon_realm, username_value, password_value FROM logins WHERE blacklisted_by_user = 0")
    
    for row in cursor.fetchall():
        password = decrypt_password(row[2], key)
        
        print(f"URL:\t\t{row[0]}")
        print(f"Username:\t{row[1]}")
        print(f"Password:\t{password}")
        print("")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--db', required=True, metavar="<path>", help="Chrome login database")
    parser.add_argument('--key', required=True, metavar="<key>", help="Encryption key")
    
    args = parser.parse_args()
    
    main(args.db, bytes.fromhex(args.key))