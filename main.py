from LennyWoods import LennyWoods
from User import User
def main():
    lenny = LennyWoods('data.db')
    lenny.start()

    lenny.database.start()
#    lenny.database.update('users', 'eng_vocab', '', 'chat_id', '2')
#    lenny.database.save()
#    lenny.database.update('users', 'ru_vocab', '', 'chat_id', '2')
#    lenny.database.save()
    #lenny.database.update('users', 'eng_vocab', 'qulity', 'chat_id', '2')
    #lenny.database.save()

    #lenny.database.select('users', 'chat_id', '2')

if __name__ == '__main__':
    main()
