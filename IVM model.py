# -*- coding: utf-8 -*-
"""IVM_Side_Project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1SymwkOe1tRHpNFE0xFQMHuucLcgcYKhm
"""

from google.colab import drive

drive.mount('/content/drive');

pip install pyvis

import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')      #download if using this module for the first time

# -*- coding: utf-8 -*-
"""
Spyder Editor
@author: Fernando Sanchez
This is a temporary script file.
"""

from openpyxl import load_workbook
import pandas as pd
import xlrd
import matplotlib.pyplot as plt
import networkx as nx
from pyvis.network import Network
from IPython.core.display import display, HTML
import matplotlib.pyplot as plt
import heapq
import math
from collections import defaultdict
import nltk
from nltk.tokenize import word_tokenize
from collections import Counter


from nltk.stem import WordNetLemmatizer 

#For Gensim
import gensim
import string
from gensim import corpora
from gensim.corpora.dictionary import Dictionary
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
import heapq

#Goal for tomorrow -> Create a class structure to give more cohesion, instead of just having functions at random
#Goals:
'''
-Turn all methods and put them into a cohesive class
-Start cleaning the text for all components -> eliminate stopwords
-Change color

'''

class NetEye:
  def __init__(self, filename):
    self.workbook = xlrd.open_workbook(filename);
    self.sheet = self.workbook.sheet_by_index(1);
    self.G = self.make_graph();

  def make_graph(self):
    self.tracker = defaultdict(lambda: []); #-> Dictionary will hold the node and its description
    G = nx.DiGraph();
    for i in range(1, self.sheet.nrows, 1):
      row = self.sheet.row_values(i, 0);
      G.add_node(row[0], size = 10)
      G.add_node(row[5], size = 10)
      enabling_description = self.clean_tokenize(row[2]); #to be added and cleaned
      self.tracker[row[0]].append(enabling_description);
      dependent_description = self.clean_tokenize(row[4]) # to be added and cleaned
      self.tracker[row[5]].append(dependent_description)
      string_converter = "Enabler_Comp: " + row[1] + "<br>" + "Enabling Description: " + str(enabling_description) + "<br>" + "Dependent Component: "+  row[3] + "<br>" +  "Description: " + str(dependent_description) + "<br>";
      G.add_edge(row[0], row[5], title = string_converter);
      
    return G

  def clean_tokenize(self, string):
    if len(string) < 10:
      return list(string);
    pranker = word_tokenize(string)
    #Now that we tokenized the string, we get rid of the punctuation
    container = [word for word in pranker if word.isalpha()]
    studder = stopwords.words('english');
    result = [word for word in container if word not in studder]

    maker = defaultdict(lambda: 0);
    for word in result:
      maker[word] += 1;

    pre = []
    for word, count in maker.items():
      tuplet = (-1 * count, word)
      pre.append(tuplet)

    heapq.heapify(pre)
    lister = []
    while len(pre) > 0:
      lister.append(heapq.heappop(pre)[1])
    
    lister = lister[:5]
    return lister #Method returns the top five words in the description
    

  def subgraph(self):
    #Function that asks for user's policy information and returns a set of policies that it is connected to
    subgrapher = nx.DiGraph();
    query = input("Please input a policy you'd like to see\n");
    edges = self.G.edges(query); #Edges
    lister = list(self.G.neighbors(query)); #Nodes
    subgrapher.add_nodes_from(lister);
    for node_affected in lister:
      stringer = self.G[query][node_affected]['title'];
      subgrapher.add_edge(query, node_affected, title=stringer);

    for nodes in subgrapher:
      connections = nx.all_neighbors(subgrapher, nodes)
      weight = len(list(connections)) *0.90
      subgrapher.nodes[nodes]['size'] = weight;
      affecting = subgrapher.out_degree(nodes) # Gives you how many documents this particular node is affecting
      subgrapher.nodes[nodes]['title'] = "Degree: " + str(affecting) + "<br>";
      affectors = subgrapher.in_degree(nodes);
      subgrapher.nodes[nodes]['title'] += " In-Degree: " + str(affectors) + "<br>";
    net = Network('2000px', '2000px', directed=True);
    net.from_nx(subgrapher)
    net.show_buttons(filter_=['physics'])
    net.show('nx.html');
    display(HTML('nx.html'))
    return

  def policy_driver(self):
    #Funciton that will return a list of policies and their degrees -> aka, the number of policies they affecct
    #Function will return a max heap to inform the user of what policies are being influenced the most
    dict_lookup ={
      
    }
    max_heaper_pred = [];
    max_heaper_succ = []
    heapq.heapify(max_heaper_pred);
    #Step 1: Get the graph and count how many nodes there are
    amount_of_nodes = self.G.order();
    print(amount_of_nodes);
    #Step 2: Iterate over the nodes
    nodes = list(self.G);
    for policy in nodes:
      affectors = self.G.pred[policy];
      pair = (-1 * len(affectors), policy);
      heapq.heappush(max_heaper_pred, pair);

      affecting = self.G.succ[policy];
      pair_suc = (len(affecting), policy);
      heapq.heappush(max_heaper_succ, pair_suc);
    
  
    print(max_heaper_pred);
    return

  def short_path(self):
    starter = input("Provide the source document ")
    ender = input("Provide the target document ")
    if nx.has_path(self.G, starter, ender):
      pather = nx.shortest_path(self.G, source=starter, target= ender);
      print(pather)
      return
    else:
      print("A path between the two provided documents")
      return
  def all_paths(self):
    starter = input("Provide the source document ")
    ender = input("Provide the target document ")
    print("doner");
    for path in sorted(nx.all_simple_edge_paths(self.G, starter, ender)):
      print(path)
    return

  def make_Network(self):
    major = Network('2500px', '2500px', directed=True);
    #Construct a list that maps each node to the amount of neighbors they have
  
    for nodes in self.G.nodes():
      connections = nx.all_neighbors(self.G, nodes)
      weight = len(list(connections)) *0.90
      self.G.nodes[nodes]['size'] = weight;
      affecting = self.G.out_degree(nodes) # Gives you how many documents this particular node is affecting
      self.G.nodes[nodes]['title'] = "Degree: " + str(affecting) + "<br>";
      affectors = self.G.in_degree(nodes);
      self.G.nodes[nodes]['title'] += " In-Degree: " + str(affectors) + "<br>";
    
    maker = nx.DiGraph(self.G);
    major.from_nx(maker)
    major.show_buttons(filter_=['physics'])
    major.show("NetEye.html")
    display(HTML('NetEye.html'))
    return major;


