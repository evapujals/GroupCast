
class Impress(object):
    _tell = ['impress', 'show_content']

    def __init__(self):
        self.data = {}

    def impress(self, info):
        print info

    def show_content(self, name, data, cycles):
        text = ""
        for val in list(data.values()):
            text = text + val
        string_length = len(text)
        print "ID: " + str(name)
        print "Content: " + text
        print "Number of cycles: ", int(cycles)
        print "Length of string: ", int(string_length), "\n"
