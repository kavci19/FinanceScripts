from plyer import notification
from datetime import datetime, timedelta
from MailClient import send_mail
from Stocks import stockID


def computeThreeBar(current, oneMinute, twoMinute, stockName, buffer=0.03):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)

    quoteCurrent = stockID(current)
    quoteOneMinuteAgo = stockID(oneMinute)
    quoteTwoMinutesAgo = stockID(twoMinute)

    #quoteCurrent = stockID([2755.25, 2756])
    #quoteOneMinuteAgo = stockID([2754.75, 2754.75])
    #quoteTwoMinutesAgo = stockID([2754, 2755.25])

    print(stockName)
    print("Quote two minutes ago (open, close) is: " + str(quoteTwoMinutesAgo.open) +", "+ str(quoteCurrent.close))
    print("Quote one minute ago (open, close) is: " + str(quoteOneMinuteAgo.open) +", " + str(quoteOneMinuteAgo.close))
    print("Quote current (open, close) is: " + str(quoteCurrent.open) + ", "+ str(quoteCurrent.close))

    if (quoteTwoMinutesAgo.isUpward() and
            quoteOneMinuteAgo.isDownwardOrEqual() and
            quoteCurrent.isUpward()):

        if quoteOneMinuteAgo.close >= quoteTwoMinutesAgo.halfMark():


            buffer = 0.55*(quoteTwoMinutesAgo.close - quoteTwoMinutesAgo.open)

            #print(buffer)
            #print(quoteTwoMinutesAgo.close - buffer)

            print(quoteOneMinuteAgo.close)
            if (quoteTwoMinutesAgo.close + buffer >= quoteOneMinuteAgo.open and
                    quoteTwoMinutesAgo.close - buffer <= quoteOneMinuteAgo.close):



                if (quoteCurrent.open + buffer >= quoteOneMinuteAgo.close and
                        quoteCurrent.open - buffer <= quoteOneMinuteAgo.close):

                    if (quoteCurrent.isQuarterGrowthPlus(quoteOneMinuteAgo)):
                        print('Buy now!')
                        #notification.notify(
                            #title="Invest in /CLK20",
                            #message="Bar Algorithm predicts that this is a good entry point",
                            #timeout=10)
                        send_mail(stockName)
