from LennyWoods import LennyWoods
from User import User
def main():
    lenny = LennyWoods('data.db')
    lenny.database.start()
    lenny.start();

#    columns = {
#        'chat_id': 'text',
#        'now_word': 'text',
#        'now_trans': 'text',
#        'eng_vocab': 'text',
#        'ru_vocab': 'text',
#    }

#    lenny.database.create_table('users', columns)
#    lenny.database.save()

if __name__ == '__main__':
    main()
