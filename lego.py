import random
import sys
import copy
import gui
import time
import threading

# Define the size of the boards
N = 10
# Define the size of the population : must be an even number
P = 100


def main():

    # Redirect standard output to file (created in project directory). Save original channel to restore.
    oldstdout = sys.stdout
    sys.stdout = open('Lego_Output.txt', 'w')

    # Create the population and start the breeding process
    population = Population()

    # Show the result board in another thread (interferes with the printing)
    gui_thread = threading.Thread(target=gui.gui(population.resultBoard))
    gui_thread.start()

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
    def drawA(self, i, j, indicator):
        if indicator == 1:
            # Draw
            return Board.drawBrick(self, i, j, 1, 1, 'a')
        else:
            # Erase
            return Board.drawBrick(self, i, j, 1, 1, '')

    # Draws a three dots brick:     [...]
    def drawB(self, i, j, indicator):
        if indicator == 1:
            # Draw
            # Check if the brick can fit in this position (not too close to the end of the row)
            if j < N-2:
                return Board.drawBrick(self, i, j, 1, 3, 'b')
            else:
                return -1
        else:
            # Erase
            return Board.drawBrick(self, i, j, 1, 3, '')

    # Draws a six dots brick:       [:::]
    def drawC(self, i, j, indicator):
        if indicator == 1:
            # Draw
            # Check if the brick can fit in this position (not too close to the end of the row, and not in the last row)
            if j < N-2 and i < N-1:
                return Board.drawBrick(self, i, j, 2, 3, 'c')
            else:
                return -1
        else:
            # Erase
            return Board.drawBrick(self, i, j, 2, 3, '')

    # Draws a two dots brick:     [..]
    def drawD(self, i, j, indicator):
        if indicator == 1:
            # Draw
            # Check if the brick can fit in this position (not too close to the end of the row)
            if j < N-1:
                return Board.drawBrick(self, i, j, 1, 2, 'd')
            else:
                return -1
        else:
            # Erase
            return Board.drawBrick(self, i, j, 1, 2, '')

    # Draws a four dots brick:       [::]
    def drawE(self, i, j, indicator):
        if indicator == 1:
            # Draw
            # Check if the brick can fit in this position (not too close to the end of the row, and not in the last row)
            if j < N-1 and i < N-1:
                return Board.drawBrick(self, i, j, 2, 2, 'e')
            else:
                return -1
        else:
            # Erase
            return Board.drawBrick(self, i, j, 2, 2, '')

    # Draws a four dots brick:     [....]
    def drawF(self, i, j, indicator):
        if indicator == 1:
            # Draw
            # Check if the brick can fit in this position (not too close to the end of the row)
            if j < N-3:
                return Board.drawBrick(self, i, j, 1, 4, 'f')
            else:
                return -1
        else:
            # Erase
            return Board.drawBrick(self, i, j, 1, 4, '')

    # Draws a brick at a given starting point, if not occupied. Also gets: length, width, and brick type
    # Types a, b, c... are bricks, and '""' (empty string) means deletion
    def drawBrick(self, startX, startY, lengthX, widthY, type):
        # Draw the brick:
        if type != "":
            # Check:
            for row in range(startX, startX + lengthX):
                for column in range(startY, startY + widthY):
                    if self.board[row][column] != '':
                        return -1
            # Draw:
            k = 1
            for row in range(startX, startX + lengthX):
                for column in range(startY, startY + widthY):
                    self.board[row][column] = type + str(k)
                    k += 1
            return 1

        # Erase the brick:
        else:
            # Erase:
            for row in range(startX, startX + lengthX):
                for column in range(startY, startY + widthY):
                    self.board[row][column] = ""
            return 1

    # Calculate the fitting function:
    # -1 for an empty cell, +2 for occupied cell, +5 for occupied cell at the sides
    def fittingFunction(self):
        self.capacity = 0
        fitness = 0
        fullSequency = 0

        for row in range(N):
            for column in range(N):
                if self.board[row][column] == "":
                    fullSequency -= 1
                if self.board[row][column] != "":
                    self.capacity += 1
                    fullSequency += 2
                    fitness += fullSequency
                if (column == 0 or column == (N-1)) and (self.board[row][column] != ""):
                    fitness += 5
        return fitness

    # Generate a random mutation at a random position in a board
    # Erase the brick if the position is occupied, or try to draw a random brick if it isn't
    def mutation(self):
        # Generate a random to decide whether the mutation will happen at all - odds are 1:100
        if random.randint(0, (P*P)/2) == 1:

            # Choose some random position on the board
            randY = random.randint(0, N - 1)
            randX = random.randint(0, N - 1)

            if self.board[randY][randX] == "":
                # Call a random function from the drawing functions
                randFunc = random.randint(0, 5)
                # The position is not occupied -> try to draw a random brick
                if 1 == Board.drawingFunctions[randFunc](self, randY, randX, 1):
                    return [1, randY, randX, self.board[randY][randX]]

            else:
                # The position is occupied:
                # Find the starting position of the brick that occupies that position
                str = self.board[randY][randX]
                startY = randY
                startX = randX

                # Move to the left while the brick isn't over
                # AND the brick's type stays the same (not to get to a brick of a different type)
                # AND the position number gets smaller (prevents getting to a different brick of the same type)
                while self.board[startY][startX-1] != "" and self.board[startY][startX-1][:-1] == str[:-1] and int((self.board[startY][startX-1])[-1:]) < int(str[-1:]):
                    startX -= 1
                # If needed, jump lines up untill reaching the first position in the brick
                while int(self.board[startY][startX][-1:]) != 1:
                    startY -= 1

                # Subtract the ASCII values to get the correct drawing (erasing, actually) function
                specificFunc = ord(str[:-1]) - ord('a')

                # Erase the brick that starts at the found position
                if 1 == Board.drawingFunctions[specificFunc](self, startY , startX, -1):
                    return [2, startY, startX]

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
        print("Board's capacity is {0}% ".format(self.capacity*100/(N*N)))

    # Set a list of the possible drawing functions
    drawingFunctions = []
    drawingFunctions.insert(0, drawA)
    drawingFunctions.insert(1, drawB)
    drawingFunctions.insert(2, drawC)
    drawingFunctions.insert(3, drawD)
    drawingFunctions.insert(4, drawE)
    drawingFunctions.insert(5, drawF)


