import galois
import numpy as np
print(galois.__version__)
value =9
irre_poly="x^2 + 1"
# x^2 + 1
# x^2 + x + 2
# x^2 + 2x + 2
GF = galois.GF(int(value),repr="poly",irreducible_poly=irre_poly) # poly, int, power

note_list = []
all_note_list = []
poly_index = ['1','2','x + 1','x + 2','2x + 1','2x + 2','x','2x']
mult_table = [[GF(i)*GF(j) for j in range(int(value))] for i in range(int(value))]
for list_index in poly_index :
    print(list_index, ":")
    for index,row in enumerate(mult_table):
        for index2,column in enumerate(row):
            if str(list_index) == str(column) : # α + 1
                print( "(" + str(column) + ")", end="\t")
                note_list.append([index,index2])
            else :
                print( column, end="\t" )
            if ( len(str(column)) <=4 ):
                print('',end="\t")
        print()
    print(note_list)
    print("=========================================================")
    all_note_list.append(note_list.copy())
    note_list.clear()

print(all_note_list)

# mult_table = [[GF(i)*GF(j) for j in range(int(value))] for i in range(int(value))]
# note_list = []
# all_note_list = []
# for number in range(1,int(value)) :
#     print(number)
#     for index,row in enumerate(mult_table):
#         for index2,column in enumerate(row) :
#             if index == 0 or index2 == 0 :
#                 pass
#             elif str(number) == str(column) : # α + 1
#                 print( "(" + str(column) + ")", end="\t")
#                 note_list.append([index,index2])
#             elif index <= index2: # 2,2 3,3 3,4
#                 print( "X", end="\t")
#             else:
#                 print( end="\t")
            
#         print()
#     print(note_list)
#     all_note_list.append(note_list.copy())
#     note_list.clear()
#     print()

# print( all_note_list )


Listirreducible_polys = list(galois.irreducible_polys(3, 2))
# for i in Listirreducible_polys:
print(Listirreducible_polys)
# print(GF.properties)




