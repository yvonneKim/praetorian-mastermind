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

        # calculates set of all possible response tuples
        self.resRange = {x for x in itertools.product(range(0, r+1), repeat=2) if x[1] <= x[0]}

    def getNumberOfGuesses(self):
        return self.g

    def reduceTable(self, r):
        # reduces the table as guesses are made. Called in nextGuess()
        # uses self.guess for the last guess, response param r (i,j)
        t = self.table
        remove = []
        for k in t:
            for g in t[k]:
                if g == self.guess:
#                    print("RESPONSE for key: "+str(k)+", guess: "+str(g)+" is "+str(t[k][g]))
                    if t[k][g] != r:
#                        print("DOES NOT MATCH "+str(r)+"- MOVING KEY "+str(k)+" TO REMOVE!")
                        remove.append(k)

#        print("REMOVE LIST SIZE : "+str(len(remove)))
        for r in remove:
            if r in t:
                del t[r]

#        print("TABLE SIZE NOW : "+str(len(self.table)))
                
        
    def randomGuess(self):
        return random.sample(set(range(0, self.t)), self.r)

    def nextGuess(self, res=None):
        # takes in tuple res that represents the response
        # (i, j) where i is # matches, j is # that match position as well
        # if res is (-1, -1), means first guess, just return defaulto
        
        if res == None:
            return {'guess': list(self.guess)}

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
#            print(s)
            if s.intersection(self.resRange) >= maxSet:
                maxSet = s
#                print("adding another to keepers: "+str(g))
                keepers.append(g)
        self.guess = random.choice(keepers)
        
#        self.guess = self.randomGuess() # change this 
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
            keys = list(itertools.permutations(range(0, self.t), self.r))
            for i in keys:
                self.table[i] = {}
                for j in keys:
                    self.table[i][j] = self.matchRes(i, j)

        else:

            if self.t > 10 and self.r > 5: # if it's outrageously large
                all_keys = list(itertools.islice(itertools.permutations(range(0, self.t), self.r), self.MAX_PERMS))
                keys = list(itertools.islice(itertools.permutations(range(0, self.t), self.r), self.MAX_PERMS))
            else:
                all_keys = list(itertools.permutations(range(0, self.t), self.r))                
                keys = list(itertools.permutations(range(0, self.t), self.r))
                
            print("Initial key table size is "+str(len(keys)))
            
            for k in seed.keys():
                keys = [x for x in keys if self.matchRes(x, k) == seed[k]]
                if len(keys) == 0: # got the wrong batch of perms to try
                    return False
                print(" ... reduced to "+str(len(keys)))

            for i in keys:
                self.table[i] = {}
                for j in all_keys:
                    self.table[i][j] = self.matchRes(i, j)

        print("Final key table size is: "+str(len(self.table)))

        
if __name__=="__main__":
    m = Mastermind(4, 6)
    m.genTable()
    print(m)
