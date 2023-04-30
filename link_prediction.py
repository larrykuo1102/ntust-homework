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



# testset = dataset[:int(len(dataset)*1)]
# print(len(dataset))
# testset = dataset.sample(frac=0.3, random_state=42, replace=False)
# print(len(testset))
# print(len(dataset))
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
        shortest_path_length = -nx.shortest_path_length(G1, source=node1, target=node2)
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
        shortest_path_length = -nx.shortest_path_length(G1, source=node1, target=node2)
    except :
        shortest_path_length = -100
    
    test_Record.append([jacc, common_neighbors, pa1, adamic, shortest_path_length, indegree ])




        


training_data = pd.DataFrame(record)

training_data.to_csv('training_data.csv')




sc_X = StandardScaler()
# train_X = sc_X.fit_transform(train_X)
# train_label = sc_X.transform(train_label)


X_shortest = training_data[[0]]
X_shortest = sc_X.fit_transform(X_shortest)

X_common = training_data[[1]]
X_common = sc_X.fit_transform(X_common)

X_jaccard = training_data[[2]]
X_jaccard = sc_X.fit_transform(X_jaccard)

X_pa1 = training_data[[3]]
X_pa1 = sc_X.fit_transform(X_pa1)

X_adamic = training_data[[4]]
X_adamic = sc_X.fit_transform(X_adamic)

X_katz = training_data[[5]]
X_katz = sc_X.fit_transform(X_katz)

clf_shortest = SVC().fit(X_shortest, train_labels)
clf_common = SVC().fit(X_common, train_labels)
clf_jaccard = SVC().fit(X_jaccard, train_labels)
clf_pa1 = SVC().fit(X_pa1, train_labels)
clf_adamic = SVC().fit(X_adamic, train_labels)
clf_katz = SVC().fit(X_katz, train_labels)

classifier = VotingClassifier(estimators=[('shortest', clf_shortest), ('common', clf_common), ('jaccard', clf_jaccard),
                                          ('pa1', clf_pa1), ('adamic', clf_adamic), ('katz', clf_katz)],
                              voting='hard',
                              weights=[1, 1, 1, 1, 1, 1]) #

classifier.fit(record, train_labels)
y_pred = classifier.predict(test_Record)
print("Accuracy: %.2f%%" % (classifier.score(test_Record, test_labels) * 100.0))



# # Fitting Logistic Regression to the Training set

######################
# classifier = SVC()
# classifier.fit(record, train_labels)
# y_pred = classifier.predict(test_Record)
# print("Accuracy: %.2f%%" % (classifier.score(test_Record, test_labels) * 100.0))
#######################





# perform KFold cross validation
# kf = KFold(n_splits=5, shuffle=True, random_state=42)
# accuracy_scores = []

# for train_indices, test_indices in kf.split(X):
#     X_train, X_test = X.iloc[train_indices], X.iloc[test_indices]
#     y_train, y_test = y.iloc[train_indices], y.iloc[test_indices]
    
#     # X_train, X_test = X[train_indices], X[test_indices]
#     # y_train, y_test = y[train_indices], y[test_indices]
    
#     classifier.fit(X_train, y_train)
#     y_pred = classifier.predict(X_test)
    
#     accuracy_scores.append(accuracy_score(y_test, y_pred))

# # compute mean accuracy score
# mean_accuracy_score = sum(accuracy_scores) / len(accuracy_scores)

# print("Mean Accuracy Score: %.2f%%" % (mean_accuracy_score * 100.0))


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
        shortest_path_length = -nx.shortest_path_length(G1, source=node1, target=node2)
    except :
        shortest_path_length = -100


    
    predict_dict.append([jacc, common_neighbors, pa1, adamic, shortest_path_length, indegree ])
        


# predict_data = pd.DataFrame.from_dict(predict_dict, orient='index', columns=[
#                                       'Shortest', 'Common', 'Jaccard', 'PA1', 'adamic', 'katz'])

# predict_data.to_csv('predict_data.csv')
# predict_X = predict_data[['Shortest', 'Common', 'Jaccard', 'PA1', 'adamic', 'katz']]
predict_y = classifier.predict(predict_dict) 

# print((predict_X))
predict_y
predict_y.astype(int)
predict_y = pd.DataFrame(predict_y, columns=["ans"] )["ans"].astype(int)
predict_y.index = predict_y.index.rename("node_pair_id")
# predict_y = predict_y.reset_index().rename(columns={"index":"node_pair_id"})
# print(predict_y)
predict_y.to_csv("./result.csv")