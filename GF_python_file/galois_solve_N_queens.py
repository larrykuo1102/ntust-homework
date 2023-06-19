import galois
import time
import numba
import numpy as np
from math import trunc
n = 997 # 997 1009 10007
queensum = n - 1
solve = []
mult_table = []
galois_inform = {
    "diag1" : [0]*(queensum*2-1),
    "diag2" : [0]*(queensum*2-1),
    "row" : [0]*queensum,
    "col" : [0]*queensum
}


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

def select_queens() :
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
            
    print( diag1 )
    print( diag2 )
    print( col )
    print( row )
    pass

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


def run() :
    global queensum
    global galois_inform
    print( queensum, "queens")
    solve = [-1 for i in range(queensum)]
    # print(solve)
    currtime = time.time()
    initial_Galois_table(1) # argument: index 
    initial_galois_inform() # 計算 row, col 斜線 反斜線 裡面是否有重複 如果值超過2 代表有conflict
    # print(galois_inform)
    print( time.time() - currtime)
    
    print(len(mult_table))
    currtime = time.time()
    select_queens()
    print( time.time() - currtime)
    



print( galois.prev_prime(1000))
run()
# queens = [ [3, 7], [7, 6], [4, 5] ] # [2, 2], [6, 1], [1, 4], [5, 3]
# queens = [[i[0]-1, i[1]-1] for i in queens]
# print(queens)
# ans = find_empty_positions(queens)
# print(ans)
