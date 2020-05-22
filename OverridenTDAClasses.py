import asyncio
import json

import websockets
from td.client import TDClient
from td.stream import TDStreamerClient

from BarAlgorithm import computeThreeBar


class TDClient2(TDClient):
    def create_streaming_session(self):
        '''
            Creates a new streaming session that can be used to stream different data sources.
            RTYPE: TDStream Object
        '''

        # Grab the Streamer Info.
        userPrincipalsResponse = self.get_user_principals(
            fields=['streamerConnectionInfo', 'streamerSubscriptionKeys', 'preferences', 'surrogateIds'])

        # Grab the timestampe.
        tokenTimeStamp = userPrincipalsResponse['streamerInfo']['tokenTimestamp']

        # Grab socket
        socket_url = userPrincipalsResponse['streamerInfo']['streamerSocketUrl']

        # Parse the token timestamp.
        tokenTimeStampAsMs = self._create_token_timestamp(
            token_timestamp=tokenTimeStamp)

        # Define our Credentials Dictionary used for authentication.
        credentials = {"userid": userPrincipalsResponse['accounts'][0]['accountId'],
                       "token": userPrincipalsResponse['streamerInfo']['token'],
                       "company": userPrincipalsResponse['accounts'][0]['company'],
                       "segment": userPrincipalsResponse['accounts'][0]['segment'],
                       "cddomain": userPrincipalsResponse['accounts'][0]['accountCdDomainId'],
                       "usergroup": userPrincipalsResponse['streamerInfo']['userGroup'],
                       "accesslevel": userPrincipalsResponse['streamerInfo']['accessLevel'],
                       "authorized": "Y",
                       "timestamp": tokenTimeStampAsMs,
                       "appid": userPrincipalsResponse['streamerInfo']['appId'],
                       "acl": userPrincipalsResponse['streamerInfo']['acl']}

        # Create the session
        streaming_session = TDStreamerClient2(websocket_url=socket_url, user_principal_data=userPrincipalsResponse,
                                              credentials=credentials)

        return streaming_session

class TDStreamerClient2(TDStreamerClient):
    def stream(self):
        '''
            Initalizes the stream by building a login request, starting an event loop,
            creating a connection, passing through the requests, and keeping the loop running.
        '''

        # Grab the login info.
        login_request = self._build_login_request()

        # Grab the Data Request.
        data_request = json.dumps(self.data_requests)

        # Start a loop.
        self.loop = asyncio.get_event_loop()

        # Start connection and get client connection protocol
        connection = self.loop.run_until_complete(self._connect())

        # Start listener and heartbeat
        asyncio.ensure_future(self._receive_message(connection))
        asyncio.ensure_future(self._send_message(login_request))
        asyncio.ensure_future(self._send_message(data_request))
        # asyncio.ensure_future(self.close_stream())



        # Keep Going.
        self.loop.run_forever()



    async def _receive_message(self, connection):
        '''
            Receiving all server messages and handle them.
            NAME: connection
            DESC: The WebSocket Connection Client.
            TYPE: Object
        '''

        ES_TwoMinutesAgo = [0,0]
        ES_OneMinuteAgo = [0,0]
        ES_Current = [0,0]

        CLM_TwoMinutesAgo = [0, 0]
        CLM_OneMinuteAgo = [0, 0]
        CLM_Current = [0, 0]

        # Keep going until cancelled.
        while True:



            try:

                # recieve and decode the message.
                message = await connection.recv()

                try:
                    message_decoded = json.loads(message)

                    if "data" in message_decoded:
                        ES_Open = message_decoded.get('data')[0].get('content')[0].get('2')
                        ES_Close = message_decoded.get('data')[0].get('content')[0].get('5')

                        CLM_Open = message_decoded.get('data')[0].get('content')[1].get('2')
                        CLM_Close = message_decoded.get('data')[0].get('content')[1].get('5')



                        ES_TwoMinutesAgo = ES_OneMinuteAgo
                        ES_OneMinuteAgo = ES_Current
                        ES_Current = [ES_Open, ES_Close]

                        CLM_TwoMinutesAgo = CLM_OneMinuteAgo
                        CLM_OneMinuteAgo = CLM_Current
                        CLM_Current = [CLM_Open, CLM_Close]


                        computeThreeBar (ES_Current, ES_OneMinuteAgo, ES_TwoMinutesAgo, "/ES")
                        print()
                        computeThreeBar(CLM_Current, CLM_OneMinuteAgo, CLM_TwoMinutesAgo, "/CLM20")
                        print()
                        print()



                except:
                    message = message.encode('utf-8').replace(b'\xef\xbf\xbd', bytes('"None"', 'utf-8')).decode('utf-8')
                    message_decoded = json.loads(message)

                if 'data' in message_decoded.keys():
                    await self._write_to_csv(data=message_decoded['data'])

                #print('-' * 20)
                #print('Received message from server: {}'.format(str(message_decoded)))



            except websockets.exceptions.ConnectionClosed:

                # stop the connection if there is an error.
                print('Connection with server closed')
                break