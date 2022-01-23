from FtxClient import FtxClient
import sched, time

key = 'YOUR API KEY HERE'
secret = 'YOUR SECRET API KEY HERE'
ftx = FtxClient(key, secret, 'Main account')

s = sched.scheduler(time.time, time.sleep)

bidav = 0
askav = 0
cup = 0
cdn = 0

while True:
    order = ftx.get_orderbook('RAY/USD', 100)
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
    moneyscew_limit1 = moneyscew * 0.1
    moneyscew_limit2 = moneyscew * 1.5
    if moneyscew > 0:
        if moneyscew_new > moneyscew_limit2:
            print('signal up ' + str(cup) + " by " + str(moneyscew_new - moneyscew_limit2))
            cup += 1
        elif moneyscew_new < moneyscew_limit1:
            print('signal down ' + str(cdn) + ' with ' + str(moneyscew_new-moneyscew_limit1))
            cdn += 1
    elif moneyscew < 0:
        if moneyscew_new < moneyscew_limit2:
            print("signal down " + str(cdn) + " with " + str(moneyscew_new-moneyscew_limit2))
            cdn += 1
        elif moneyscew_new > moneyscew_limit1:
            print("signal up " + str(cup) + " by " + str(moneyscew_new - moneyscew_limit1))
            cup += 1

    bidav = bidav_new
    askav = askav_new
