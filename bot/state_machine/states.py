import re
from enum import IntEnum, auto
from .types import InlineButton, KeyboardButton
from apiwrapper.models import Message


class States(IntEnum):
    START_STATE = auto()
    NAME_STATE = auto()
    BIRTHDAY_STATE = auto()
    AGE_STATE = auto()
    SEX_STATE = auto()
    NATIONALITY_STATE = auto()
    PHONE_STATE = auto()
    EMAIL_STATE = auto()
    PASSPORT_STATE = auto()
    MILITARY_CARD_STATE = auto()
    EDUCATION_STATE = auto()
    WAIT_STATE = auto()


class BaseState:
    state_id = None
    pattern = None
    next_state = None

    def ask(self, bot, api, event, user):
        pass

    def handle(self, bot, api, event, user):
        '''
        handle event
        and return next state
        '''
        return None


class StartState(BaseState):
    state_id = States.START_STATE
    pattern = '/start'

    def ask(self, bot, api, event, user):
        text = '<b>Здравствуйте, это вопросы к вакансии "Инженер". </b>\nДля продолжение нажмите <b>далее</b>.'
        buttons = [
            InlineButton(text='Далее', callback='next')
        ]
        bot.send_message(user.messenger_id, text, buttons=buttons)

    def handle(self, bot, api, event, user):
        if event.data == 'next':
            return NameState


class NameState(BaseState):
    state_id = States.NAME_STATE

    def ask(self, bot, api, event, user):
        text = '<b>Введите вашу Фамилию Имя Отчество(через пробел).</b>'
        bot.send_message(user.messenger_id, text)

    def handle(self, bot, api, event, user):
        full_name = event.data.split(' ')
        if len(full_name) >= 3:
            surname, name, second_name = full_name[0], full_name[1], full_name[2]
            if surname and name and second_name:
                user.surname = surname
                user.name = name
                user.second_name = second_name
                api.save_object(user)
                return BirthdayState
        else:
            text = '<b>Неверные данные. Попробуйте еще раз.</b>'
            bot.send_message(user.messenger_id, text)


class BirthdayState(BaseState):
    state_id = States.BIRTHDAY_STATE

    def ask(self, bot, api, event, user):
        text = '<b>Введите вашу дату рождения \'dd.mm.yy\'</b>'
        bot.send_message(user.messenger_id, text)

    def handle(self, bot, api, event, user):
        if event.data:
            user.birthday = event.data
            api.save_object(user)
            return AgeState


class AgeState(BaseState):
    state_id = States.AGE_STATE

    def ask(self, bot, api, event, user):
        text = '<b>Введите ваш возраст.</b>'
        bot.send_message(user.messenger_id, text)

    def handle(self, bot, api, event, user):
        if event.data:
            user.age = event.data
            api.save_object(user)
            return SexState


class SexState(BaseState):
    state_id = States.SEX_STATE

    def ask(self, bot, api, event, user):
        text = '<b>Выберите ваш пол.</b>'
        buttons = [
            InlineButton(text='Мужской', callback='man'),
            InlineButton(text='Женский', callback='woman'),
        ]
        bot.send_message(user.messenger_id, text, buttons=buttons)

    def handle(self, bot, api, event, user):
        if event.data:
            user.sex = event.data
            api.save_object(user)
            return NationalityState


class NationalityState(BaseState):
    state_id = States.NATIONALITY_STATE

    def ask(self, bot, api, event, user):
        text = '<b>Введите вашу национальность.</b>'
        bot.send_message(user.messenger_id, text)

    def handle(self, bot, api, event, user):
        if event.data:
            user.nationality = event.data
            api.save_object(user)
            return PhoneState


class PhoneState(BaseState):
    state_id = States.PHONE_STATE

    def ask(self, bot, api, event, user):
        text = '<b>Введите ваш номер телефона.</b>'
        bot.send_message(user.messenger_id, text)

    def handle(self, bot, api, event, user):
        if event.data:
            user.mobile_phone = event.data
            api.save_object(user)
            return EmailState


class EmailState(BaseState):
    state_id = States.EMAIL_STATE

    def ask(self, bot, api, event, user):
        text = '<b>Введите ваш email.</b>'
        bot.send_message(user.messenger_id, text)

    def handle(self, bot, api, event, user):
        regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        if re.search(regex, event.data):
            user.email = event.data
            api.save_object(user)
            return PassportState
        else:
            text = '<b>Введите корректный email.</b>'
            bot.send_message(user.messenger_id, text)


class PassportState(BaseState):
    state_id = States.PASSPORT_STATE

    def ask(self, bot, api, event, user):
        text = '<b>Введите ваш идентификационный номер.</b>'
        bot.send_message(user.messenger_id, text)

    def handle(self, bot, api, event, user):
        if event.data:
            user.passport_data = event.data
            api.save_object(user)
            return MilitaryCardState


class MilitaryCardState(BaseState):
    state_id = States.MILITARY_CARD_STATE

    def ask(self, bot, api, event, user):
        text = '<b>У вас есть военный билет?</b>'
        buttons = [
            InlineButton(text='Да', callback='yes'),
            InlineButton(text='Нет', callback='no'),
        ]
        bot.send_message(user.messenger_id, text, buttons)

    def handle(self, bot, api, event, user):
        if event.data:
            user.military_card = event.data
            api.save_object(user)
            return EducationState


class EducationState(BaseState):
    states_id = States.EDUCATION_STATE

    def ask(self, bot, api, event, user):
        text = '<b>Выберите ваше образование.</b>'
        buttons = [
            InlineButton(text='Высшее', callback='higher'),
            InlineButton(text='Среднее специальное',
                         callback='specialized_secondary'),
            InlineButton(text='Среднее', callback='average')
        ]
        bot.send_message(user.messenger_id, text, buttons)

    def handle(self, bot, api, event, user):
        if event.data:
            user.education = event.data
            api.save_object(user)
            return WaitState


class WaitState(BaseState):
    state_id = States.WAIT_STATE

    def ask(self, bot, api, event, user):
        text = '<b>Спасибо за пройденный опрос. С вами свяжутся в ближайшее время😉.</b>'
        bot.send_message(user.messenger_id, text)
