import galois
import time
import random
import numba
import numpy as np
from math import trunc
n = 10007 # 997 1009 10007 100003
queensum = n - 1
solve = []
mult_table = []
pickupQueens = {}
galois_inform = {
    "diag1" : [0]*(queensum*2-1),
    "diag2" : [0]*(queensum*2-1),
    "row" : [0]*queensum,
    "col" : [0]*queensum
}
row_conflicts = []      # Keeps track of row conflicts
diagr_conflicts = []    # Keeps track of right diagonal conflicts
diagl_conflicts = []    # Keeps track of left diagonal conflicts
board = []


'''

1. do galois field(n) 
O(n^2)
2. get n in the galois field table

3. do combination if it needed
尋找左上右下 對角線衝突 then pick 1
尋找左上右下 非對角線衝突 then pick 1
尋找右上左下衝突 then pick 1


4. find remain position


list = [ _, _, _, _, _]
if value == -1 => remain position
else col = value
'''


@numba.jit(nopython=True)
def get_mult_table(index):
    global n
    # mult_table = np.zeros((n, n), dtype=np.int64)
    mult_table = []
    for i in range(1,n):
        for j in range(1,n):
            temp = (i * j) % n
            if ( temp == index ) :
                mult_table.append(j-1)
                # mult_table[i, j] = temp
                # mult_table[i, j+1:] = -1
                break
    return mult_table

def check_diagonal_queens(lst):
    n = len(lst)
    cols = 0
    diag1 = 0
    diag2 = 0

    for i in range(n):
        if lst[i] != -1:
            col = lst[i]
            diag1_mask = 1 << (i + col)
            diag2_mask = 1 << (i - col + n - 1)

            if cols & (1 << col) or diag1 & diag1_mask or diag2 & diag2_mask:
                return True

            cols |= 1 << col
            diag1 |= diag1_mask
            diag2 |= diag2_mask

    return False




def find_empty_positions(queens) :
    global queensum
    col_pos = [True] * queensum
    row_pos = [True] * queensum
    diag1 = [True] * (queensum*2-1)
    diag2 = [True] * (queensum*2-1)

    for queen in queens :
        row, col = queen
        col_pos[col] = False
        row_pos[row] = False
        diag1[row + col] = False # 反斜
        diag2[row - col + (queensum-1)] = False # 斜線
    print("diag1", diag1)
    print("diag2", diag2)
    col_pos = [ index  for index,i in enumerate(col_pos) if i == True]
    row_pos = [index for index,i in enumerate(row_pos) if i == True]
    print(row_pos, col_pos)
    empty_position = []
    for row in row_pos :
        for col in col_pos :
            print()
            if ( diag1[row + col ] == False  ) :
                print("test", [row,col])
            elif ( diag2[row - col + (queensum-1)] ==  False) :
                print("test1", [row,col])
            else :
                empty_position.append([row,col])

    return empty_position




def get_Galois_position(n):
    global mult_table
    note_list = []
    for index,row in enumerate(mult_table):
        for index2,column in enumerate(row) :
            if index == 0 or index2 == 0 :
                pass
            elif str(n) == str(column) : # α + 1
                note_list.append(index2)

            
    return note_list

def initial_Galois_table( index ) :
    global n 
    global mult_table
    solve = []
    mult_table = []
    galois_inform = {
        "diag1" : [0]*(queensum*2-1),
        "diag2" : [0]*(queensum*2-1),
        "row" : [0]*queensum,
        "col" : [0]*queensum
    }
    pickupQueens = {}
    row_conflicts = []      # Keeps track of row conflicts
    diagr_conflicts = []    # Keeps track of right diagonal conflicts
    diagl_conflicts = []    # Keeps track of left diagonal conflicts
    board = []
    if n > 2 **20 :
        GF = galois.GF(int(n))
        print(GF.ufunc_mode)

        for i in range(1,n):
            for j in range(1,n):
                temp = GF(i)*GF(j)
                if ( temp == index ) :
                    mult_table.append(j-1)
                    break
    else :
        mult_table = get_mult_table(index)

def get_conflict_queens() :
    global galois_inform
    diag1 = []
    diag2 = []
    col = []
    row = []
    for index,i in enumerate(galois_inform["diag1"]) :
        if i > 1 :
            diag1.append((index,i))
    for index,i in enumerate(galois_inform["diag2"]) :
        if i > 1 :
            diag2.append((index,i))
    for index,i in enumerate(galois_inform["col"]) :
        if i > 1 :
            col.append((index,i))
    for index,i in enumerate(galois_inform["row"]) :
        if i > 1 :
            row.append((index,i))
            
    print( "diag1", diag1 )
    print( "diag2" ,diag2 )
    print( "col" ,col )
    print( "row", row )

