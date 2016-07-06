from databaseControl import *
import requests, json
from time import *

class pointsUpdater:
    
    def run(self):
        self.createURL = "http://yarakitwitch.azurewebsites.net/ChatUsers/Create/"
        self.updateURL = "http://yarakitwitch.azurewebsites.net/ChatUsers/Edit/"
        self.infoURL = "http://yarakitwitch.azurewebsites.net/ChatUsers/GetId/"
        users = self.points.getUsers()
        for user in users:
            sub = self.subs.getUser("subs", user[0])
            try:
                json_data = {'username': user[0], 'points': user[1], 'subscribedSince': sub[1]}
            except TypeError:
                json_data = {'username': user[0], 'points': user[1], 'subscribedSince': '1969-06-09 13:33:37'}

            r = requests.post(self.createURL, data = json_data)
            if r.status_code != 200:
                rid = requests.post(self.infoURL, data = json_data)
                info_data = rid.json()
                json_data['ChatUserId'] = info_data['id']
                r2 = requests.post(self.updateURL+str(info_data['id']), data = json_data)
                if r2.status_code != 200:
                    print "nie udalo sie dodac lub zaktualizowac danych dla " + user[0]
                else:
                    print "update " + user[0]
                    
    def loop(self):
        self.points = DatabaseControl()
        self.subs = CustomDbCtrl("subs.db")
        while True:
            print '============================\natualizuje baze na stronie\n============================'
            self.run()
            sleep(60)