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


def getChar(num, dic):
    for val, key in dic.items():
        if num == val:
            return key


def toNumVecX(msg, dic):
    listMsg = list(msg)
    n = len(listMsg)
    newMsg = []
    for i in range(0, n):
        newMsg.append(getNum(listMsg[i], dic))
    return newMsg


def getString(vec, dic):
    tmp = ''
    for val in vec:
        if getChar(np.rint(val), dic):
            tmp = tmp + getChar(np.rint(val), dic)

    return tmp


def getKey(msg, dic):
    key = ''
    for i in range(0, len(msg)):
        key += random.choice(dic)
    return rep(key, len(msg))


def rep(s, m):
    a, b = divmod(m, len(s))
    return s * a + s[:b]


def getSum(a, b):
    return [x + y for x, y in zip(a, b)]


def addNum(list, a):
    return [x + a for x in list]


def getSub(a, b):
    return [x - y for x, y in zip(a, b)]


def encrypt(msg, key, dic):
    T = toNumVecX(msg, dic)
    G = toNumVecX(key, dic)
    tmp = getSum(T, G)
    C = []
    for i in tmp:
        C.append(i % len(dic))
    return C


def decrypt(msg, key, dic):
    C = toNumVecX(msg, dic)
    G = toNumVecX(key, dic)
    tmp = getSub(C, G)
    CGN = addNum(tmp, len(dic))
    T = []
    for i in CGN:
        T.append(i % len(dic))

    return T


def init(msg):
    print("Ваше сообщение: ", msg)
    dic = getAlphabet()
    key = getKey(msg, dic)
    print("Ключ: ", key)
    C = encrypt(msg, key, dic)
    cs = getString(C, dic)
    print("Зашифрованное сообщение: ", cs)
    T = decrypt(cs, key, dic)
    ts = getString(T, dic)
    print("Дешифрованное сообщение: ", ts)
