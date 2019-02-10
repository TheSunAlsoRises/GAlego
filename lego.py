import random
import sys
import copy

# Define the size of the boards
N = 10
# Define the size of the population : must be an even number
P = 200


def main():

    # Redirect standard output to file (created in project directory). Save original channel to restore.
    oldstdout = sys.stdout
    sys.stdout = open('Lego_Output.txt', 'w')

    # Create the population and start the breeding process
    Population()

    # Restore standard output to screen
    sys.stdout = oldstdout
    exit()


# A lego board of size NxN
# All the methods below work on a SINGLE object of 'Board' class
class Board:

    board = None
    capacity = 0

    # Constructor:
    def __init__(self):
        self.board = []
        # Create a 2 dimensional array of NxN cells
        for row in range(N):
            # Add an empty array that will hold each cell in this row
            self.board.append([])
            for column in range(N):
                # Append an empty cell
                self.board[row].append("")

    # Draws a single dot brick:     [.]
    def drawA(self, i, j):
        Board.drawBrick(self, i, j, 1, 1, 'a')

    # Draws a three dots brick:     [...]
    def drawB(self, i, j):
        # Check if the brick can fit in this position (not too close to the end of the row)
        if j < N-2:
            Board.drawBrick(self, i, j, 1, 3, 'b')
        else:
            return -1

    # Draws a six dots brick:       [:::]
    def drawC(self, i, j):
        # Check if the brick can fit in this position (not too close to the end of the row, and not in the last row)
        if j < N-2 and i < N-1:
            Board.drawBrick(self, i, j, 2, 3, 'c')
        else:
            return -1

    # Draws a brick at a given starting point, if not occupied. Also gets: length, width, and brick type
    # Types a, b, c... are bricks, and '""' (empty string) means deletion
    def drawBrick(self, startX, startY, lengthX, widthY, type):
        # Check:
        for row in range(startX, startX + lengthX):
            for column in range(startY, startY + widthY):
                if self.board[row][column] != '':
                    return -1
        # Draw:
        if type != "":
            k = 1
        else:
            k = ""
        for row in range(startX, startX + lengthX):
            for column in range(startY, startY + widthY):
                self.board[row][column] = type + str(k)
                if k != "":
                    k += 1

    # Calculate the fitting function: the number of occupied cells in the board
    def fittingFunction(self):
        self.capacity = 0
        for row in range(N):
            for column in range(N):
                if self.board[row][column] != "":
                    self.capacity += 1
        return self.capacity

    def printBoard(self):
        boardString = ""
        for row in range(N):
            for column in range(N):
                if self.board[row][column] == '':
                    boardString += '--'
                else:
                    boardString += self.board[row][column]
            boardString += '\n'

        # Cut the last'\n'
        boardString = boardString[:-1]
        print(boardString)
        print("Board's fitting function value: "+ str(self.capacity))


