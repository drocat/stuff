from cryptography.fernet import Fernet
import dofast as df


def encrypt(message: bytes, key: bytes) -> bytes:
    return Fernet(key).encrypt(message)


def decrypt(token: bytes, key: bytes) -> bytes:
    return Fernet(key).decrypt(token)


# df.p(encrypt('somekey', 'passport123'))
import base64
from Crypto.Cipher import AES


def encode(msg_text: str, passphrase: str) -> str:
    msg_text += '|' + msg_text * 100
    msg_text = msg_text[:1024]
    bytes_text = msg_text.encode().rjust(1024)  # in case this is a long text
    passphrase = passphrase.encode().ljust(32, b'*')
    cipher = AES.new(passphrase, AES.MODE_ECB)
    return base64.b64encode(cipher.encrypt(bytes_text)).decode('ascii')


def decode(msg_text: str, passphrase: str) -> str:
    bytes_text = msg_text.encode().ljust(1024)
    passphrase = passphrase.encode().ljust(32, b'*')
    try:
        cipher = AES.new(passphrase, AES.MODE_ECB)
        return cipher.decrypt(
            base64.b64decode(bytes_text)).decode().split('|')[0]
    except Exception as e:
        df.error(f"Maybe wrong password. {e}")
        return ""


# prefix_encoded = 'qFhbK6JYIjPKJwulGyQo+9IDAawMvJbNwJwsl9h/JIhVYfGseXHvRpIOUQ7+Z8IjdZcJCml7F4SZCujY9htyCn6II8OdZO659uQg+9i4VVh+iCPDnWTuufbkIPvYuFVYfogjw51k7rn25CD72LhVWH6II8OdZO659uQg+9i4VVh+iCPDnWTuufbkIPvYuFVYfogjw51k7rn25CD72LhVWH6II8OdZO659uQg+9i4VVh+iCPDnWTuufbkIPvYuFVYfogjw51k7rn25CD72LhVWH6II8OdZO659uQg+9i4VVh+iCPDnWTuufbkIPvYuFVYfogjw51k7rn25CD72LhVWA=='
url = 'https://ali-oss-bucket-1.oss-cn-beijing.aliyuncs.com/'
# url = ''
prefix_encoded = encode(url, '0')
print(prefix_encoded)

from getpass import getpass
password = getpass('Type in your password: ')
url = decode(prefix_encoded, password) + 'abc.zip'

df.p(url)
#
