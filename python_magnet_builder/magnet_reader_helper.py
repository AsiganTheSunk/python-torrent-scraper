from typing import Iterable
from bencodepy import encode
from hashlib import sha1
from base64 import b16encode, b32encode, b64encode
from python_magnet_builder.constants.magnet_base_encode import MagnetBaseEncoding


class MagnetReaderHelper:
    def generate_hash(self, magnet_byte_info: Iterable, base_encoding=MagnetBaseEncoding.Base16) -> str:
        """
        This function will digest the magnet_byte_info to generate the hash for a magnet.
        By the Default, the base_encoding is 16
        :param magnet_byte_info:
        :param base_encoding:
        :return:
        """
        _hash: str = ''
        try:
            hash_contents = encode(magnet_byte_info)
            digest = sha1(hash_contents).digest()
            if base_encoding is MagnetBaseEncoding.Base16:
                _hash = b16encode(digest).decode().lower()
            elif base_encoding is MagnetBaseEncoding.Base32:
                _hash = b32encode(digest).decode().lower()
            elif base_encoding is MagnetBaseEncoding.Base64:
                _hash = b64encode(digest).decode().lower()
        except Exception as err:
            print(err)
        return _hash
