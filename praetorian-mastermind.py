import requests, json, sys, Mastermind
from scipy.special import comb

class MastermindSolver:

    def __init__(self):
        self.VERSION_INFO_MSG = 'Python version < 3.0 does not support modern TLS versions. You will have trouble connecting to our API using Python 2.X.'
        self.EMAIL = 'yhk@utexas.edu' # hardcoded cos this is MINE!!! ONLY MINE!
        self.BASE_URL = 'https://mastermind.praetorian.com'
        self.WRONG_LEVEL = 'Requested level cannot yet be challenged, complete lower levels first.'
        self.NEXT_LEVEL = 'Onto the next level'
        self.TOOK_TOO_LONG = 'Guess took too long, please restart game.'
        self.TOO_MANY_GUESSES = 'Too many guesses. Try again!'

        self.level = 1
        self.headers = self.initHeaders(self.EMAIL)
        self.seed_power = 3 # how many guesses to leave after seed
        
        
    def initHeaders(self, email):
    ### returns a header to use in subsequent requests ###

        if sys.version_info < (3,0):
            sys.exit(self.VERSION_INFO)
        headers = requests.post(self.BASE_URL + '/api-auth-token/', data={'email':email}).json()
        headers['Content-Type'] = 'application/json'
        return headers

    
    def request(self, url, method, data=None):
    ### sends a request to the game as a GET or POST to any of the api endpoints ###
    ### data arg, if provided, is a dict object that is serialized into json for POST ###
    ### returns the response as json ###

        if method == 'POST':
            if data:
                r = requests.post(url, data=json.dumps(data), headers=self.headers).json()
            else:
                r = requests.post(url, headers=self.headers).json()

        elif method == 'GET':
            r = requests.get(url, headers=self.headers).json()

        else:
            print("I should raise an exception!")

        return r


    def resumeLevel(self):
    ### brings us to the level that we were at before ###
    ### returns the response ###

        levelurl = self.BASE_URL + '/level/' + str(self.level) + '/'
        r = self.request(levelurl, method='GET')
        while('error' in r and r['error']):
            self.level += 1
            levelurl = self.BASE_URL + '/level/' + str(self.level) + '/'
            r = self.request(levelurl, method='GET')            

        return r        


    def reset(self):
    ### resets the game ###
        url = self.BASE_URL + '/reset/'
        r = self.request(url, method='POST')
        print("< Game reset ! >")


    def seedGen(self, m, levelurl):
    ### generates a seed for genTable ###

        seed_count = m.getNumberOfGuesses() - self.seed_power

        print("Initializing seed ....")

        seed = {}
        for x in range(0, seed_count):
            g = m.randomGuess()
            r = self.request(levelurl, method='POST', data={'guess':g})
            if('error' in r and r['error']):
                r = self.request(levelurl, method='GET')
                continue

            print(str(g)+" : " + str(r['response']))
            seed[tuple(g)] = tuple(r['response'])

        print(".... Seed Complete")
        print("---------------------------------------------------------")
        return seed
        
    
    def zeroGuesser(self, m, goal, limit):
    ### solver that attempts to reduce the number space by guessing
    ### for [0,0]s first before solving as normal
        levelurl = self.BASE_URL + '/level/' + str(self.level) + '/'
        done = 0
        while done < goal:
            g = m.randomGuess()
            print(g)
            r = self.request(levelurl, method='POST', data={'guess':g})            
            if ('response' in r and tuple(r['response'])) == (0,0):
                print("FOUND ZERO GUESS- REDUCING GUESS SPACE")
                m.reduceGuessSpace(g)
                print(m.getGuessSpace())
                print("Number of guesses left :"+str(m.getNumberOfGuesses()))                
                done += 1
                
            elif('error' in r and r['error'] == self.TOO_MANY_GUESSES):
                print("OUT OF GUESSES- RESTARTING LEVEL\n")
                return 0
                
            elif('error' in r and r['error'] == self.TOOK_TOO_LONG):
                print("GUESS TOOK TOO LONG- RESTARTING LEVEL\n")
                return 0
                
            elif('message' in r and r['message'] == self.NEXT_LEVEL):
                print(" >>> LEVEL WON! Onto the next. <<< ")
                return goal

            else:
                print("Number of guesses left :"+str(m.getNumberOfGuesses()))                
                print(r)

        print("Found "+ str(done) +" zeroes this time")
        return done
        
    def basicSolve(self, m):
    ### basic solver for small values of r and t ###

        levelurl = self.BASE_URL + '/level/' + str(self.level) + '/'

        seed = self.seedGen(m, levelurl);
        m.genTable(seed)

        win = False
        res = None

        while win == False:
            g = m.nextGuess(res)
            print("TRYING GUESS: "+str(g))        
            r = self.request(levelurl, method='POST', data=g)

            if('error' in r and r['error'] == self.TOO_MANY_GUESSES):
                print("OUT OF GUESSES- RESTARTING LEVEL\n")
                return False
                
            elif('error' in r and r['error'] == self.TOOK_TOO_LONG):
                print("GUESS TOOK TOO LONG- RESTARTING LEVEL\n")
                return False
                
            elif('message' in r and r['message'] == self.NEXT_LEVEL):
                print(" >>> LEVEL WON! Onto the next. <<< ")
                return True

            elif('roundsLeft' in r):
                print(" >>> ROUND WON! "+str(r['roundsLeft'])+" left to go. <<< ")
                print(" ------------------------------------------------------- ")
                return True
                
            else:
                print(r)
                res = tuple(r['response'])


    def run(self):
    ### the main runner ##

        while(self.level < 7):
            r = self.resumeLevel()
            rounds = r['numRounds']

            print("\n=========================================================")
            print("======================== LEVEL "+str(self.level)+" ========================")
            print("GLADIATORS: %s\nWEAPONS: %s\nGUESSES: %s\nROUNDS: %s"
                  % (r['numGladiators'], r['numWeapons'], r['numGuesses'], r['numRounds'])
                  )
            print("---------------------------------------------------------")                            
    
            basic = True if r['numWeapons'] < 20 else False
            m = Mastermind.Mastermind(r['numGladiators'], r['numWeapons'], r['numGuesses'])
            
            if basic == False: 
                print("ADVANCED SOLVE ACTIVATE")
                got = self.zeroGuesser(m, 2, 0)
                if got != 2:
                    continue

            while (rounds > 0):
                if self.basicSolve(m):
                    rounds -= 1
                    r = self.resumeLevel()                    
                    m = Mastermind.Mastermind(r['numGladiators'], r['numWeapons'], r['numGuesses'])
                else:
                    break

            if rounds == 0:
                self.level += 1


def main():
    ms = MastermindSolver()
    if len(sys.argv) > 1:
        if sys.argv[1] == 'reset':
            ms.reset()
        
    ms.run()


if __name__ == "__main__":
    main()
