from FtxClient import FtxClient
import sched, time

key = 'INSERT API KEY HERE'
secret = 'INSERT SECRET KEY HERE'
ftx = FtxClient(key, secret, 'Main account')

pair = 'BTC/USD'

bidav = 0
askav = 0
cup = 0
cdn = 0
upmoney = 0
downmoney = 0
sp = ''

type_of_tran = ""

tran_open = False

while True:
    order = ftx.get_orderbook(pair, 50)
    bidmoney = []
    askmoney = []
    for bid in order['bids']:
        bidmoney.append(bid[0] * bid[1])
    for ask in order['asks']:
        askmoney.append(ask[0] * ask[1])

    bidav_new = sum(bidmoney) / len(bidmoney)
    askav_new = sum(askmoney) / len(askmoney)


    moneyscew_new = askav_new - bidav_new
    moneyscew = askav - bidav
    moneyscew_limit1 = moneyscew * 0
    moneyscew_limit2 = moneyscew * 2
    if moneyscew > 0:
        if moneyscew_new > moneyscew_limit2:
            print('signal up ' + str(cup) + " by " + str(moneyscew_new - moneyscew_limit2))
            upmoney += moneyscew_new - moneyscew_limit2
            cup += 1
            if not tran_open:
                sp = ftx.get_single_market(pair)
                print('TRANSACTION LONG MADE AT: ' + str(sp['price']))
                tran_open = not tran_open
                type_of_tran = 'LONG'

        elif moneyscew_new < moneyscew_limit1:
            print('signal down ' + str(cdn) + ' with ' + str(moneyscew_new - moneyscew_limit1))
            downmoney += moneyscew_new - moneyscew_limit1
            cdn += 1
            if not tran_open:
                sp = ftx.get_single_market(pair)
                print('TRANSACTION SHORT MADE AT: ' + str(sp['price']))
                tran_open = not tran_open
                type_of_tran = 'SHORT'

    elif moneyscew < 0:
        if moneyscew_new < moneyscew_limit2:
            print("signal down " + str(cdn) + " with " + str(moneyscew_new - moneyscew_limit2))
            downmoney += moneyscew_new - moneyscew_limit2
            cdn += 1
            if not tran_open:
                sp = ftx.get_single_market(pair)
                print('TRANSACTION SHORT MADE AT: ' + str(sp['price']))
                tran_open = not tran_open
                type_of_tran = 'SHORT'
        elif moneyscew_new > moneyscew_limit1:
            print("signal up " + str(cup) + " by " + str(moneyscew_new - moneyscew_limit1))
            upmoney += moneyscew_new - moneyscew_limit1
            cup += 1
            if not tran_open:
                sp = ftx.get_single_market(pair)
                print('TRANSACTION LONG MADE AT: ' + str(sp['price']))
                tran_open = not tran_open
                type_of_tran = 'LONG'

    print(upmoney + downmoney)
    if type_of_tran == 'LONG':
        if abs(upmoney) < abs(downmoney):
            np = ftx.get_single_market(pair)
            print('TRANSACTION LONG CLOSED AT: ' + str(np['price']))
            print('RETURN: ' + str(np['price'] - sp['price']))
            tran_open = not tran_open
            break
    elif type_of_tran == 'SHORT':
        if abs(upmoney) > abs(downmoney):
            np = ftx.get_single_market(pair)
            print('TRANSACTION SHORT CLOSED AT: ' + str(np['price']))
            print('RETURN: ' + str(sp['price'] - np['price']))
            tran_open = not tran_open
            break

    bidav = bidav_new
    askav = askav_new
