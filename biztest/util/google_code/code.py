import hmac, base64, struct, hashlib, time
import authenticator.hotp

def calGoogleCode(secretKey):
    input = int(time.time())//30
    lens = len(secretKey)
    lenx = 8 - (lens % 4 if lens % 4 else 4)
    secretKey += 4 * '='
    print(secretKey, ' ----- ' ,lenx  , lens ,'|')


    key = base64.b32decode(secretKey, True)
    print(key)
    msg = struct.pack(">Q", input)
    googleCode = hmac.new(key, msg, hashlib.sha1).digest()
    print(googleCode)
    o = ord(googleCode[19]) & 15
    googleCode = str((struct.unpack(">I", googleCode[o:o+4])[0] & 0x7fffffff) % 1000000)
    if len(googleCode) == 5:
        googleCode = '0' + googleCode
    return googleCode

key = "AAAAB3NzaC1yc2EAAAADAQABAAABAQDQypxeGt6wCzhNFbBbcd6GGzS0oMwPCM2im9yjE6lmfk04BfEpyo7kDjTHbFEdJbYIJzEFcfuqKnxEByLJZlxcvye5shOChQun413OvVHfbQ56SH/m4hCPs2S8sxMt6Zf1liMa2v0gTlOuGH+U1LAKGlfbtLNwiG+kLWZdoDLnqC7VfGbiF4iUcWVu8MFnFXkLrfeOWpngTorGmfTBw9dMEh5kzHRvF1Zk6NYiqw4kT5QIw7uzOmwP5UGRjn+OKt0ylGwzaklHXdnh9hebMN9sg55K0xg21NU6ltJu/uMzCULGYdTHuzYaS3G9dY9w9tsqwm3TA7kGiQdaa9kDCz7r"
#calGoogleCode(key)



# -*- coding:utf-8 -*-
import hmac, base64, struct, hashlib, time

def get_hotp_token(secret, intervals_no):
    key = base64.b32decode(secret, True)
    msg = struct.pack(">Q", intervals_no)
    h = hmac.new(key, msg, hashlib.sha1).digest()
    o = ord(chr(h[19])) & 15
    h = (struct.unpack(">I", h[o:o+4])[0] & 0x7fffffff) % 1000000
    return h

def get_totp_token(secret):
    return get_hotp_token(secret, intervals_no=int(time.time())//30)

print(get_totp_token('xxxxxxxxx'))