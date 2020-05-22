import asyncio
import json
from MailClient import send_mail
from BarAlgorithm import computeThreeBar
import websockets
from td.client import TDClient
from td.stream import TDStreamerClient
import pprint
from td.client import TDClient
from OverridenTDAClasses import TDClient2, TDStreamerClient2
from datetime import datetime, timedelta
import sys


def main():


    CONSUMER_ID = 0 #insert id here

    REDIRECT_URI = 'http://localhost'

    JSON_PATH = None

    TDSession = TDClient2(consumer_id=CONSUMER_ID, redirect_uri=REDIRECT_URI, json_path=JSON_PATH)

    TDSession.login()

    TDStreamingClient = TDSession.create_streaming_session()

    TDStreamingClient.chart(service='CHART_FUTURES', symbols=['/ES', '/CLM20'], fields=[0, 1, 2, 3, 4, 5, 6, 7])

    while True:
        TDStreamingClient.stream()











if __name__ == "__main__":
    main()
