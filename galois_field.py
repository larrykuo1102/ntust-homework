import galois
import pprint
import numpy as np
print(galois.__version__)
GF = galois.GF(3**2, repr="poly")



mult_table = [[GF(i)*GF(j) for j in range(3**2)] for i in range(3**2)]
note_list = []
for index,row in enumerate(mult_table):
    for index2,column in enumerate(row) :
        if "α + 1" == str(column) :
            print( "(" + str(column) + ")", end="\t")
            note_list.append((index,index2))
        else :
            print( column, end="\t")
        
    print()
print(note_list)

f = GF.Random((3, 2), seed=1) ; f
print(f)

Listirreducible_polys = list(galois.irreducible_polys(3, 2))
for i in Listirreducible_polys:
    print(i)
# print(GF.properties)




