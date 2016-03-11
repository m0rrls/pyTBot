import urllib2, json, string

class Followers:

    def __init__(self):
        self.url = "https://api.twitch.tv/kraken/channels/yarakii/follows/?limit=100"
        response = urllib2.urlopen(self.url)
        self.data = json.load(response)
        self.nrOfFollowers = self.data['_total']
        self.listing = set()
        #print self.nrOfFollowers
        #print self.data['follows'][0]['user']['display_name']

    def getFollowers(self):
        #zm1 = self.data['follows']
        #print len(zm1)
        while len(self.listing) < self.nrOfFollowers:
            ident = 0
            while ident < 100 and len(self.listing) < self.nrOfFollowers:
                #print str(ident) + ": " + self.data['follows'][ident]['user']['display_name']
                self.listing.add(self.data['follows'][ident]['user']['display_name'])
                ident = ident + 1
            self.url = self.data['_links']['next']
            response = urllib2.urlopen(self.url)
            self.data = json.load(response)
        return self.listing

    def getNr(self):
        return self.nrOfFollowers

    def checkIfFollows(self, follower):
        self.getFollowers()
        if follower in self.listing:
            return True
        else:
            return False

obj = Followers()
zbior = obj.getFollowers()
for x in zbior:
    print x

if obj.checkIfFollows("M0RRlS"):
    print "PogChamp"
