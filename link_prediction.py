from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
# from dask_ml.linear_model import LogisticRegression
# from dask_ml.preprocessing import StandardScaler
import networkx as nx
import math
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
import numpy as np 
import pandas as pd 
from sklearn.ensemble import VotingClassifier
from networkx.algorithms.link_prediction import preferential_attachment
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score
dataset = pd.read_csv("./new_train_data.csv")  


G = nx.DiGraph()  
G1 = nx.Graph()  

label1 = dataset[(dataset["label"]==1)]
label0 = dataset[(dataset["label"]==0)]

edge = label1[["node1","node2"]].values

nodes = set(dataset['node1']).union(set(dataset['node2']))


G.add_edges_from(edge)
G.add_nodes_from(nodes)  # Add all nodes to graph
G1.add_edges_from(edge)
G1.add_nodes_from(nodes)  # Add all nodes to graph
# G.add_nodes_from(node2)

# G1.add_nodes_from(node2)

nodes = list(G.nodes())
edges = list(G.edges())
def calculate_score( source, target) :
    neighbors1 = set(G.neighbors(source))
    neighbors2 = set(G.neighbors(target))
    # 計算 Jaccard Coefficient      
    preds = nx.link_prediction.jaccard_coefficient(G1, [(source, target)])
    for u, v, p in preds:
        jaccard_coefficients = p
    
    # calculate common neighbors similarity
    num_common_neighbors = len(list(nx.common_neighbors(G1, source, target)))
    # PA1 PA2
    
    preds = nx.link_prediction.preferential_attachment(G1, [(source, target)])
    for u, v, p in preds:
        preferential1 = p
    
    preds = nx.link_prediction.adamic_adar_index(G1, [(source, target)])
    for u, v, p in preds:
        adamic = p

    
    return jaccard_coefficients, num_common_neighbors, preferential1, adamic
    
train_edges, test_edges, train_labels, test_labels = train_test_split(dataset[['node1', 'node2']].values, dataset['label'].values, test_size=0.5)


record = []
katz = nx.katz_centrality(G)
for edge in train_edges:
    # 獲取邊的兩個端點
    node1, node2 = edge # source -> target
    

    jacc, common_neighbors, pa1, adamic = calculate_score(node1,node2)
    indegree = G.in_degree(int(node1)) + G.in_degree(int(node2))+G.out_degree(int(node1)) + G.out_degree(int(node2))
    katz_score = katz[node2] + katz[node1]
    

    try :
        shortest_path_length = -len(nx.shortest_path_length(G1, source=node1, target=node2))
    except :
        shortest_path_length = -100


    
    record.append([jacc, common_neighbors, pa1, adamic, shortest_path_length, indegree ])
 
    
test_Record = []
katz = nx.katz_centrality(G)
for edge in test_edges:
    # 獲取邊的兩個端點
    node1, node2 = edge # source -> target

    jacc, common_neighbors, pa1, adamic = calculate_score(node1,node2)
    katz_score = katz[node2] + katz[node1]
    indegree = G.in_degree(int(node1)) + G.in_degree(int(node2))+G.out_degree(int(node1)) + G.out_degree(int(node2))

    try :
        shortest_path_length = -len(nx.shortest_path_length(G1, source=node1, target=node2))
    except :
        shortest_path_length = -100

    # test_Record[(node1,node2)].append(shortest_path_length)  
    
    # test_Record[(node1,node2)].append(label)
    
    test_Record.append([jacc, common_neighbors, pa1, adamic, shortest_path_length, indegree ])




        
# testset = dataset[int(len(dataset)*0.3):]

training_data = pd.DataFrame(record)

print(training_data[[0]])
  
# print( training_data ) 
training_data.to_csv('training_data.csv')

# train_X = training_data[['Shortest', 'Common', 'Jaccard', 'PA1','adamic', 'katz']]


######################
classifier = LogisticRegression()
classifier.fit(record, train_labels)
y_pred = classifier.predict(test_Record)
print("Accuracy: %.2f%%" % (classifier.score(test_Record, test_labels) * 100.0))
#######################

print("load predict csv")
predict_set = pd.read_csv("./new_test_data.csv")
predict_edge = predict_set[["node1","node2"]].values

G.add_nodes_from(predict_set['node1'])
G.add_nodes_from(predict_set['node2'])
G1.add_nodes_from(predict_set['node1'])
G1.add_nodes_from(predict_set['node2'])

predict_dict = []
katz = nx.katz_centrality(G)
for edge in predict_edge:
    # 獲取邊的兩個端點
    node1, node2 = edge # source -> target
    

    jacc, common_neighbors, pa1, adamic = calculate_score(node1,node2)
    katz_score = katz[node2] + katz[node1]
    indegree = G.in_degree(int(node1)) + G.in_degree(int(node2))+G.out_degree(int(node1)) + G.out_degree(int(node2))

    
    try :
        shortest_path_length = -nx.len(shortest_path_length(G1, source=node1, target=node2))
    except :
        shortest_path_length = -100

    # predict_dict[(node1,node2)].append(shortest_path_length)  
    
    predict_dict.append([jacc, common_neighbors, pa1, adamic, shortest_path_length, indegree ])

predict_y = classifier.predict(predict_dict) 

# print((predict_X))
predict_y
predict_y.astype(int)
predict_y = pd.DataFrame(predict_y, columns=["ans"] )["ans"].astype(int)
predict_y.index = predict_y.index.rename("node_pair_id")

predict_y.to_csv("./result.csv")