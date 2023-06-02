import galois

n = 11
queens = n - 1
solve = []

GF = galois.GF(int(n)) 
mult_table = [[GF(i)*GF(j) for j in range(int(n))] for i in range(int(n))]
'''

1. do galois field(n)

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


def find_empty_positions(queens):
    empty_positions = [True] * 8
    diag1 = [True] * 15
    diag2 = [True] * 15

    # 设置已知皇后的位置为 False，并排除斜线和反斜线上的位置
    for queen in queens:
        row, col = queen
        empty_positions[col] = False
        diag1[row + col] = False
        diag2[row - col + 7] = False

    # 查找空位
    result = []
    for i in range(8):
        if empty_positions[i] and diag1[queens[-1][0] + i] and diag2[queens[-1][0] - i + 7]:
            result.append((len(result), i))  # 存储位置的行索引和列索引

    return result


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

def run( n ) :
    global queens
    print( queens, "queens")
    solve = [-1 for i in range(queens)]
    print(solve)

    for galois_index in range(1,n) :
        galois_pos = get_Galois_position(galois_index)
        print(galois_pos)



run(n)
