import requests
import os

class Notify:
    
    @staticmethod
    def notify(message):
        print("Notify: ", message)
        
        token = os.getenv("telegram_token", "")
        chat_id = os.getenv("telegram_chat_id", "")

        if not token == "" and not chat_id == "":
            send_text = 'https://api.telegram.org/bot' + token + \
                '/sendMessage?disable_notification=true&chat_id=' + \
                chat_id + '&parse_mode=Markdown&text=' + message

            _ = requests.get(send_text)