def pick_queens() :
    global mult_table
    global galois_inform
    global queensum
    global pickupQueens
    diag1 = [0] * (queensum * 2 -1)
    diag2 = [0] * (queensum * 2 -1)
    col = [0] * queensum
    test_table = [(index,i) for index,i in enumerate(mult_table)]
    
    for _ in range(queensum) :
        random_choice = random.choice( test_table )
        test_table.remove(random_choice)
        row,column = random_choice[1],random_choice[0]
        
        diag1[row+column] += 1
        diag2[row-column+(queensum-1)] += 1
        col[column] += 1
        
        if diag1[row+column] < 2 and diag2[row-column + (queensum-1)] < 2 and col[column] < 2 :
            pickupQueens[column] = row
            

def initial_galois_inform() :
    global mult_table
    global galois_inform
    global queensum
    for index, i in enumerate(mult_table) :
        row, col = index, i
        galois_inform["col"][col] += 1
        galois_inform["row"][row] += 1
        galois_inform["diag1"][row + col] += 1 # 反斜
        galois_inform["diag2"][row - col + (queensum-1)] += 1 # 斜線

def changeConflicts(col, row, val):
    
    row_conflicts[row] += val
    diagr_conflicts[col + row] += val
    diagl_conflicts[col + (queensum - row - 1)] += val

# Finds the index of the best new queen position. Ties are broken randomly.
# Parameter: the current column index
def minConflictPos(col):
    global queensum
    minConflicts = queensum
    minConflictRows = []
    for row in range(queensum):
        # calculate the number of conflicts using the conflict arrays
        conflicts = row_conflicts[row] + diagr_conflicts[col + row] + diagl_conflicts[col + (queensum - row - 1)]
        # if there are no conflicts in a row, immediately return that row value
        if conflicts == 0:
            return row
        # if the number of conflicts is less, change it to the minConflicts value
        if conflicts < minConflicts:
            minConflictRows = [row]
            minConflicts = conflicts
        # if the number of conflicts is equal, append the index instead of changing it
        elif conflicts == minConflicts:
            minConflictRows.append(row)
    # randomly choose the index from the list of tied conflict values
    choice = random.choice(minConflictRows)
    return choice

def createBoard():
    global queensum
    global board
    global row_conflicts
    global diagr_conflicts
    global diagl_conflicts
    global mult_table
    global pickupQueens

    # Begin with an empty board
    board = []

    # Initialize the conflict arrays
    # The diagonal conflict lists are the size of the number of diagonals of the board
    diagr_conflicts = [0] * ((2 * queensum) - 1)
    diagl_conflicts = [0] * ((2 * queensum) - 1)
    row_conflicts = [0] * queensum

    # Create an ordered set of all possible row values
    rowSet = set(range(0,queensum))
    
    # Create a list to keep track of which queens have not been placed
    notPlaced = []
    # print(galois_inform["diag1"])
    test_num = 0
    for col in range(0, queensum):
        # Pop the next possible row location to test
        # Calculate the conflicts for potential location
        
        if pickupQueens.get(col) : # 14.XX
            testRow = pickupQueens[col]
            try :
                rowSet.remove(testRow)
            except :
                pass
        else:
            testRow = rowSet.pop()
        
        ##### pick half of mult_table 17.XX seconds
        # if col < len(mult_table)/2 :
            
        #     testRow = mult_table[col]
        #     try :
        #         rowSet.remove(testRow)
        #     except :
        #         pass
        # else :
        
        
        # pick up triangle 17.XX seconds -> 15.XX
        # if mult_table[col] >= col :
        #     testRow = mult_table[col]
        #     test_num += 1
        #     try :
        #         rowSet.remove(testRow)
        #     except :
        #         pass
        # else :
        #     testRow = rowSet.pop()
            
        
        
        # testRow = rowSet.pop()
        conflicts = row_conflicts[testRow] + diagr_conflicts[col + testRow] + diagl_conflicts[col + (queensum- testRow - 1)]
        # If there are no conflicts, place a queen in that location on the board
        if conflicts == 0:
            board.append(testRow)
            changeConflicts(col, board[col], 1)
        # If a conflict is found...
        else:
            # Place the potential row to the back of the set
            rowSet.add(testRow)
            # Take the next row from the set to test
            # testRow2 = rowSet.pop()
            testRow2 = random.choice(tuple(rowSet))
            rowSet.remove(testRow2)
            # Calculate the conflicts
            conflicts2 = row_conflicts[testRow2] + diagr_conflicts[col + testRow2] + diagl_conflicts[col + (queensum- testRow2 - 1)]
            # If there are no conflicts, place a queen in that location on the board
            if conflicts2 == 0:
                board.append(testRow2)
                changeConflicts(col, board[col], 1)
            else:
                # Otherwise, add the possible row back to the set
                rowSet.add(testRow2)
                # Add a None to the board to hold the place of the potential queen
                board.append(None)
                # Keep track of which column was not placed to be handled later
                notPlaced.append(col)
    print( "test_num", test_num )
    for col in notPlaced:
        # Place the remaining queen locations
        # board[col] = rowSet.pop()
        
        testRow2 = random.choice(tuple(rowSet))
        board[col] = testRow2
        rowSet.remove(testRow2)
        # Update the conflict lists
        changeConflicts(col, board[col], 1)
        
