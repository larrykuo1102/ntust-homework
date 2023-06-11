import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
import random
import pandas as pd
from networkx import community
def makeSampleGraph():
    '''
    生成图
    '''

    dataset = pd.read_csv('./community_detection/train.csv') 
    G = nx.Graph()
    # dataset = dataset[:500]
    # print(len(dataset))ㄌ
    edge = dataset[["Node1","Node2"]].values
    G.add_weighted_edges_from(list((x, y, 1) for x,y in edge))
    # G.add_edges_from(edge)

    return G


sample_graph = makeSampleGraph()

partition = nx.algorithms.community.louvain_communities(sample_graph)

result_community = {}
for index, i in enumerate( partition) :
    for node in i :
        result_community[node] = index
        
testdata = pd.read_csv('./community_detection/test.csv')
testdata = testdata[['Node1','Node2']].values
result = []
for x, y in testdata :
    # print(result_community.get(y,-2))
    if (result_community.get(x,-1) == result_community.get(y, -2)) :
        result.append(1)
    else :
        result.append(0)
    # print(x, y)

predict_y = pd.DataFrame(result, columns=["Category"] )["Category"].astype(int)
predict_y.index = predict_y.index.rename("Id")
predict_y.to_csv("./community_detection/sampleSubmission.csv")