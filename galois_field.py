import galois
import pprint
import numpy as np
print(galois.__version__)
GF = galois.GF(3**2, repr="int") # poly, int, power



mult_table = [[GF(i)*GF(j) for j in range(3**2)] for i in range(3**2)]
note_list = []
for number in range(1,9) :
    print(number)
    for index,row in enumerate(mult_table):
        for index2,column in enumerate(row) :
            if index == 0 or index2 == 0 :
                pass
            elif str(number) == str(column) : # α + 1
                print( "(" + str(column) + ")", end="\t")
                note_list.append((index,index2))
            elif index <= index2: # 2,2 3,3 3,4
                print( "X", end="\t")
            else:
                print( end="\t")
            
        print()
    print(note_list)
    note_list.clear()
    print()


f = GF.Random((3, 2), seed=1) ; f
print(f)

Listirreducible_polys = list(galois.irreducible_polys(3, 2))
for i in Listirreducible_polys:
    print(i)
# print(GF.properties)




