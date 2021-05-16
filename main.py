import config


if __name__ == '__main__':
    from bot import Bot
    bot_ = Bot(bot_token=config.BOT_TOKEN)
    bot_.run()
