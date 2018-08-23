"""
Name: Models of Complex Networks
Author: Pablo Eliseo Reynoso Aguirre
Date: April 17, 2017
Desrcription: The task involves implementation of generators for complex network models.

                a)Erdos - Renyi (ER) networks G(N, K), G(N, p) Considering K,p = {0.00, 0.01, 0.02, 0.03, 0.05, 0.1}
                b)Barabasi & Albert(BA) Considering preferential attachment m = 1, 2, 4, 10
                c)Configuration Model(CM) Considering Poisson (ER) = 2, 4; power-law (SF) gamma = 2.2, 2.5, 2.7, 3.0

                e) Plots of some of the small size generated networks as N=50 (ER, WS), N=100 (BA, CM)
                f) Plots of the degree distributions, including the theoretical values (corresponding to the selected parameters) and the experimental ones (for the generated network)
                g) Estimation of the exponent for the empirical degree distributions of BA and CM (SF)


"""


from A2_nets import ErdosRenyi as ER;
from A2_nets import BarbasiAlbert as BA;
from A2_nets import ConfigurationModel as CM;


num_bins = 10;
n = 100;
gammas = [2.0,2.2,2.5,2.7,3.0,4.0];
probabilities = [0.01,0.02,0.03,0.05,0.1,0.2,0.5];

#Erdos - Renyi
erdos_renyi = False;
if erdos_renyi:
    for p in probabilities:

        G = ER.ErdosRenyi(n, p);
        G.generate_network_model();
        G.plot_degree_distribution(num_bins, save=True);
        G.plot_original_distribution(save=True);
        G.draw_network_graph(save=True);
        G.print_network_model_info();


####Exponent Estimation in Barbasi-Albert and Configuration-Model Networks

#Barbasi - Albert Model
barbasi_albert = False;

if barbasi_albert:

    for p in probabilities:

        G = BA.BarabasiAlbert(n, p);
        G.generate_network_model();
        G.plot_degree_distribution(num_bins, save=True);
        G.plot_original_distribution(save=True);
        G.draw_network_graph(save=True);
        exponent_ba = G.exponent_estimation(num_bins);
        G.print_network_model_info(exponent_ba);

#Configuration Model

configuration_m = True;

if configuration_m:
    for g in gammas:

        G = CM.ConfigurationModel(n, gamma=g);
        G.generate_network_model();
        G.plot_degree_distribution(num_bins, save=True);
        G.plot_original_distribution(save=True);
        G.draw_network_graph(save=True);
        exponent_cm = G.exponent_estimation(num_bins);
        G.print_network_model_info(exponent_cm);