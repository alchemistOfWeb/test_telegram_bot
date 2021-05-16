import asyncio

import config


if __name__ == '__main__':
    from bot import Bot
    bot_ = Bot(token=config.BOT_TOKEN)
    bot_.run()
