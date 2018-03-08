import requests, json, sys

# returns a header to use in subsequent requests
def authenticate():
    if sys.version_info < (3,0):
        sys.exit('Python version < 3.0 does not support modern TLS versions. You will have trouble connecting to our API using Python 2.X.')
    email = 'yhk@utexas.edu' 
    r = requests.post('https://mastermind.praetorian.com/api-auth-token/', data={'email':email})
    r.json()
    # > {'Auth-Token': 'AUTH_TOKEN'}
    headers = r.json()
    headers['Content-Type'] = 'application/json'
    return headers 

    
def run(headers):
    h = headers
    level = 1
    
    while(level < 7):
        levelurl = 'https://mastermind.praetorian.com/level/'+str(level)+'/'
        r = requests.get(levelurl, headers=h)
        print("STARTING LEVEL "+str(level)+"\n")
        print(r.json())
        guesser = Guesser(r.json())
        
        win = False
        while(win == False):
            g = guesser.next() 
            print("TRYING GUESS: "+str(guesser))
            r = requests.post(levelurl, data=json.dumps(g), headers=h)
            print(r.json())
            if('message' in r.json()):
                win = True
            if('error' in r.json()): # means we're out of guesses...
                print("OUT OF GUESSES- RESTARTING LEVEL\n")
                break

    
### c(glads, weaps) * weaps! = total # of possibilities
### log(total#) = min number of steps to find answer
# pass in json of the seed to init
# for now, works only with level parameters
class Guesser:
    def __init__(self, j):
        self.glads = j['numGladiators']
        self.guesses = j['numGuesses']
        self.rounds = j['numRounds']
        self.weaps = j['numWeapons']
        self.guess = [0,1,2,3]
        
    def __str__(self):
        return ' '.join(str(self.guess))
        
    def next(self):
        # for now, returns the same thing over and over
        return {'guess':[0,1,2,3]}

    
def main():
    run(authenticate())

if __name__ == "__main__":
    main()