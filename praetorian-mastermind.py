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
            print("TABLE STATE: "+str(guesser))
            print("TRYING GUESS: "+str(g))
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
# for now, works only with level 1 parameters
class Guesser:
    def __init__(self, j):
        self.gl = j['numGladiators']
        self.gs = j['numGuesses']
        self.rn = j['numRounds']
        self.wp = j['numWeapons']

        # guess table keeps track of possibilities for each num's position
        # each column is for each "weapon" number. it's rows have position numbers
        # that are crossed off as we eliminate. -1 indicates a non-match.
        #
        #     -wp->
        # |   0 , 1 , 2 , 3 , 4 , 5
        # gl -----------------------
        # v  -1  -1  -1  -1  -1  -1  [0]
        #     0   0   0   0   0   0  [1]
        #     1   1   1   1   1   1  [2]
        #     2   2   2   2   2   2  [3]
        #     3   3   3   3   3   3  [4]
        #
        # as we eliminate each number's possible positions, replace with "x"s.
        # NOTE: the __str__() output of this table switches the axis :^/

        self.gs_table = [[y-1 for y in range(self.gl+1)] for x in range(self.wp)]        
        
    def __str__(self):
        out = "\n"
        i = 0
        for col in self.gs_table:
            out += str(i)+" | "
            i += 1
            for val in col:
                out += str(val)+" "
            out += '\n'
        return out
        
    def next(self):
        # returns next guess (as dict, to be json-ified) from the last
        # state of the gs_table
        # first time running next() gives a defaulto [0, 1, 2, 3] guess

        
        return {'guess':[0,1,2,3]}

    
def main():
    run(authenticate())

if __name__ == "__main__":
    main()
