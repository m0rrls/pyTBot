import requests, json, string

def resToStr(tab):
    s = ""
    for x in tab:
        for y in x:
            s = s + str(y) + '\t\t'
        s = s + '\n'
    return s[:-1]

class SGist:
    #posts anonymous gist and return url to it
    def postAnon(self, desc, filename, cont):
        f123 = {"description": str(desc),"public": True, "files": {str(filename): { "content": str(cont)}}}
        #self.f123 = {"description": "Yarakii's subs","public": True, "files": {"topestKek.txt": { "content": "erroreq\ngezzior\nyarakii"}}}
        r = requests.post('https://api.github.com/gists', data=json.dumps(f123))
        js = r.json()
        return js['html_url']

#t1 = [('ania', 46.91087707178667), ('hisechi', 46.895182627253234), ('m0rrls', 0.006687256973236799)]
#print resToStr(t1)
#s = SGist().postAnon("test klasy","lulz.txt","T\nO\nP\nK\nE\nK")
