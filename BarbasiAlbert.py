"""
Name: Barbasi Albert Network Model
Author: Pablo Eliseo Reynoso Aguirre
Date: April 14, 2017
Desrcription: Developing a graph model consisting of n labeled nodes connected by m arcs which are chosen randomly
              and an initial number of nodes n0<n. Based on the Model from Barbasi-Albert 1999.

              The graph can be represented as G(n0,n,m);
              Where:
                    n0: initial number of nodes
                    n: number of nodes
                    m: number of arcs


"""

import networkx as nx;
import random as rndm;
import numpy as np;
from A2_nets import utilities as utils;


class BarabasiAlbert:

    def __init__(self, num_nodes, new_node_edges, init_num_nodes=5):

        self.n = num_nodes;
        self.m = new_node_edges;
        self.n0 = init_num_nodes;
        self.name = "BA_" + str(self.n) + "_" + str(self.n0) + "_" + str(self.m);
        self.path = 'Generated_Networks/BA/' + self.name;


    def generate_network_model(self):

        self.model_init();
        self.model_growth();


    def model_init(self):

        self.BA_model = nx.DiGraph();
        self.BA_model.add_nodes_from(range(self.n0));

        for node_i in range(self.n0):
            for node_j in range(node_i+1, self.n0):
                self.BA_model.add_edge(node_i,node_j);


    def model_growth(self):

        for new_node in range(self.n0, self.n):
            self.BA_model.add_node(new_node);
            self.preferential_attachment(new_node);


    def preferential_attachment(self, new_node):

        total_degrees = 2*self.BA_model.number_of_edges();
        intervals = np.cumsum(self.BA_model.degree().values());
        selected_nodes_list = [];
        while (len(selected_nodes_list) < self.m and len(selected_nodes_list) < self.BA_model.number_of_nodes() - 1):
            random_number = total_degrees * rndm.random();
            for node in range(new_node):
                if random_number < intervals[node]:
                    if node in selected_nodes_list:
                        break;
                    else:
                        self.BA_model.add_edge(node, new_node);
                        selected_nodes_list.append(node);
                        break;


    def plot_degree_distribution(self, numberOfBins=10, save=False, log=True):

        utils.compute_pdf(self.BA_model, numberOfBins, log, self.name, self.path, save);


    def plot_original_distribution(self, save=False, log=True):

        degree_values = self.BA_model.degree().values();
        freq_list = np.array(nx.degree_histogram(self.BA_model)[np.min(degree_values):]) / float(self.n);
        degree_list = np.arange(np.min(degree_values), np.max(degree_values) + 1);
        ks = [1. * k ** (-3) for k in degree_list];
        sumks = np.sum(ks);
        original_distribution = ks / sumks;
        utils.compare_distributions(degree_list, freq_list, original_distribution, log, self.name, self.path, save);


    def exponent_estimation(self, bins_number=8, gamma=3.0):

        exponent = utils.generalized_exponent_estimation(self.BA_model, bins_number, self.name, self.path, gamma);
        return exponent;

    def draw_network_graph(self, circular=False, save=False):

        utils.draw_network(self.BA_model, self.name, self.path, save, circular);


    def write_network(self):

        nx.write_pajek(self.BA_model, self.path + ".net");


    def print_network_model_info(self, exponent):

        print("::::::::::::::::::::::::::::::::::::::::");
        print("::Barbasi-Albert Network Model::");
        print("Configuration: ");
        print("Number of nodes: ",self.n);
        print("Number of initial nodes: ",self.n0);
        print("Number of edges: ",self.BA_model.number_of_edges());
        print("Exponent estimated: ",exponent);
        print(":::::::::::::::::::::::::::::::::::::::::");

