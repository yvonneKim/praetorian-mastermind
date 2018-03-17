import itertools, random
# beep boop I am programming

class Mastermind:
    def __init__(self, r, t):
        # r = glads; t = weaps
        self.r = r
        self.t = t
        self.table = {}
        self.guess = tuple(i for i in range(0, r)) 


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

        print("REMOVE LIST SIZE : "+str(len(remove)))
        for r in remove:
            if r in t:
                del t[r]

        print("TABLE SIZE NOW : "+str(len(self.table)))

                
        
    def randomGuess(self):
        return random.sample(set(range(0, self.t)), self.r)

    def nextGuess(self, res):
        # takes in tuple res that represents the response
        # (i, j) where i is # matches, j is # that match position as well
        # if res is (-1, -1), means first guess, just return defaulto
        
        if res[0] == -1:
            return {'guess': list(self.guess)}

        self.reduceTable(res)
        self.guess = self.randomGuess() # change this 
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

        
    def genTable(self):
        keys = list(itertools.permutations(range(0, self.t), self.r))
        for i in keys:
            self.table[i] = {}
            for j in keys:
                self.table[i][j] = self.matchRes(i, j)

    
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
