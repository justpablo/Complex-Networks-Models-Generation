"""
Name: Configuration Network Model
Author: Pablo Eliseo Reynoso Aguirre
Date: April 14, 2017
Desrcription: Developing a graph model consisting of n labeled nodes and a degree distribution p(k),
              building a network given a degree sequence, based on 1995 theory.

              The graph can be represented as G(n,gamma);
              Where:
                    n: number of nodes
                    gamma: degree exponent

"""

import networkx as nx;
import random as rndm;
import numpy as np;
from A2_nets import utilities as utils;

class ConfigurationModel:

    def __init__(self, nodes_num, gamma):

        self.n = nodes_num;
        self.gamma = gamma;
        self.name = "CM_" + str(self.n) +"_"+ str(self.gamma);
        self.path = 'Generated_Networks/CM/' + self.name;


    def generate_network_model(self):

        self.C_model = nx.Graph();
        self.C_model.add_nodes_from(range(self.n));
        edges_vector = self.generate_edges_vector();
        stubs_vector = self.generate_stubs_vector(edges_vector);
        edges = self.generate_edges_from_stubs(stubs_vector);
        self.C_model.add_edges_from(edges)


    def generate_edges_vector(self):

        ks = [1. * k ** (-self.gamma) for k in range(1, int(np.sqrt(self.n)) + 1)];
        sumks = np.sum(ks);
        ks = ks / sumks;
        intervals = np.cumsum(ks);
        edges_vector = [self.calculate_edges_number(intervals) for _ in range(self.n)];
        return edges_vector;


    def generate_edges_from_stubs(self, stubs_vector, maxIter=10):

        stubs = stubs_vector[:];
        pairs = [];
        while (len(stubs) > 1 or iter < maxIter):
            rndm.shuffle(stubs);
            remaining, i = [], 0;
            while (i < len(stubs) - 1):
                pair = (stubs[i], stubs[i + 1]);
                if pair[0] != pair[1] and pair not in pairs:
                    pairs.append(pair);
                    i += 2;
                else:
                    remaining.append(pair[0]);
                    i += 1;
                if i == len(stubs) - 1: remaining.append(stubs[i]);
            stubs = remaining[:];
        return pairs;


    def calculate_edges_number(self, intervals):

        randomNumber = rndm.random();
        for i in range(len(intervals)):
            if randomNumber < intervals[i]:
                return i + 1;


    def generate_stubs_vector(self, edges_vector):

        listOfNodes = range(self.n);
        stubs_vector = [];
        for i in listOfNodes:
            for _ in range(edges_vector[i]):
                stubs_vector.append(i);
        return stubs_vector;


    def plot_degree_distribution(self, numberOfBins=10, save=False, log=True):

        utils.compute_pdf(self.C_model, numberOfBins, log, self.name, self.path, save);


    def plot_original_distribution(self, save=False, log=True):

        degree_values = self.C_model.degree().values();
        freq_list = np.array(nx.degree_histogram(self.C_model)[np.min(degree_values):]) / float(self.n);
        degree_list = np.arange(np.min(degree_values), np.max(degree_values) + 1);
        ks = [1. * k ** (-self.gamma) for k in degree_list];
        sumks = np.sum(ks);
        original_distribution = ks / sumks;
        utils.compare_distributions(degree_list, freq_list, original_distribution, log, self.name, self.path, save);


    def exponent_estimation(self, num_bins=8):

       exponent = utils.generalized_exponent_estimation(self.C_model, num_bins, self.name, self.path, self.gamma);
       return exponent;

    def draw_network_graph(self, circular=False, save=False):

        utils.draw_network(self.C_model, self.name, self.path, save, circular);


    def write_network(self):

        nx.write_pajek(self.C_model, self.path + '.net');


    def print_network_model_info(self, exponent):

        print("::::::::::::::::::::::::::::::::::::::::");
        print("::Configuration Network Model::");
        print("Configuration: ");
        print("Number of nodes: ",self.n);
        print("Gamma: ",self.gamma);
        print("Number of edges: ",self.C_model.number_of_edges());
        print("Exponent estimated: ",exponent);
        print(":::::::::::::::::::::::::::::::::::::::::");

