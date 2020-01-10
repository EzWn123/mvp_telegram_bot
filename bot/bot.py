import telebot
from telebot.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, KeyboardButton, Message,
                           ReplyKeyboardMarkup, ReplyKeyboardRemove)

from apiwrapper import client
from state_machine import states, types
from state_machine.state_machine import StateMachine


class TelegramBot(types.Bot):
    def __init__(self, token, api_url, host='', ssl_cert_path=''):
        self.bot = telebot.TeleBot(token)
        self.api = client.ApiClient(api_url)
        self.state_machine = StateMachine(self, self.api)
        self.state_machine.add_states(
            [states.StartState, states.NameState, states.BirthdayState, states.AgeState, states.SexState, states.NationalityState, states.PhoneState, states.EmailState, states.PassportState, states.MilitaryCardState, states.EducationState, states.WaitState])

        self.bot.message_handler(content_types=['text'])(self.handler)
        self.bot.callback_query_handler(func=lambda call: True)(self.handler)

        self.bot.remove_webhook()
        webhook_url = 'https://{}/telegrambot/webhook/'.format(host)
        self.bot.set_webhook(
            url=webhook_url, certificate=open(ssl_cert_path, 'r'))

    def generate_markup(self, buttons, row_width=2):
        markup = None
        if isinstance(buttons[0], types.InlineButton):
            markup = InlineKeyboardMarkup(row_width=row_width)
            markup.add(
                *[InlineKeyboardButton(x.text, callback_data=x.callback) for x in buttons if isinstance(x, types.InlineButton)])
        elif isinstance(buttons[0], types.KeyboardButton):
            markup = ReplyKeyboardMarkup(
                resize_keyboard=True, row_width=row_width)
            markup.add(*[KeyboardButton(x.text)
                         for x in buttons if isinstance(x, types.KeyboardButton)])
        return markup

    def send_message(self, user_id, text, buttons=None, buttons_rows=2, parse_mode='Html'):
        markup = self.generate_markup(
            buttons, row_width=buttons_rows) if buttons else None
        message = self.bot.send_message(
            user_id, text, reply_markup=markup, parse_mode='html')
        event = types.Event(
            user={'id': message.from_user.id},
            data=message.text,
            event_type='text',
        )
        return event

    def handler(self, tg_event):
        if isinstance(tg_event, CallbackQuery):
            self.bot.answer_callback_query(tg_event.id)
            event = types.Event(
                user={'id': tg_event.from_user.id},
                data=tg_event.data,
                event_type='callback',
            )
        else:
            event = types.Event(
                user={'id': tg_event.from_user.id},
                data=tg_event.text,
                event_type='text',
            )
        self.state_machine.handle(event)
