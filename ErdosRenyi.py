
"""
Name: Erdos Renyi Network Model
Author: Pablo Eliseo Reynoso Aguirre
Date: April 14, 2017
Desrcription: Developing a graph model consisting of N labeled nodes connected by k arcs which are chosen randomly
              from the N(N-1)/2 possible (max-allowed) arcs. Based on the Model from Erdos-Renyi 1959.

              The graph can be represented as G(n,k); and G(n,p).
              Where:
                    n: number of nodes
                    k: number of arcs  -> constrained to: 0<= k <= n*(n-1)/2
                    p: fraction of links from the maximum arcs allowed  -> constained to: p>= 2*ln(n)/n

              Considering:

              k = p * (n*(n-1)/2)
              p = 2*k / n*(n-1)


"""

from scipy.stats import binom;
from A2_nets import utilities as utils;
import networkx as nx;
import random as rndm;
import seaborn as sns;
import numpy as np;
sns.set_palette("pastel", desat=.4)
sns.set_style("darkgrid")


class ErdosRenyi():

    def __init__(self, num_nodes, conn_prob):

        self.n = num_nodes;
        self.p = conn_prob;
        self.k_max = (self.n * self.n-1)/2;
        self.name = "ER_" + str(self.n) + "_" + str(self.p);
        self.path = 'Generated_Networks/ER/' + self.name;


    def generate_network_model(self):

        self.ER_model = nx.DiGraph();
        self.ER_model.add_nodes_from(range(self.n));
        self.add_edges();


    def add_edges(self):

        for node_i in range(self.n):
            for node_j in range(node_i+1,self.n):
                prob = rndm.random();
                if(prob < self.p):
                    self.ER_model.add_edge(node_i,node_j);


    def plot_degree_distribution(self, numberOfBins=10, save=False, log=False):

        utils.compute_pdf(self.ER_model, numberOfBins, log, self.name, self.path, save);


    def plot_original_distribution(self, save=False, log=False):

        model_degrees = self.ER_model.degree().values();
        freq_list = np.array(nx.degree_histogram(self.ER_model)[np.min(model_degrees):]) / float(self.n);
        degree_list = np.arange(np.min(model_degrees), np.max(model_degrees) + 1);
        original_distribution = binom.pmf(degree_list, self.n, self.p);
        utils.compare_distributions(degree_list, freq_list, original_distribution, log, self.name, self.path, save);


    def draw_network_graph(self, circular=False, save=False):

        utils.draw_network(self.ER_model, self.name, self.path, save, circular);


    def write_network(self):

        path = "Networks/ER(" + str(self.n) + "," + str(self.p) + ").net";
        nx.write_pajek(self.ER_model, path);


    def print_network_model_info(self):

        print("::::::::::::::::::::::::::::::::::::::::");
        print("::Erdos-Renyi Network Model::");
        print("Configuration: ");
        print("Number of nodes: ", self.n);
        print("Probability of connection: ", self.p);
        print("Number of edges: ", self.ER_model.number_of_edges());
        print(":::::::::::::::::::::::::::::::::::::::::");

