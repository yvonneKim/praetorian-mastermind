import itertools, random
# beep boop I am programming

class Mastermind:
    def __init__(self, r, t, res=None):
        # r = glads; t = weaps
        self.r = r
        self.t = t
        self.table = {}
        self.guess = tuple(i for i in range(0, r)) # default guess

        # given res param, inits with default table for that res
        # the default table is for the default guess [0, 1, 2, ...]
        self.genTable(res)

        # calculates set of all possible response tuples
        self.resRange = {x for x in itertools.product(range(0, r+1), repeat=2) if x[1] <= x[0]}

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
        # if given a seed, which is a response tuple for a default guess,
        # will initialize the table given the seed
        assert seed is None
        
        if seed is None:
            keys = list(itertools.permutations(range(0, self.t), self.r))
            for i in keys:
                self.table[i] = {}
                for j in keys:
                    self.table[i][j] = self.matchRes(i, j)

        else:
            keys = list(itertools.permutations(range(0, self.t), self.r))
            for i in keys:
                if self.matchRes(i, self.guess) == seed:
                    self.table[i] = {}
                    for j in keys:
                        self.table[i][j] = self.matchRes(i, j)

        print("size of the generated table is: "+str(len(self.table)))
                    
                    
    def __str__(self):

        s = "       "
        for i in self.table:
            s += str(i) + " "
        s += "\n===================================================================================================================================\n"
        
        for i in self.table:
            s += str(i) + " || "
            for j in self.table[i]:
                s += str(self.table[i][j]) + " | "
            s += "\n-------------------------------------------------------------------------------------------------------------------------------\n"
                
        return s


if __name__=="__main__":
    m = Mastermind(4, 6)
    m.genTable()
    print(m)
