from telebot import types
from apiwrapper.models import User
import logging


class StateMachine:
    def __init__(self, bot, api):
        self._bot = bot
        self.states = {}
        self.patterns = {}
        self.api = api

    def add_states(self, classes_states):
        for _class in classes_states:
            self.states.update({_class.state_id: _class})
            if _class.pattern:
                self.patterns.update({_class.pattern: _class})

    def handle(self, event):
        user_id = event.user.get('id')

        user = self.api.get_object(
            User, user_id)
        if not user:
            user = User(messenger_id=user_id)
            user = self.api.save_object(user)

        pattern_triggered = False
        if event.event_type == 'text':
            # handle text patterns
            for pattern, state in self.patterns.items():
                if pattern[-1] == '.':
                    if event.data.startswith(pattern[:-1]):
                        pattern_triggered = True
                        new_state = state
                else:
                    if event.data == pattern:
                        pattern_triggered = True
                        new_state = state
        if not pattern_triggered:
            if self.states.get(user.state):
                # handle event by previous state and get next state
                new_state = self.states[user.state]().handle(
                    self._bot, self.api, event, user)
            else:
                # get first state
                new_state = self.states[1]

        if new_state:
            # run and save new state
            new_state = new_state()
            user.state = new_state.state_id

            user = self.api.save_object(user)

            new_state.ask(self._bot, self.api, event, user)
