import itertools, random
# beep boop I am programming

class Mastermind:
    def __init__(self, r, t):
        # r = glads; t = weaps
        self.r = r
        self.t = t
        self.table = {}
        self.guess = tuple(i for i in range(0, r))


    def randomGuess(self):
        return random.sample(set(range(0, self.t)), self.r)
        
    def getGuess(self):
        g = self.guess
        self.guess = self.randomGuess() # just gonna do random for now?
        return {'guess': list(self.guess)}

    def next(self):
        # what's the next best guess? how do we determine that? try random for now
        pass

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

        
    def genTable(self):
        keys = list(itertools.permutations(range(0, self.t), self.r))
        for i in keys:
            self.table[i] = {}
            for j in keys:
                self.table[i][j] = {j : self.matchRes(i, j)}

    
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
