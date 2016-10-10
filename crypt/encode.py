import numpy as np
import random
import fractions
import rsa


def getAlphabet():
    delta = 1040
    d = {(a - delta): chr(a) for a in range(delta, delta + 64)}
    d.update({64: ' '})
    d.update({65: '.'})
    d.update({66: ','})
    d.update({67: '?'})
    d.update({68: '!'})
    d.update({69: '\n'})
    d.update({70: '-'})
    return d


def getNum(char, dic):
    for val, key in dic.items():
        if char == key:
            return val


def getString(vec, dic):
    tmp = ''
    for val in vec:
        if getChar(np.rint(val), dic):
            tmp = tmp + getChar(np.rint(val), dic)

    return tmp


def getChar(num, dic):
    for val, key in dic.items():
        if num == val:
            return key


def SplitList(list, chunk_size):
    return [list[offs:offs + chunk_size] for offs in range(0, len(list), chunk_size)]


def toNumVecX(msg, dic):
    listMsg = list(msg)
    n = len(listMsg)
    # exapnd message to 6 size block
    delta = 6 - n % 6
    if delta != 0 and delta != 6:
        for i in range(0, delta):
            listMsg.append(' ')

    # form new message by blocks nx6
    newMsg = SplitList(listMsg, 6)
    # convert to numbers
    for i in range(0, len(newMsg)):
        for j in range(0, len(newMsg[i])):
            newMsg[i][j] = getNum(newMsg[i][j], dic)
    return newMsg


def generateKey(vec, dic):
    n = len(vec)
    key = np.array([[50., 27., 60., 30., 53., 44.],
                    [32., 36., 12., 13., 55., 51.],
                    [59.,  4., 49., 2., 10., 54.],
                    [62., 26., 60., 20., 2., 17.],
                    [58., 68.,  3., 18., 37., 66.],
                    [24., 32., 58., 45., 14., 20.]])
    # key = np.zeros((n, n))
    # for i in range(0, n):
    #     for j in range(0, n):
    #         key[i, j] = getNum(random.choice(dic))

    # det = np.linalg.det(key)
    # if det == 0 or hasGCD(det, len(dic)) or xgcd(det, len(dic)) == 0:
    #     print('need new key')
    #     generateKey(vec, dic)
    return key


def encrypt(vec, dic, key):
    # numVec = key.dot(vec) % len(dic)
    encVec = []
    for i in range(0, len(vec)):
        encVec.extend(key.dot(vec[i]) % len(dic))

    return getString(encVec, dic)


def gcd(a, b):
    for i in range(-b, b):
        if (i * a % b) == 1.0:
            return i
    return None


def xgcd(b, n):
    x0, x1, y0, y1 = 1, 0, 0, 1
    while n != 0:
        q, b, n = b // n, n, b % n
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return b, x0, y0


def hasGCD(a, b):
    gcd = fractions.gcd(a, b)
    if gcd == 1:
        return False
    else:
        return True


def removeBlanks(msg):
    while msg.endswith(' '):
        msg = msg[:-1]
    return msg


def decrypt(cryptMsg, dic, key):
    vec = toNumVecX(cryptMsg, dic)
    decVec = []
    det = np.linalg.det(key).astype(int)
    adjKey = np.linalg.inv(key) * det % len(dic)
    coef = xgcd(det, len(dic))[1]
    if coef:
        invKey = coef * adjKey % len(dic)
        for i in range(0, len(vec)):
            decVec.extend(invKey.dot(vec[i]) % len(dic))

    s = getString(decVec, dic)
    return removeBlanks(s)


def keyToString(key, dic):
    n = key.shape
    tmp = ''
    for i in range(0, n[0]):
        for j in range(0, n[1]):
            tmp = tmp + getChar(key[i, j], dic)

    return tmp


def init(msg):
    # msg = 'Рыба-текст\n'
    dic = getAlphabet()
    vec = toNumVecX(msg, dic)
    key = generateKey(vec, dic)
    enc = encrypt(vec, dic, key)
    dec = decrypt(enc, dic, key)
    status = False
    if msg == dec:
        status = True

    return msg, enc, dec, status


# print(init('Пыф'))