'''
Next steps:
2.Export the information (short paths, longest path) into Excel File for analysis
4. See if you can change the shape of a node, corresponding to the number of other nodes they affect
'''
  

  
filename = '/content/drive/MyDrive/IntegratedValueModelAllAgencies.xlsx'

_Brother = NetEye(filename);
_Brother.make_Network();
#_Brother.subgraph(); #VA Business Reference Model
#_Brother.policy_driver() #Tells us the policy that's being affected the most (ranked by incoming edges)
#_Brother.short_path() #Gives you the short path between two policies
#VA Business Reference Model - VA Legislation
#DoD Strategy for Suicide Prevention December 2015 -VA Secretary 4 Priorities for VA
#print(_Brother.G.nodes());
#print(_Brother.G.edges())

#for path in nx.all_simple_paths(_Brother.G, "DoD Strategy for Suicide Prevention December 2015", "VA Secretary 4 Priorities for VA", cutoff = 4):
  #print(path)

#print(_Brother.G.nodes());
#print(_Brother.G.edges())

_Brother.policy_driver() #Tells us the policy that's being affected the most (ranked by incoming edges)

#_Brother.short_path() #Gives you the short path between two policies ### DoD Strategy for Suicide Prevention December 2015 -VA Secretary 4 Priorities for VA