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


        if last_chat_text.startswith('/add'):
            parsed = None
            try:
                parsed = last_chat_text[5:].split(' * ')
            except:
                self.telegram.send_message(last_chat_id, 'Not valid input 1')
                return

            if len(parsed) != 2:
                self.telegram.send_message(last_chat_id, 'Not valid input')
            else:
                self.add_word(last_chat_id, parsed[0], parsed[1])

        elif last_chat_text.startswith('/delete'):
            pass
        else:
            self.telegram.send_message(last_chat_id, last_chat_text)


    def add_word(self, chat_id, word, translation):
        self.database.select('users', 'chat_id', '2')
        user = User(self.database.fetchone())
        user.eng_vocab = user.eng_vocab + '|' + word
        user.ru_vocab = user.ru_vocab + '|' + translation

        self.database.update('users', 'eng_vocab', user.eng_vocab, 'chat_id', '2')
        self.database.update('users', 'ru_vocab', user.ru_vocab, 'chat_id', '2')
        self.database.save()
        self.database.select('users', 'chat_id', '2')
        print(self.database.fetchone())

    def setup_database(self):
        self.database.start()
        self.database.save()
