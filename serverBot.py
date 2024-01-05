# !/usr/bin/env python

import argparse, dingtalk_stream, logging, time, threading, datetime
from dingtalk_stream import AckMessage
from dingtalk_webhook.dingtalk_webhook import initWebhook, send_message
from serverOperator.serverOperator import initOperator, getInfoMessage, startUpServer, shutDownServer, checkServer
from utils.log import preiodic_check_log

def setup_logger():
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter('%(asctime)s %(name)-8s %(levelname)-8s %(message)s [%(filename)s:%(lineno)d]'))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger

def define_options():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--webhook', dest='webhook', required=True,
        help='webhook for bot'
    )
    parser.add_argument(
        '--atUserPhone', dest='atUserPhone', required=True,
        help='user phone for warning'
    )
    parser.add_argument(
        '--client_id', dest='client_id', required=True,
        help='app_key or suite_key from https://open-dev.digntalk.com'
    )
    parser.add_argument(
        '--client_secret', dest='client_secret', required=True,
        help='app_secret or suite_secret from https://open-dev.digntalk.com'
    )
    parser.add_argument(
        '--host', dest='host', required=True,
        help='The host address of idrac'
    )
    parser.add_argument(
        '--user', dest='user', required=True,
        help='The username for idrac'
    )
    parser.add_argument(
        '--password', dest='password', required=True,
        help='The password for idrac'
    )
    parser.add_argument(
        '--temperatureLimit', dest='temperatureLimit', type=int, required=True,
        help='The temperature limit for warning'
    )
    parser.add_argument(
        '--powerLimit', dest='powerLimit', type=int, required=True,
        help='The power limit for warning'
    )
    options = parser.parse_args()
    return options

def periodicCheck():
    global lastCheckTime, lastCheckMessage
    while True:
        status, message = checkServer()
        if status == True:
            send_message(message)

        preiodic_check_log("./logs/periodic_check.log", 'status: {status}\nmessage: {message}'.format(status='ERROR' if status else 'OK', message=message))
        lastCheckTime = datetime.datetime.now()
        lastCheckMessage = message
        time.sleep(120)

class ServerBotHandler(dingtalk_stream.ChatbotHandler):
    global lastCheckTime, lastCheckMessage

    def __init__(self, logger: logging.Logger = None):
        super(dingtalk_stream.ChatbotHandler, self).__init__()
        if logger:
            self.logger = logger

    async def process(self, callback: dingtalk_stream.CallbackMessage):
        incoming_message = dingtalk_stream.ChatbotMessage.from_dict(callback.data)
        incoming_message_str = incoming_message.text.content.strip()

        if "help" in incoming_message_str:
            response = """
Commands:
    help: show this help message
    status: check serverBot
    info: show server's info
    startup: start up server
    shutdown: shut down server
""".strip()
        elif "status" in incoming_message_str:
            response = "ServerBot is running.\nLast check time: {lastCheckTime}\nLast check message: {lastCheckMessage}".format(lastCheckTime=lastCheckTime, lastCheckMessage=lastCheckMessage)
        elif "info" in incoming_message_str:
            response = getInfoMessage()
        elif "startup" in incoming_message_str:
            response = startUpServer()
        elif "shutdown" in incoming_message_str:
            response = shutDownServer()
        else:
            response = "Give me \"help\" to get commands."

        self.reply_text(response, incoming_message)

        return AckMessage.STATUS_OK, 'OK'

def main():
    logger = setup_logger()
    options = define_options()

    credential = dingtalk_stream.Credential(options.client_id, options.client_secret)
    initWebhook(options.webhook, options.client_secret, options.atUserPhone)
    initOperator(options.host, options.user, options.password, options.temperatureLimit, options.powerLimit)

    thread = threading.Thread(target=periodicCheck)
    thread.start()

    client = dingtalk_stream.DingTalkStreamClient(credential)
    client.register_callback_handler(dingtalk_stream.chatbot.ChatbotMessage.TOPIC, ServerBotHandler(logger))
    client.start_forever()

if __name__ == '__main__':
    main()