import requests as req
import asyncio

from pprint import pprint
import config

from time import sleep


if __name__ == '__main__':
    from bot import Bot
    bot_ = Bot()
    bot_.start()
