import math
import os
import random
import sys
import types
import rsa

'''
Euclid's algorithm for determining the greatest common divisor
Use iteration to make it faster for larger integers
'''


def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

'''
Euclid's extended algorithm for finding the multiplicative inverse of two numbers
'''


def multiplicative_inverse(a, b):
    """Returns a tuple (r, i, j) such that r = gcd(a, b) = ia + jb
    """
    # r = gcd(a,b) i = multiplicitive inverse of a mod b
    #      or      j = multiplicitive inverse of b mod a
    # Neg return values for i or j are made positive mod b or a respectively
    # Iterateive Version is faster and uses much less stack space
    x = 0
    y = 1
    lx = 1
    ly = 0
    oa = a  # Remember original a/b to remove
    ob = b  # negative values from return results
    while b != 0:
        q = a // b
        (a, b) = (b, a % b)
        (x, lx) = ((lx - (q * x)), x)
        (y, ly) = ((ly - (q * y)), y)
    if lx < 0:
        lx += ob  # If neg wrap modulo orignal b
    if ly < 0:
        ly += oa  # If neg wrap modulo orignal a
    # return a , lx, ly  # Return only positive values
    return lx

'''
Tests to see if a number is prime.
'''


def find_p_q(nbits):
    """Returns a tuple of two different primes of nbits bits"""
    pbits = nbits + (nbits / 16)  # Make sure that p and q aren't too close
    qbits = nbits - (nbits / 16)  # or the factoring programs can factor n
    p = getprime(pbits)
    while True:
        q = getprime(qbits)
        # Make sure p and q are different.
        if not q == p:
            break
    return (p, q)


def read_random_int(nbits):
    """Reads a random integer of approximately nbits bits rounded up
    to whole bytes"""

    nbytes = int(math.ceil(nbits / 8.))
    randomdata = os.urandom(nbytes)
    return bytes2int(randomdata)


def getprime(nbits):
    """Returns a prime number of max. 'math.ceil(nbits/8)*8' bits. In
    other words: nbits is rounded up to whole bytes.
    """

    while True:
        integer = read_random_int(nbits)

        # Make sure it's odd
        integer |= 1

        # Test for primeness
        if is_prime(integer):
            break

        # Retry if not prime

    return integer


def is_prime(num):
    if num == 2:
        return True
    if num < 2 or num % 2 == 0:
        return False
    for n in range(3, int(num**0.5) + 2, 2):
        if num % n == 0:
            return False
    return True


def generate_keypair(p, q):
    if not (is_prime(p) and is_prime(q)):
        raise ValueError('Both numbers must be prime.')
    elif p == q:
        raise ValueError('p and q cannot be equal')
    #n = pq
    n = p * q

    # Phi is the totient of n
    phi = (p - 1) * (q - 1)

    # Choose an integer e such that e and phi(n) are coprime
    e = random.randrange(1, phi)

    # Use Euclid's Algorithm to verify that e and phi(n) are comprime
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)

    # Use Extended Euclid's Algorithm to generate the private key
    d = multiplicative_inverse(e, phi)

    # Return public and private keypair
    # Public key is (e, n) and private key is (d, n)
    return ((e, n), (d, n))


def newkeys(nbits):
    p, q = find_p_q(nbits)
    return generate_keypair(p, q)


def encrypt(plaintext, pk):
    # Unpack the key into it's components
    key, n = pk
    # Convert each letter in the plaintext to numbers based on the character
    # using a^b mod m
    cipher = [((char) ** key) % n for char in plaintext]
    # Return the array of bytes
    return cipher


def decrypt(ciphertext, pk):
    # Unpack the key into its components
    key, n = pk
    # Generate the plaintext based on the ciphertext and key using a^b mod m
    plain = [((char ** key) % n) for char in ciphertext]
    # Return the array of bytes as a string
    # return ''.join(plain)
    return plain
