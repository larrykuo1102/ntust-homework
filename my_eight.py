from itertools import combinations
k = 8 # N queens
need_print = 0 # 0: not print 1: print
all_list = []
test_all_list = []
def put_queen(state:list,n:int):
    if ( n > 0 ):
        for row in range(1,k+1):
            for column in range(n, k+1):
                if check_valid(state,[row,column]) :
                    state.append([row,column])  
                    if len(state) == k :
                        if state not in all_list:
                            check_duplicate_and_append(state.copy())
                            all_list.append(state.copy())
                        # print(state)
                        state.pop()
                    else :
                        a = put_queen(state, n-1)
                        if (a == False and len(state)!=k and len(state)!=0):
                            state.pop()
    return False

def check_valid(current_state:list, next:list):
    row = next[0]
    column = next[1]
    for i in current_state :
        if row == i[0] : # check column
            return False
        if column == i[1]: # check row
            return False
        if abs(i[0]-row) == abs(i[1]-column): # check diagonal
            return False
    return True

factor = k + 1
def X_Y_exchange(state):
    return [[x[1],x[0]]for x in state]

def X_projection(state):
    return [[x[0],factor-x[1]]for x in state]

def Y_projection(state):
    return [[factor-x[0],x[1]]for x in state]

def XY_projection(state):
    return [[factor-x[1],factor-x[0]]for x in state]

def rotate_90(state): # 5,3 -> 6,5
    return [[factor-x[1],x[0]]for x in state]

def rotate_180(state): # 5,3 -> 4,6
    return [[factor-x[0],factor-x[1]]for x in state]

def rotate_270(state): # 5,3 -> 3,4
    return [[x[1],factor-x[0]]for x in state]

def check_duplicate_and_append(current_state) :
    count_exist = 0
    count_X_Y_exist = 0
    count_X_projection = 0
    count_Y_projection = 0
    count_XY_projection = 0
    count_rotate_90 = 0
    count_rotate_180 = 0
    count_rotate_270 = 0
    success:bool=True
    for each in all_list:
        for i in current_state :
            if i in each :
                count_exist += 1
            if i in X_Y_exchange(each):
                count_X_Y_exist +=1
            if i in X_projection(each):
                count_X_projection +=1
            if i in Y_projection(each):
                count_Y_projection +=1
            if i in XY_projection(each):
                count_XY_projection +=1
            if i in rotate_90(each):
                count_rotate_90 +=1
            if i in rotate_180(each):
                count_rotate_180 +=1
            if i in rotate_270(each):
                count_rotate_270 +=1
        if count_exist == 8 or count_X_Y_exist == k or count_X_projection == k or count_Y_projection == k or count_XY_projection == k :
            success = False
        elif count_rotate_270 == k or count_rotate_90 == k or count_rotate_180 == k :
            success = False
        else :
            count_exist = 0
            count_X_Y_exist = 0
            count_X_projection = 0
            count_Y_projection = 0
            count_XY_projection = 0
            count_rotate_90 = 0
            count_rotate_180 = 0
            count_rotate_270 = 0
    if success :
        test_all_list.append(current_state.copy())

def main( n ):
    my_state :list = []
    put_queen(my_state,n)
    print(len(all_list))
    test = [[1, 1], [2, 2], [3, 5], [4, 8], [5, 3], [6, 7], [7, 6], [8, 4]]
    comb_test = list(combinations(test,4)) 
    print( len( comb_test ) )
    all_possible = [[[1, 1], [2, 2], [3, 5], [4, 8], [5, 3], [6, 7], [7, 6], [8, 4]], [[1, 2], [2, 1], [3, 7], [4, 4], [5, 6], [6, 5], [7, 3], [8, 8]], [[1, 3], [2, 6], [3, 1], [4, 5], [5, 4], [6, 2], [7, 8], [8, 7]], [[1, 4], [2, 8], [3, 3], [4, 1], [5, 7], [6, 6], [7, 5], [8, 2]], [[1, 5], [2, 7], [3, 8], [4, 6], [5, 1], [6, 4], [7, 2], [8, 3]], [[1, 6], [2, 3], [3, 2], [4, 7], [5, 8], [6, 1], [7, 4], [8, 5]], [[1, 7], [2, 5], [3, 4], [4, 3], [5, 2], [6, 8], [7, 1], [8, 6]], [[1, 8], [2, 4], [3, 6], [4, 2], [5, 5], [6, 3], [7, 7], [8, 1]]]
    # testall = [[1,1],[3,5],[4,8],[6,7],[12,1],[33,5],[45,86],[62,7]]
    # all_list.append(testall)
    success = []
    yes = True
    for row in all_list:
        for single in comb_test :
            for i in single:
                if i not in row :
                    yes = False
            if yes == True:
                success.append(row)
            yes = True
            
            for i in X_Y_exchange(test):
                if i not in row :
                    yes = False
            if yes == True:
                success.append(row)
            yes = True

            for i in X_projection(test):
                if i not in row :
                    yes = False
            if yes == True:
                success.append(row)
            yes = True

            for i in Y_projection(test):
                if i not in row :
                    yes = False
            if yes == True:
                success.append(row)
            yes = True

            for i in XY_projection(test):
                if i not in row :
                    yes = False
            if yes == True:
                success.append(row)
            yes = True
            
            for i in rotate_90(test):
                if i not in row :
                    yes = False
            if yes == True:
                success.append(row)
            yes = True
            
            for i in rotate_180(test):
                if i not in row :
                    yes = False
            if yes == True:
                success.append(row)
            yes = True
            
            for i in rotate_270(test):
                if i not in row :
                    yes = False
            if yes == True:
                success.append(row)
            yes = True
        

    print( len(success) )
    for i in success :
        print( i)
    
    
    if need_print == 1 :
        for i in test_all_list:
            print(i)
    print(len(test_all_list))
main(k)
a = [[8, 8], [4, 7], [1, 6], [3, 5], [6, 4], [2, 3], [7, 2], [5, 1],[1,1],[3,5],[4,8],[6,7]]

# test = [[1,1],[3,5],[4,8],[6,7]]

# yes = True
# for i in test :
#     if i not in a :
#         yes = False
# print(yes)

# print(X_Y_exchange(a))
# print(X_projection(a))
# print(Y_projection(a))
# print(rotate_180(a))
# print(rotate_270(a))
# print(rotate_90(a))