# A population of random lego boards
class Population:

    population = None
    drawingFunctions = None
    fittingSum = 0
    generation = 0

    def __init__(self):
        # Set a list of the possible drawing functions
        self.drawingFunctions = []
        self.drawingFunctions.insert(0, Board.drawA)
        self.drawingFunctions.insert(1, Board.drawB)
        self.drawingFunctions.insert(2, Board.drawC)

        self.population = []
        # Create an array of 'Board' objects that will be the population
        print("The random initial population contains " + str(P) + " boards:")
        for individual in range(P):
            print("\nBoard #" + str(individual + 1) + ":")
            # Create a new board
            new_board = Board()

            # Fill the new board with random bricks:
            # For random amount of bricks in this board (1-10)
            for index in range(random.randint(3, 10)):
                # Call a random function from the drawing functions, for some random position on the board
                randFunc = random.randint(0, 2)
                randX = random.randint(0, N-1)
                randY = random.randint(0, N-1)
                self.drawingFunctions[randFunc](new_board, randX, randY)
            # Apply the fitting function to check the board's capacity
            # And sum it for the value of the whole population
            self.fittingSum += new_board.fittingFunction()
            new_board.printBoard()

            # Append the board to the population
            self.population.append(new_board)

        print("The total fitting value of the population is: " + str(self.fittingSum))

        noProgressTimes = 0
        while True:
            self.generation += 1
            print("Generation: {0}".format(self.generation))
            self.population = self.crossover()
            prevFittingSum = self.fittingSum
            self.fittingSum = 0
            for i in range(P):
                print("Board #{0}".format(i+1))
                self.population[i].printBoard()
                self.fittingSum += self.population[i].fittingFunction()
            print("The total fitting value of the population is: " + str(self.fittingSum))
            if prevFittingSum == self.fittingSum:
                noProgressTimes += 1
            else:
                noProgressTimes = 0
            if noProgressTimes > 50:
                # choose the best board
                self.population.sort(key=lambda x: x.fittingFunction(), reverse=True)
                print("Board with the best fitness is: \n")
                self.population[0].printBoard()
                break


    def chooseRandomlyParent(self):
        parent = self.population[random.randint(0, len(self.population) - 1)]
        self.population.remove(parent)
        return parent

    def checkFullParts(self, i, j, parent):
        for index in range(j):
            # add here all elements that have more than one row
            if (parent.board[i][index] == 'c1'):
                return False
        for index in range(j, N):
            if (parent.board[i][index] == 'c4'):
                return False
        return True

    def checkCrossoverLegalitty(self, randX, randY, parent):
        if (parent.board[randX][randY] == '' or
                parent.board[randX][randY] == 'a1' or
                parent.board[randX][randY] == 'b1' or
                parent.board[randX][randY] == 'c1'):
            if (self.checkFullParts(randX, randY, parent)):
                return True
        return False

    def concatChromosomeParts(self, randX, randY, child, parent):
        for j in range(randY, N):
            child[randX][j] = parent[randX][j]
        if ((randX + 1) <= N):
            for i in range(randX + 1, N):
                for j in range(N):
                    child[i][j] = parent[i][j]
        return child

    def crossover(self):
        nextGeneration = []
        for i in range(int(P / 2)):
            mother = self.chooseRandomlyParent()
            father = self.chooseRandomlyParent()
            # choose randomly crossover
            randX = random.randint(0, N-1)
            randY = random.randint(0, N-1)
            childA = copy.deepcopy(mother)
            childB = copy.deepcopy(father)
            # check if the crossover is legal for both parents create new children, else take the parents
            if self.checkCrossoverLegalitty(randX, randY, mother) and self.checkCrossoverLegalitty(randX, randY,father):
                childA.board = self.concatChromosomeParts(randX, randY, childA.board, father.board)
                childA.fittingFunction()
                childB.board = self.concatChromosomeParts(randX, randY, childB.board, mother.board)
                childB.fittingFunction()

                # after sort indexes 0,1 will contain participants with highest fitness
                bestFittnes = [mother, father, childA, childB]
                bestFittnes.sort(key=lambda x: x.fittingFunction(), reverse=True)

                # If the two chosen boards are exactly the same (can cause occupation of the population!),
                # take only one of the two-best and the best next one
                if bestFittnes[0].board != bestFittnes[1].board:
                    nextGeneration.append(bestFittnes[0])
                    nextGeneration.append(bestFittnes[1])

                elif bestFittnes[0].board != bestFittnes[2].board:
                    nextGeneration.append(bestFittnes[0])
                    nextGeneration.append(bestFittnes[2])
                else:
                    nextGeneration.append(bestFittnes[0])
                    nextGeneration.append(bestFittnes[3])

            # Couldn't crossover at all
            else:
                nextGeneration.append(mother)
                nextGeneration.append(father)

        return nextGeneration


# Upon run call 'main'
if __name__ == "__main__":
    main()
