#!/usr/bin/env python3
import sys
import os

def main():
    if len(sys.argv)>1 and sys.argv[1]=="dev":
        os.environ['dc-tg-env'] = "dev"

    from config import CONFIG
    import handler

    from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

    updater = Updater(CONFIG['bot_token'])
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', handler.start))
    dp.add_handler(CommandHandler('help', handler.help))
    dp.add_handler(CommandHandler('info', handler.info))
    dp.add_handler(CommandHandler('status', handler.status))
    dp.add_handler(CommandHandler('subscribe', handler.subscribe))
    dp.add_handler(CommandHandler('unsubscribe', handler.unsubscribe))
    dp.add_handler(CommandHandler('subscribtions', handler.subscribtions))
    dp.add_error_handler(handler.on_error)

    print(f"===============\nstarting dcNotifyTg to recive dcNotify subscribtions in [{CONFIG['env']}]")
    updater.bot.send_message(text=f"===============\nstarting dcNotifyTg to recive dcNotify subscribtions in [{CONFIG['env']}]", chat_id=CONFIG["chat_id"])
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()