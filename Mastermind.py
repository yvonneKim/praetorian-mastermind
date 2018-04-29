import itertools, random
# beep boop I am programming

class Mastermind:
    def __init__(self, r, t, g, res=None):
        self.MAX_PERMS = 2000000
        # r = glads; t = weaps
        self.r = r
        self.t = t
        self.g = g
        self.table = {}
        self.guess = tuple(i for i in range(0, r)) # default guess
        self.guessSpace = set(range(0, self.t))

        # calculates set of all possible response tuples
        self.resRange = {x for x in itertools.product(range(0, r+1), repeat=2) if x[1] <= x[0]}

    def getNumberOfGuesses(self):
        return self.g

    def getNumberOfGladiators(self):
        return self.r

    def getNumberOfWeapons(self):
        return self.t

    def getGuessSpace(self):
        return self.guessSpace

    def reduceGuessSpace(self, s):
        self.guessSpace = self.guessSpace.difference(s)

    def reduceTable(self, r):
        # reduces the table as guesses are made. Called in nextGuess()
        # uses self.guess for the last guess, response param r (i,j)
        t = self.table
        remove = []
        for k in t:
            for g in t[k]:
                if g == self.guess:
                    if t[k][g] != r:
                        remove.append(k)

        for r in remove:
            if r in t:
                del t[r]

        
    def randomGuess(self):
        self.g -= 1
        return random.sample(self.guessSpace, self.r)

    
    def nextGuess(self, res=None):
        # takes in tuple res that represents the response
        # (i, j) where i is # matches, j is # that match position as well
        # if res is None, means first guess, just return defaulto
        
        if res != None:
            self.reduceTable(res)            

        t = self.table
        if len(t) == 1:
            self.guess = list(t.keys())[0]
            return {'guess': self.guess}
            
        keepers = []
        maxSet = set()
        for g in list(t.values())[0]:
            s = set()
            for k in t:
                s.add(t[k][g])
            if s.intersection(self.resRange) >= maxSet:
                maxSet = s
                keepers.append(g)
        self.guess = random.choice(keepers)
        self.g -= 1
        
        return {'guess': list(self.guess)}

    
    def matchRes(self, i, j):
        # takes in two tuples and returns tuple (x , y) where
        # x is # that match, y is # of those matches that also match
        # the position.

        x = 0
        y = 0
        for index, elem in enumerate(i):
            if elem in j:
                x += 1
                if j[index] == elem:
                    y += 1

        return (x, y)

        
    def genTable(self, seed=None):
        # if given a seed, which is dict of guess, res pairs,
        # will initialize the table given the seed
        if seed is None:
            keys = list(itertools.permutations(self.guessSpace, self.r))
            for i in keys:
                self.table[i] = {}
                for j in keys:
                    self.table[i][j] = self.matchRes(i, j)

        else:
            all_keys = list(itertools.permutations(self.guessSpace, self.r))                
            keys = list(itertools.permutations(self.guessSpace, self.r))
                
            print("Initial key table size is "+str(len(keys)))
            
            for k in seed.keys():
                keys = [x for x in keys if self.matchRes(x, k) == seed[k]]
                print(" ... reduced to "+str(len(keys)))

            for i in keys:
                self.table[i] = {}
                for j in all_keys:
                    self.table[i][j] = self.matchRes(i, j)

        print("Final key table size is: "+str(len(self.table)))
        print("---------------------------------------------------------")
        
        
if __name__=="__main__":
    m = Mastermind(4, 6)
    m.genTable()
    print(m)
