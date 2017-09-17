
class User:
    def __init__(self, data):
        self.chat_id = data[0]
        self.now_word = data[1]
        self.now_trans = data[2]
        self.eng_vocab = data[3]
        self.ru_vocab = data[4]
