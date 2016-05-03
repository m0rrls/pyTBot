import requests, random

class EmoteQuiz:
    def __init__(self):
        r = requests.get('https://api.twitch.tv/kraken/chat/emotes/emoticons')
        j = r.json()['emoticons']
        self.emotes = []
        for x in j:
            if '\\' not in x['regex']:
                self.emotes.append(x['regex'])
        #print j['emoticons'][0]['regex']
        #print self.emotes

    def rand(self):
        return random.choice(self.emotes)

emotes = EmoteQuiz()
