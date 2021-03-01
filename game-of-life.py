#!/usr/bin python

import random
import time
# Class definitions

class Endgame(Exception):
    def __init__(self, e=None):
        pass

class Cell:
    def __init__(self, y, x):
        self.Log = []
        if random.randint(0,10) == 1:
            self.setAlive()
        else:
            self.setDead()
        self.X = x
        self.Y = y

    def setAlive(self):
        self.alive = True
        self.Log.append("Set alive.")

    def setDead(self):
        self.alive = False
        self.Log.append("Set dead.")

    def printStatus(self):
        if self.alive == True:
            return("#")
        elif self.alive == False:
            return("-")

    def add_log(self, stringtoadd):
        self.Log.append(str(stringtoadd))

    def printLog(self):
        for iter in range(len(self.Log)):
            print(f"{iter}:{self.Log[iter]}")


class Board:
    def __init__(self):
        self.xrange = 5
        self.yrange = 5
        self.Board = []

    def BoardSetup(self):
        for y_iter in range(self.yrange):
            Row = []
            for x_iter in range(self.xrange):
                Row.append(Cell(y_iter,x_iter)) # remember to call class instance
            self.Board.append(Row)


    def printBoard(self):
        time.sleep(0.02)
        print(chr(27) + "[2J")
        for x in range(self.xrange):
            if len(str(x)) == 1:
                prepend = " "
                print(f"{prepend}{x}",end="")
            else:
                print(x,end=" ")
        print("x")
        for Row in self.Board:
            print (self.Board.index(Row),end="")
            for Col in Row:
                print(Col.printStatus(), sep=" ", end=" ")
            print()


    def resolveNextDoors(self,Row,Col) -> list:
        NextDoors = []
        NextDoorOpts = [(0,-1), (-1,-1), (-1,0), (-1,1), (0,1), (1,1), (1,0), (1,-1)]
        for NextDoorOpt in NextDoorOpts:
            NDoorRow = Row+NextDoorOpt[0]
            NDoorCol = Col+NextDoorOpt[1]
            # Stack overflow
            if NDoorRow > self.yrange - 1:
                NDoorRow = 0
            if NDoorCol > self.xrange - 1:
                NDoorCol = 0
            # Stack underflow
            if NDoorCol < 0:
                NDoorCol = self.xrange - 1
            if NDoorRow < 0:
                NDoorRow = self.yrange - 1
            NextDoors.append([NDoorRow,NDoorCol])
        return NextDoors


    def DoMate(self, HostCell, PartnerCell):
        #Find empty next-door, and set it to "alive"
        PotentialSpawnCells = []
        TurnBabies = []
        for coord in self.resolveNextDoors(HostCell.Y, HostCell.X):
            if self.Board[coord[0]][coord[1]].alive == False:
                PotentialSpawnCells.append(coord)
        if len(PotentialSpawnCells) == 0:
            return []
        else:
            random_coord = random.choice(PotentialSpawnCells)
    #        print((HostCell.Y, HostCell.X), PotentialSpawnCells)
            NewSpawn = Cell(random_coord[0],random_coord[1])
            NewSpawn.setAlive()
            NewSpawn.add_log(f"New spawn, born of {HostCell.Y},{HostCell.X} and {PartnerCell.Y},{PartnerCell.X}.")
            TurnBabies.append(NewSpawn)
        return(TurnBabies)

    def PopulateBoard(self,TurnBabies):
        if len(TurnBabies) != 0:
            for Baby in TurnBabies:
                self.Board[Baby.Y][Baby.X] = Baby


    def advanceTurn(self):
        for Row in range(self.yrange):
            for Col in range(self.xrange):
                needToPopulate = False
                # Do edge wraparound
                # Check if a partner exists.


                if self.Board[Row][Col].alive == True:
                    NextDoors = self.resolveNextDoors(Row,Col)
                    for NextDoor in NextDoors:
                        if self.Board[NextDoor[0]][NextDoor[1]].alive == True:
                            TurnBabies = self.DoMate(self.Board[Row][Col], self.Board[NextDoor[0]][NextDoor[1]])
                            #print(f"Y:{Row},X:{Col} could (w/ consent) mate with Y:{NextDoor[0]},X:{NextDoor[1]}.")
                            needToPopulate = True
                            break
        if needToPopulate == True:
            self.PopulateBoard(TurnBabies)
        else:
            raise Endgame("Motherfucker, we're done here.")
        self.printBoard()


# Global functions definitions
def main():
    GameBoard = Board()
    GameBoard.BoardSetup()
    GameBoard.printBoard()
    while True:
        GameBoard.advanceTurn()

# Runtime
if __name__ == "__main__":
    main()
