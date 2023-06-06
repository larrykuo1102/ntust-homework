import galois
import time
import numba
import numpy as np
from math import trunc
n = 10007 # 997 1009 10007
queensum = n - 1
solve = []
mult_table = []



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
def get_mult_table(n):
    mult_table = np.zeros((n, n), dtype=np.int64)
    for i in range(n):
        for j in range(n):
            mult_table[i, j] = (i * j) % n
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

def initial_Galois_table() :
    global n 
    global mult_table
    if n > 2 **20 :
        GF = galois.GF(int(n))
        print(GF.ufunc_mode)
        mult_table = [[GF(i)*GF(j) for j in range(n)] for i in range(n)]
    else :
        mult_table = get_mult_table(n)

def run( n ) :
    global queensum
    print( queensum, "queens")
    solve = [-1 for i in range(queensum)]
    # print(solve)
    currtime = time.time()
    initial_Galois_table()
    print( time.time() - currtime)
    
    print(len(mult_table))
    for galois_index in range(1,n) :
        galois_pos = get_Galois_position(galois_index)
        print(galois_pos)



print( galois.prev_prime(1000))
run(n)
# queens = [ [3, 7], [7, 6], [4, 5] ] # [2, 2], [6, 1], [1, 4], [5, 3]
# queens = [[i[0]-1, i[1]-1] for i in queens]
# print(queens)
# ans = find_empty_positions(queens)
# print(ans)
