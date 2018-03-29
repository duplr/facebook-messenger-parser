from tkinter.filedialog import askopenfilename
from html.parser import HTMLParser


class Person:
    def __init__(self, name):
        self.name = name
        self.messages = 0
        self.words = {}

    def __eq__(self, other):
        return other == self.name

    def __str__(self):
        return self.name


class Parser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.participants = []
        self.previousEndTag = None
        self.previousStartTag = None
        self.previousContactIndex = None
        self.globalFrequency = {}
        self.globalTotal = 0
        self.userFlag = 0

    def error(self, message):
        pass

    def handle_starttag(self, tag, attrs):
        self.previousStartTag = tag
        for name, value in attrs:
            if name == 'class' and value == 'user':
                self.userFlag = 1

    def handle_endtag(self, tag):
        self.previousEndTag = tag

    def handle_data(self, data):
        if self.previousEndTag == "h3" and data.startswith('Participants: '):
            participants = data[14:].split(', ')
            for contact in participants:
                self.participants.append(Person(contact))
        elif self.userFlag:
            self.userFlag = 0
            if data in self.participants:
                self.previousContactIndex = self.participants.index(data)
            else:
                self.participants.append(Person(data))
                self.previousContactIndex = -1
        elif self.previousContactIndex is not None:
            if self.previousStartTag != "p":
                return None
            contact = self.participants[self.previousContactIndex]
            contact.messages += 1
            self.globalTotal += 1
            wordlist = data.lower.split() if ignoreCase else data.split()
            for foundWord in wordlist:
                if foundWord not in contact.words:
                    contact.words[foundWord] = 1
                    if foundWord not in self.globalFrequency:
                        self.globalFrequency[foundWord] = 1
                else:
                    contact.words[foundWord] += 1
                    self.globalFrequency[foundWord] += 1
            self.previousContactIndex = None


if __name__ == "__main__":
    userQuit = False
    while not userQuit:
        ignoreCase = False
        if input("Treat all words as lowercase? [Y/N]: ").lower == 'y':
            ignoreCase = True
        threshold = input("Exclude word frequencies under: ")
        while not threshold.isnumeric():
            threshold = input("Please enter a number: ")
        print("Please select an html file under [archive location]/facebook-[username]/messages")

        filename = askopenfilename()
        chatFile = open(filename, 'r', encoding='utf8')
        chatParser = Parser()
        print("Depending on the length of your conversation, this could take a while...")
        chatParser.feed(chatFile.read())
        output = open(filename + ".csv", 'w', encoding='utf8')

        columnTitleRow = "name,word,frequency\n"
        output.write(columnTitleRow)

        for username in chatParser.participants:
            for singleWord, wordFreq in sorted(username.words.items(), key=lambda x: x[1], reverse=True):
                if wordFreq > int(threshold):
                    row = "{},\"{}\",{}\n".format(username, singleWord, wordFreq)
                    output.write(row)

        if chatParser.globalFrequency != {}:
            for singleWord, wordFreq in sorted(chatParser.globalFrequency.items(), key=lambda x: x[1], reverse=True):
                if wordFreq > int(threshold):
                    row = "*,\"{}\",{}\n".format(singleWord, wordFreq)
                    output.write(row)

        print("Output successful: {}".format(output.name))
        output.close()
        userQuit = False if input("Process another file? [Y/N]: ").lower() == 'y' else True
    exit(0)
