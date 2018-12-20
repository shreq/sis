# sieć neuronowa typu wielowarstwowy perceptron
# nauczaną metodą wstecznej propagacji błędu
# ma nauczyć się obliczania pierwiastka drugiego stopnia liczby
# nauczyć przy użyciu wejściowego wektora liczb losowych z zakresu 1-100

import numpy
from Network import Network

input_list = []
target_list = []

for i in range(10):
    r = numpy.random.randint(1, 100)
    input_list.append(r)
    target_list.append(numpy.sqrt(r))

for i in range(10):
    error = []

    for j in range(1, 4):
        i_nodes = 1
        h_nodes = 4
        o_nodes = 1
        lr = 0.1
        bias = 1
        network = Network(i_nodes, h_nodes, o_nodes, lr, bias)
        w = 0
        error = []

        print('witam ' + str(i) + ' ' + str(j))

        for k in range(len(input_list)):
            print('halko ' + str(w) + ' ' + str(k))
            network.train(input_list[k], target_list[k])
            f = network.query

