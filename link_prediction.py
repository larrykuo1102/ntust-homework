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
dataset = pd.read_csv("./new_train_data.csv")  
testset = dataset[:int(len(dataset)*1)]
# print(len(dataset))
# testset = dataset.sample(frac=0.3, random_state=42, replace=False)
# print(len(testset))
# print(len(dataset))
G = nx.DiGraph()  

label1 = testset[(dataset["label"]==1)]
label0 = testset[(dataset["label"]==0)]

edge = label1[["node1","node2"]].values

nodes = set(testset['node1']).union(set(testset['node2']))
# node1 = label0['node1'].values
# node2 = label0['node2'].values


G.add_edges_from(edge)
G.add_nodes_from(nodes)  # Add all nodes to graph
# G.add_nodes_from(node2)

# G1.add_nodes_from(node2)

nodes = list(G.nodes())
edges = list(G.edges())
all_edge = testset[['node1', 'node2']].values
def calculate_score( source, target) :
    neighbors1 = set(G.neighbors(source))
    neighbors2 = set(G.neighbors(target))
    # 計算 Jaccard Coefficient      
    jaccard_coefficients = 0 if len(neighbors1 | neighbors2) == 0 else len(neighbors1 & neighbors2) / len(neighbors1 | neighbors2)
    
    # calculate common neighbors similarity
    num_common_neighbors = len(neighbors1 & neighbors2)
    similarity = 0 if (len(neighbors1) + len(neighbors2) - num_common_neighbors) == 0 else num_common_neighbors / (len(neighbors1) + len(neighbors2) - num_common_neighbors)
    # PA1 PA2
    preferential1 = G.degree(source) + G.degree(target)
    preferential2 = G.degree(source) * G.degree(target)

    
    return jaccard_coefficients, similarity, preferential1, preferential2
    
record = {}
katz = nx.katz_centrality(G)
for edge in all_edge:
    # 獲取邊的兩個端點
    node1, node2 = edge # source -> target
    
    # neighbors1 = set(G.neighbors(node1)) 
    # neighbors2 = set(G.neighbors(node2))
    # link = (set(neighbors1) | set(neighbors2)) - set([node1])
    # for target in neighbors2 :

    record[(node1,node2)]= []
    jacc, common_neighbors, pa1, pa2 = calculate_score(node1,node2)
    katz_score = katz[node2] + katz[node1]
    
    record[(node1,node2)].append(jacc)
    record[(node1,node2)].append(common_neighbors)
    record[(node1,node2)].append(pa1)
    record[(node1,node2)].append(pa2)
    record[(node1,node2)].append(katz_score)
    try :
        shortest_path_length = -nx.shortest_path_length(G, source=node1, target=node2)
    except :
        shortest_path_length = -100

    record[(node1,node2)].append(shortest_path_length)  
    if (((node1,node2))in edges):
        record[(node1,node2)].append(1)
    else :
        record[(node1,node2)].append(0) # label  



        
    
training_data = pd.DataFrame.from_dict(record, orient='index', columns=[
                                       'Shortest', 'Common', 'Jaccard', 'PA1', 'PA2', 'katz', 'label'])
training_data = training_data.fillna(0)
    
print( training_data ) 
training_data.to_csv('training_data.csv')

X = training_data[['Shortest', 'Common', 'Jaccard', 'PA1','PA2', 'katz']]
y = training_data['label']

sc_X = StandardScaler()
# X_train = sc_X.fit_transform(X_train)
# X_test = sc_X.transform(X_test)

# print(X_train)
X_shortest = X[['Shortest']]
X_shortest = sc_X.fit_transform(X_shortest)

X_common = X[['Common']]
X_common = sc_X.fit_transform(X_common)
# X_test = sc_X.transform(X_test)
X_jaccard = X[['Jaccard']]
X_jaccard = sc_X.fit_transform(X_jaccard)
# X_test = sc_X.transform(X_test)
X_pa1 = X[['PA1']]
X_pa1 = sc_X.fit_transform(X_pa1)
# X_test = sc_X.transform(X_test)
X_pa2 = X[['PA2']]
X_pa2 = sc_X.fit_transform(X_pa2)
# X_test = sc_X.transform(X_test)
X_katz = X[['katz']]
X_katz = sc_X.fit_transform(X_katz)
# X_test = sc_X.transform(X_test)
# y = X_train['label']
# RandomForestClassifier
clf_shortest = SVC().fit(X_shortest, y)
clf_common = SVC().fit(X_common, y)
clf_jaccard = SVC().fit(X_jaccard, y)
clf_pa1 = SVC().fit(X_pa1, y)
clf_pa2 = SVC().fit(X_pa2, y)
clf_katz = SVC().fit(X_katz, y)

