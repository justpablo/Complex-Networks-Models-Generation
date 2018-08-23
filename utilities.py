
"""
Name: Network Model-Building Utilities Functions
Author: Pablo Eliseo Reynoso Aguirre
Date: April 17, 2017

"""


import math;
import numpy as np;
import networkx as nx;
from sklearn import linear_model;
import matplotlib.pyplot as plt;
import seaborn as sns;

sns.set_palette("deep", desat=.6);
sns.set_style("whitegrid");


def draw_network(G, name, path, save, circular):

    if circular: nx.draw_circular(G);
    else: nx.draw_random(G);

    plt.axis('off');
    plt.title(name, fontweight='bold', fontsize=12);

    if save: plt.savefig(path + '_graph.pdf', bbox_inches='tight');
    plt.close()


def generalized_exponent_estimation(G, num_bins, name, path, gamma):

    degrees_list = G.degree().values();

    kmin, kmax = np.min(degrees_list), np.max(degrees_list);
    division = np.linspace(math.log10(kmin), math.log10(kmax + 1), num_bins + 1);
    weights = np.ones_like(degrees_list) / float(len(degrees_list));

    pdf = plt.hist(degrees_list, bins=10 ** division, weights=weights, log=True);

    x = np.array([[division[i]] for i in range(len(pdf[0])) if pdf[0][i] != 0]);
    y = np.array([[np.log10(pdf[0])[i]] for i in range(len(pdf[0])) if pdf[0][i] != 0]);

    lin_reg = linear_model.LinearRegression();
    lin_reg.fit(x, y);

    return lin_reg.coef_[0][0];


def exponent_estimation(division, pdf):

    x = np.array([[division[i]] for i in range(len(pdf[0])) if pdf[0][i] != 0]);
    y = np.array([[np.log10(pdf[0])[i]] for i in range(len(pdf[0])) if pdf[0][i] != 0]);

    lin_reg = linear_model.LinearRegression();
    lin_reg.fit(x, y);

    return -lin_reg.coef_[0][0];


def compare_distributions(degree_list, freq_list, original_distribution, log, name, path, save):

    plt.plot(degree_list, freq_list, 'o', ms=8, color=sns.desaturate("darkkhaki", .80));
    plt.plot(degree_list, original_distribution, '-', ms=8, color=sns.desaturate("blueviolet", .80));
    plt.suptitle('Theoretical vs. Experimental Degree Distributions', fontweight='bold', fontsize=12);
    plt.title(name, style='italic', fontsize=9);
    plt.grid(b=True, which='minor', linestyle='-');
    plt.tick_params(axis='both', which='both', direction='out', color='0.75', length=3, width=1, top=False, right=False);
    plt.minorticks_on();

    if log:

        plt.xscale('log');
        plt.yscale('log');
        axes = plt.gca();
        xmin, xmax = configure_x_axis(np.min(degree_list), np.max(degree_list));
        axes.set_xlim([xmin, xmax])

    if save: plt.savefig(path + '_original.pdf', bbox_inches='tight');

    plt.close()


def compute_pdf(G, num_bins, log, name, path, save):

    degrees_list = G.degree().values();
    kmin, kmax = np.min(degrees_list), np.max(degrees_list);

    if log: division = 10. ** np.linspace(math.log10(kmin), math.log10(kmax + 1), num_bins + 1);
    else: division = np.linspace(kmin, kmax + 1, num_bins + 1);

    plot_pdf(log, degrees_list, division, kmin, kmax, name, path, save, num_bins);


def plot_pdf(log, degrees_list, division, kmin, kmax, name, path, save, num_bins):

    weights = np.ones_like(degrees_list) / float(len(degrees_list));
    pdf = plt.hist(degrees_list, bins=division, weights=weights, log=log, alpha=0.8, color=sns.desaturate("darkkhaki", .80));

    plt.grid(b=True, which='minor', linestyle='-');
    plt.tick_params(axis='both', which='both', direction='out', color='0.75', length=3, width=1, top=False, right=False);
    plt.minorticks_on();
    plt.xlabel("k");
    plt.ylabel("P(k)");

    if log:

        gamma = exponent_estimation(division, pdf);

        plt.suptitle(name + ' PDF', fontweight='bold', fontsize=12);
        plt.title('Estimated gamma: ' + str(gamma), fontweight='bold', style='italic', fontsize=9);
        plt.xscale('log');

        axes = plt.gca();
        ymin, ymax = configure_y_axis(pdf);
        axes.set_ylim([ymin, ymax]);
        xmin, xmax = configure_x_axis(kmin, kmax);
        axes.set_xlim([xmin, xmax]);

    else: plt.title(name + ' PDF', fontweight='bold', fontsize=12);

    if save: plt.savefig(path + '_' + str(num_bins) + 'bins_PDF.pdf', bbox_inches='tight');

    plt.show()
    plt.close()


def configure_x_axis(kmin, kmax):

    max_order_x = np.floor(kmax + 1 - 10 ** math.log10(kmax + 1));

    if kmin == 0: xmin = kmin
    else:
        min_order_x = 10 ** np.floor(math.log10(kmin));
        xmin = np.ceil((kmin - min_order_x) / min_order_x) * min_order_x;

    max_order_x = 10 ** np.floor(math.log10(kmax + 1));
    xmax = np.ceil((kmax + 1) / max_order_x) * max_order_x;

    return xmin, xmax;

def configure_y_axis(hist):

    ymax = 1;
    min_order_magnitude = math.log10(np.min([p for p in hist[0] if p != 0]));

    if min_order_magnitude == np.floor(min_order_magnitude): ymin = 10 ** (np.floor(min_order_magnitude) - 1);
    else: ymin = 10 ** np.floor(min_order_magnitude);

    return ymin, ymax;

