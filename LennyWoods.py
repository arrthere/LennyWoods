import random
import json

from Teleq import Teleq
from Sqyler import Sqyler
from User import User

class LennyWoods:

    def __init__(self, database_name):
        self.telegram = Teleq('309097307:AAEdwDKwNUn3KZH-4r8RkT_ok-D8GTKKSDQ')
        self.database = Sqyler(database_name)
        self.database.start()

    def start(self):
        offset = None

        while True:
            self.telegram.get_updates(offset)
            last_update = self.telegram.get_last_update()

            if last_update == None:
                print('No updates here')
                continue

            self.handle_update(last_update)
            offset = last_update['update_id'] + 1


    def handle_update(self, update):
        last_update_id = update['update_id']
        last_chat_text = update['message']['text']
        last_chat_id = update['message']['chat']['id']

        if last_chat_text == '/start':
            user = [last_chat_id, '', '', '', '']
            self.database.insert('users', user)
        elif last_chat_text == '/get':
            self.create_task(last_chat_id)
        elif last_chat_text.startswith('/add'):
            parsed = None
            try:
                parsed = last_chat_text[5:].split(' * ')
            except:
                self.telegram.send_message(last_chat_id, 'Not valid input.')
                return

            if len(parsed) != 2:
                self.telegram.send_message(last_chat_id, 'Not valid input.')
            else:
                self.add_word(last_chat_id, parsed[0], parsed[1])

        elif last_chat_text.startswith('/delete'):
            pass
        else:
            self.check_translation(last_chat_id, last_chat_text)

    def check_translation(self, chat_id, translation):
        self.database.select('users', 'chat_id', chat_id)
        if self.database.fetchone() == None:
            self.telegram.send_message(chat_id, 'Write /start at first.')
            return

        self.database.select('users', 'chat_id', chat_id)
        user = User(self.database.fetchone())
        if translation == user.now_trans:
            self.telegram.send_message(chat_id, 'Correct!')
        else:
            self.telegram.send_message(chat_id, 'You are wrong. The right word is "{}".'.format(user.now_trans))

        self.create_task(chat_id)

    def add_word(self, chat_id, word, translation):
        self.database.select('users', 'chat_id', chat_id)
        if self.database.fetchone() == None:
            self.telegram.send_message(chat_id, 'Write /start at first.')
            return

        self.database.select('users', 'chat_id', chat_id)
        try:
            user = User(self.database.fetchone())
            if user.eng_vocab and user.ru_vocab:
                user.eng_vocab = user.eng_vocab + '|' + word
                user.ru_vocab = user.ru_vocab + '|' + translation
            else:
                user.eng_vocab = word
                user.ru_vocab = translation

            self.database.update('users', 'eng_vocab', user.eng_vocab, 'chat_id', chat_id)
            self.database.update('users', 'ru_vocab', user.ru_vocab, 'chat_id', chat_id)
            self.database.save()

            self.database.select('users', 'chat_id', chat_id)
            print(self.database.fetchone())
            self.telegram.send_message(chat_id, 'Word {} is added!'.format(word))
        except:
            self.telegram.send_message(chat_id, 'Write /start at first.')

    def create_task(self, chat_id):
        self.database.select('users', 'chat_id', chat_id)
        if self.database.fetchone() == None:
            self.telegram.send_message(chat_id, 'Write /start at first.')
            return

        self.database.select('users', 'chat_id', chat_id)
        user = User(self.database.fetchone())

        eng_vocab = user.eng_vocab.split('|')
        ru_vocab = user.ru_vocab.split('|')
        if len(eng_vocab) < 4:
            self.telegram.send_message(chat_id, 'Add {} more words, please.'.format(4 - len(eng_vocab)))
            return

        index = random.randint(0, len(eng_vocab) - 1)
        word = eng_vocab[index]
        translation = ru_vocab[index]

        answers = []
        if random.randint(0, 1) == 0: # English word
            ru_vocab.remove(translation)
            answers = random.sample(ru_vocab, 3)
            answers.append(translation)
        else: # Russian word u know XD
            eng_vocab.remove(word)
            answers = random.sample(eng_vocab, 3)
            answers.append(word)
            word, translation = translation, word # some magic u know

        self.database.update('users', 'now_word', word, 'chat_id', chat_id)
        self.database.update('users', 'now_trans', translation, 'chat_id', chat_id)
        self.database.save()

        random.shuffle(answers)

        layout = [
            [answers[0], answers[1]],
            [answers[2], answers[3]]
        ]

        reply_markup = {"keyboard": layout, "resize_keyboard": False, "one_time_keyboard": True}
        reply_markup = json.dumps(reply_markup)

        self.telegram.send_message(chat_id, 'Choose translation for the word: {}.'.format(word), reply_markup=reply_markup)

    def setup_database(self):
        self.database.start()
        self.database.save()