# # Fitting Logistic Regression to the Training set
# classifier = SVC()
# classifier.fit(X_train, y_train)
# y_pred = classifier.predict(X_test)

# print("Accuracy: %.2f%%" % (classifier.score(X_test, y_test) * 100.0))
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
classifier = VotingClassifier(estimators=[('shortest', clf_shortest), ('common', clf_common), ('jaccard', clf_jaccard),
                                          ('pa1', clf_pa1), ('pa2', clf_pa2), ('katz', clf_katz)],
                              voting='hard',
                              weights=[1, 1, 1, 5, 5, 1]) #

# X_train = sc_X.fit_transform(X_train)
# X_test = sc_X.transform(X_test)
classifier.fit(X_train, y_train)

y_pred = classifier.predict(X_test)
print("Accuracy: %.2f%%" % (classifier.score(X_test, y_test) * 100.0))
# KFold
# kf = KFold(n_splits=5)
# sc_X = StandardScaler()
# classifier = LogisticRegression(class_weight={'Shortest': 1.5, 'Common': 2, 'Jaccard': 0.5})
# for train_indices, validation_indices in kf.split(X):
#     X_train, X_test = X.iloc[train_indices], X.iloc[validation_indices]
#     y_train, y_test = y.iloc[train_indices], y.iloc[validation_indices]
    
#     X_train = sc_X.fit_transform(X_train)
#     X_test = sc_X.transform(X_test)
    
    
#     classifier.fit(X_train, y_train)
#     y_pred = classifier.predict(X_test)
#     accuracy = classifier.score(X_test, y_test)
    
#     print("Accuracy: %.2f%%" % (accuracy * 100.0))

print("load predict csv")
predict_set = pd.read_csv("./new_test_data.csv")
predict_edge = predict_set[["node1","node2"]].values
# predict_node1 = predict_set['node1'].values
# predict_node2 = predict_set['node2'].values

# Add all nodes to graph G
# predict_edge = list(zip(predict_node1, predict_node2))
# G.clear()
G.add_nodes_from(predict_set['node1'])
G.add_nodes_from(predict_set['node2'])

predict_dict = {}
katz = nx.katz_centrality(G)
for edge in predict_edge:
    # 獲取邊的兩個端點
    node1, node2 = edge # source -> target
    
    # neighbors1 = set(G.neighbors(node1))
    neighbors2 = set(G.neighbors(node2))
    
    # for target in neighbors2 :
    if ( predict_dict.get((node1,node2))) :
        # while(predict_dict.get((node1,node2))) :
        # print("testttttt")
        node2 = node2 + 1
        print((node1,node2))
    predict_dict[(node1,node2)]= []
    jacc, common_neighbors, pa1, pa2 = calculate_score(node1,node2)
    katz_score = katz[node2] + katz[node1]
    predict_dict[(node1,node2)].append(jacc)
    predict_dict[(node1,node2)].append(common_neighbors)
    predict_dict[(node1,node2)].append(pa1)
    predict_dict[(node1,node2)].append(pa2)
    predict_dict[(node1,node2)].append(katz_score)
    
    try :
        shortest_path_length = -nx.shortest_path_length(G, source=node1, target=node2)
    except :
        shortest_path_length = -100

    predict_dict[(node1,node2)].append(shortest_path_length)  
        


predict_data = pd.DataFrame.from_dict(predict_dict, orient='index', columns=[
                                      'Shortest', 'Common', 'Jaccard', 'PA1', 'PA2', 'katz'])

predict_data.to_csv('predict_data.csv')
predict_X = predict_data[['Shortest', 'Common', 'Jaccard', 'PA1', 'PA2', 'katz']]
predict_y = classifier.predict(predict_X) 

# print((predict_X))
predict_y
predict_y.astype(int)
predict_y = pd.DataFrame(predict_y, columns=["ans"] )["ans"].astype(int)
predict_y.index = predict_y.index.rename("node_pair_id")
# predict_y = predict_y.reset_index().rename(columns={"index":"node_pair_id"})
# print(predict_y)
predict_y.to_csv("./result.csv")