def findMaxConflictCol():
    global queensum
    conflicts = 0
    maxConflicts = 0
    maxConflictCols = []

    for col in range(0,queensum):
            # Determine the row value for the current column
            row = board[col]
            # Calculate the number of conflicts using the conflict lists
            conflicts = row_conflicts[row] + diagr_conflicts[col+row] + diagl_conflicts[col+(queensum-row-1)]
            # If conflicts are greater than the current max, make that column the maximum
            if (conflicts > maxConflicts):
                    maxConflictCols = [col]
                    maxConflicts = conflicts
            # If the conflicts equal the current max, append the index value to the maxConflictCols list
            elif conflicts == maxConflicts:
                    maxConflictCols.append(col)
    # Randomly choose from the list of tied maximums
    choice = random.choice(maxConflictCols)
    return choice, maxConflicts
        
def solveNQueens():
    global queensum
    global board
    testtime1 = time.time()
    createBoard()
    print( "CreateBoard time :", time.time() - testtime1 )
    iteration = 0
    maxIteration = 0.6 * queensum    # Define the maximum iterations as 0.6 * size of board

    while (iteration < maxIteration):
        # Calculate the maximum conflicting column and the number of conflicts it contains
        col, numConflicts = findMaxConflictCol()
        # print( "test col", col, numConflicts)
        # If the number of queens in the row, and diagonals is greater than 1 each (i.e. there are conflicts)
        if (numConflicts > 3):
            # Use the minConflictPos() function to determine the row index with the least number of conflicts
            newLocation = minConflictPos(col)
            # If the better location is not its current location, switch the location
            if (newLocation != board[col]):
                # Remove the conflicts from the position the queen is leaving
                changeConflicts(col, board[col], -1)
                board[col] = newLocation
                # Add a conflict to the position the queen is entering
                changeConflicts(col, newLocation, 1)
        # If the max number of conflicts (i.e. the number of queens in each row and diagonals) on the board
        #       equals 3, then there are no conflicts since the queen is alone in it's row and both diagonals
        elif numConflicts == 3:
            # Solution is found
            return True
        iteration += 1
    # If no solution is found in under average number of iterations, return False
    return False


def run(i) :
    global queensum
    global galois_inform
    global board
    global pickupQueens
    print( queensum, "queens")
    solve = [-1 for i in range(queensum)]
    # print(solve)
    currtime = time.time()
    initial_Galois_table(i) # argument: index 
    # print(mult_table)
    initial_galois_inform() # 計算 row, col 斜線 反斜線 裡面是否有重複 如果值超過2 代表有conflict
    # print(galois_inform)
    print( time.time() - currtime)
    
    # print(len(mult_table))
    # currtime = time.time()
    # get_conflict_queens()
    # print( time.time() - currtime)
    currtime = time.time()
    pick_queens()
    print("Pick up Queens Position",)
    print(f"Pick {len(pickupQueens)} Queens")
    print( time.time() - currtime)
    
    
    if queensum <= 3 or queensum > 10000000:
        # Print error and write empty array to file
        print("Cannot build board of size: " + str(queensum))
    else:
        # Set DIM equal to the current test queensum
        # Start timer and set/reset boolen
        time0 = time.time()
        solved = False
        print("Searching for board configuration of size " + str(queensum)+"...")
        # 6 is a special case, return hard-coded solution and skip while loop
        if (queensum == 6):
            board = [1,3,5,0,2,4]
            solved = True
        # Continues restarting solveNQueens() until a solution is found
        while (not solved):
            # Solved will be True when a solution is returned
            solved = solveNQueens()

        print("Board configuration found for size " + str(queensum))

        # Calculate and print time taken to find solution
        time1 = time.time()
        tot_time = time1 - time0
        time_string = str(trunc(tot_time*100)/100)
        print("   Took " + time_string + " seconds\n")
        # print( "Board")
        # print(board)



# print( galois.next_prime(1000000))
for i in range(1):
    print(i+1)
    run(i+1)
# queens = [ [3, 7], [7, 6], [4, 5] ] # [2, 2], [6, 1], [1, 4], [5, 3]
# queens = [[i[0]-1, i[1]-1] for i in queens]
# print(queens)
# ans = find_empty_positions(queens)
# print(ans)
