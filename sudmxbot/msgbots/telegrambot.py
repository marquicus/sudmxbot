# -*- coding: utf-8 -*-

"""
Telegram Bots.
"""

from telegram.ext import CommandHandler, Updater
import logging
import sys
import os

sys.path.insert(0, os.path.abspath('.'))


class Bot:

    def __init__(self):
        try:
            self.token = os.environ.get('TELEGRAM_API_TOKEN')
            self.updater = Updater(token=self.token, use_context=True)
            logging.info("Bot {} grabbed.".format(self.updater.bot.username))
        except Exception:
            logging.error("Unable to grab bot.")
            sys.exit()

        self.dispatcher = self.updater.dispatcher

        self.start_handler = CommandHandler("inicio", self.start)
        self.hello_handler = CommandHandler("hola", self.hello)
        self.help_handler = CommandHandler("ayuda", self.help)
        self.covidmx_handler = CommandHandler("covidmx", self.covidmx)

        self.dispatcher.add_handler(self.start_handler)
        self.dispatcher.add_handler(self.hello_handler)
        self.dispatcher.add_handler(self.help_handler)
        self.dispatcher.add_handler(self.covidmx_handler)

    def start(self, update, context):
        """start command handler.

        Args:
            update (dict): message that triggered the handler
            context (CallbackContext): context
        """
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Start message goes here.",
        )

    def hello(self, update, context):
        """Hello command handler.

        Args:
            update (dict): message that triggered the handler
            context (CallbackContext): context
        """
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Hello world.",
        )

    def help(self, update, context):
        """help command handler.

        Args:
            update (dict): message that triggered the handler
            context (CallbackContext): context
        """
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Help tetx goes here.",
        )

    def covidmx(self, update, context):
        """help command handler.

        Args:
            update (dict): message that triggered the handler
            context (CallbackContext): context
        """
        from sudmxbot.models import Daily
        d = Daily.select().get()
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Reporte al dia de hoy {d.fecha}:\n{d.casos}\n{d.defunciones}.",
        )

    def start_bot(self):
        """Start the bot.
        """
        self.updater.start_polling()
        self.updater.idle()


if __name__ == "__main__":
    bot = Bot()
    bot.start_bot()
