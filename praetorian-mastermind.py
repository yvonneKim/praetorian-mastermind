import requests, json, sys, Mastermind

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

def reset(h):
    url = 'https://mastermind.praetorian.com/reset/'
    r = requests.post(url, headers=h)
    print(r.json())


def run(headers):
    h = headers
    level = 1

    while(level < 7):
        levelurl = 'https://mastermind.praetorian.com/level/'+str(level)+'/'
        r = requests.get(levelurl, headers=h)
        print("STARTING LEVEL "+str(level)+"\n")
        print(r.json())
        m = Mastermind.Mastermind(4, 6)
        m.genTable()

        win = False
        res = (-1, -1)
        while(win == False):
            g = m.nextGuess(res)
            print("TRYING GUESS: "+str(g))
            r = requests.post(levelurl, data=json.dumps(g), headers=h)
            print(r.json())
            if('message' in r.json()):
                win = True
            if('error' in r.json()): # means we're out of guesses...
                print("OUT OF GUESSES- RESTARTING LEVEL\n")
                break

            # else, it's just a regular response
            res = tuple(r.json()['response'])


def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == 'reset':
            reset(authenticate())
        
    run(authenticate())

if __name__ == "__main__":
    main()
