import requests
import time


class BotConnection:
    def __init__(self):
        self._url = "https://fwbot.ru/bot/sendResponse"

    def send_response(self, data):
        page = requests.post(self._url, json = data)
        return page.text

            # request_user_id = await self.db_session.execute(
            #     select(
            #         Adverts.user_id,
            #         Adverts.advert_title
            #     ).where(
            #         Adverts.advert_id==advert_id
            #     )
            # )
            # advert_info = request_user_id.all()
            # if advert_info == []: return
            # else: 
            #     user_id = advert_info[0][0]
            #     advert_title = advert_info[0][1]

            # data = {
            #         "user_id" : user_id,
            #         "advert_title": advert_title,
            #         "advert_url": "",
            #         "response_text": response_text,
            #         "response_price": price
            #         }
            # bot_connection = BotConnection()
            # res = bot_connection.send_response(data)
    