# A population of random lego boards
class Population:

    population = None
    fittingSum = 0
    generation = 0
    resultBoard = None

    def __init__(self):

        self.population = []
        # Create an array of 'Board' objects that will be the population
        print("The random initial population contains " + str(P) + " boards:")
        for individual in range(P):
            print("\nBoard #" + str(individual + 1) + ":")
            # Create a new board
            new_board = Board()

            # Fill the new board with random bricks:
            # For random amount of bricks in this board (1-10)
            for index in range(random.randint(5, 60)):
                # Call a random function from the drawing functions, for some random position on the board
                randFunc = random.randint(0, 5)
                randY = random.randint(0, N-1)
                randX = random.randint(0, N-1)
                Board.drawingFunctions[randFunc](new_board, randY, randX, 1)
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
                fitnum = self.population[i].fittingFunction()
                self.fittingSum += fitnum
            print("The average fitting value of the population is: " + str(self.fittingSum/P))
            if prevFittingSum == self.fittingSum:
                noProgressTimes += 1
            else:
                noProgressTimes = 0
            if noProgressTimes > 100:
                # choose the best board
                self.population.sort(key=lambda x: x.fittingFunction(), reverse=True)
                print("\nBoard with the best fitness is: \n")
                self.population[0].printBoard()
                self.resultBoard = self.population[0]
                break


    def chooseRandomlyParent(self):
        parent = self.population[random.randint(0, len(self.population) - 1)]
        self.population.remove(parent)
        return parent

    def checkFullParts(self, i, j, parent):
        for index in range(j):
            # add here all elements that have more than one row
            if parent.board[i][index] == 'c1' or parent.board[i][index] == 'e1':
                return False
        for index in range(j, N):
            if parent.board[i][index] == 'c4'or parent.board[i][index] == 'e3':
                return False
        return True

    def checkCrossoverLegalitty(self, randX, randY, parent):
        if (parent.board[randX][randY] == '' or
                parent.board[randX][randY] == 'a1' or
                parent.board[randX][randY] == 'b1' or
                parent.board[randX][randY] == 'c1' or
                parent.board[randX][randY] == 'd1' or
                parent.board[randX][randY] == 'e1' or
                parent.board[randX][randY] == 'f1'):
            if self.checkFullParts(randX, randY, parent):
                return True
        return False

    def concatChromosomeParts(self, randX, randY, child, parent):
        for j in range(randY, N):
            child[randX][j] = parent[randX][j]
        if (randX + 1) <= N:
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
                # Create first child
                childA.board = self.concatChromosomeParts(randX, randY, childA.board, father.board)
                childA.fittingFunction()

                # Send new child to (possibly) mutate
                mutationResult = childA.mutation()
                if mutationResult is not None:
                    strToPrint = "Child was mutated at row " + str(mutationResult[1] + 1) + " column " + str(mutationResult[2] + 1) + " - "
                    if mutationResult[0] == 1:
                        strToPrint += "Brick of type " + str(mutationResult[3][:-1]).upper() + " was added"
                    else:
                        strToPrint += "Brick was taken out:"
                    print(strToPrint)
                    childA.printBoard()

                # Create second child
                childB.board = self.concatChromosomeParts(randX, randY, childB.board, mother.board)
                childB.fittingFunction()

                # Send new child to (possibly) mutate
                mutationResult = childB.mutation()
                if mutationResult is not None:
                    strToPrint = "Child was mutated at row " + str(mutationResult[1] + 1) + " column " + str(mutationResult[2] + 1) + " - "
                    if mutationResult[0] == 1:
                        strToPrint += "Brick of type " + str(mutationResult[3][:-1]).upper() + " was added"
                    else:
                        strToPrint += "Brick was taken out:"
                    print(strToPrint)
                    childA.printBoard()

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
