import math
import os
import random
import sys
import types
import numpy as np
# import rsa


'''
Euclid's algorithm for determining the greatest common divisor
Use iteration to make it faster for larger integers
'''


def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

'''
Computing the least common multiple
'''


def lcm(a, b):
    lmda = abs(a * b) / gcd(a, b)
    return int(lmda)

'''
L - function: L(u) = (u-1)/n
'''


def L(u, n):
    return ((u - 1) / n)


def generate_nu(lmda, g, n):
    return ((L((g ** lmda) % n**2, n)) ** (-1)) % n

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


def is_prime(num):
    if num == 2:
        return True
    if num < 2 or num % 2 == 0:
        return False
    for n in range(3, int(num**0.5) + 2, 2):
        if num % n == 0:
            return False
    return True


def read_random_int(nbits):
    return np.random.random_integers(nbits)


def getprime(nbits):
    """Returns a prime number of max. 'math.ceil(nbits/8)*8' bits. In
    other words: nbits is rounded up to whole bytes.
    """

    nbytes = int(math.ceil(nbits / 8.))

    while True:
        integer = read_random_int(nbits)

        # Make sure it's odd
        integer |= 1

        # Test for primeness
        if is_prime(integer):
            break

        # Retry if not prime

    return integer


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
        if gcd(p * q, (p - 1) * (q - 1)) == 1:
            break
    return (p, q)


def generate_keypair(p, q):
    if not (is_prime(p) and is_prime(q)):
        raise ValueError('Both numbers must be prime.')
    elif p == q:
        raise ValueError('p and q cannot be equal')
    # n = pq
    n = p * q

    # lambda = lcm(p-1, q-1)
    lmda = lcm(p - 1, q - 1)

    # Choose an integer g where g in Z(n^2)
    g = random.randrange(1, n)
    j = gcd(lmda, g)
    while j != 1:
        g = random.randrange(1, n)
        j = gcd(g, lmda)

    # Use Euclid's Algorithm to verify that g and nu are comprime
    # nu = gcd(lmda, g)
    # while nu != 1:
    #     g = random.randrange(1, n**2)
    #     nu = gcd(g, nu)

    # Use Extended Euclid's Algorithm to generate the private key
    # d = multiplicative_inverse(e, phi)
    # nu = generate_nu(lmda, g, n)
    # Return public and private keypair
    # Public key is (n, g) and private key is (lmda, nu)
    return ((n, g), (lmda))


def newkeys(nbits):
    p, q = find_p_q(nbits)
    print(p, q)
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
