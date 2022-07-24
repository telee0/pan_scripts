#!/usr/bin/python3

"""

[2022072401]

Script to generate random passwords
    by Terence LEE <telee.hk@gmail.com>

"""

import os
import random
import string
import argparse
import hashlib


my_set = '!@$%^&*[]'

cf = {
    'set0': string.ascii_lowercase,
    'set1': string.ascii_lowercase + string.digits,
    'set2': string.ascii_lowercase + string.digits + string.ascii_uppercase,
    'set3': string.ascii_lowercase + string.digits + string.ascii_uppercase + my_set,
    'set4': string.ascii_uppercase + string.digits,
    'set5': string.digits,
    'set8': my_set,
    'set9': string.punctuation,
    'i': 2,
    'len': 15,
}


def print_charset():
    for key, value in cf.items():
        if key.startswith('set'):
            i = key[3:]
            print("charset {0}: {1}".format(i, value))


def gen_string(params):
    charset = cf['set' + str(params.charset_id)]
    length = len(charset)
    n = params.length
    s = ""
    for _ in range(n):
        i = random.randint(0, length - 1)
        s += charset[i]
    return s


def gen_hash(password):
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return salt, key


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='pass.py', description='Script to generate a random string/password.')
    parser.add_argument('-c', '--charset_id', nargs='?', type=int, default=cf['i'], help="charset ID")
    parser.add_argument('-l', '--length', nargs='?', type=int, default=cf['len'], help='length of generated string')
    parser.add_argument('-v', '--verbose', action='store_true', help="verbose mode")
    parser.add_argument('password', nargs='?')
    parser.print_help()

    print()
    print_charset()

    args = parser.parse_args()

    print()
    print(args)
    print()

    if args.password is None:
        args.password = gen_string(args)

    print("pass: {0}".format(args.password))

    if args.verbose:
        salt, key = gen_hash(args.password)
        print("salt {0}\nkey {1}".format(salt, key))
