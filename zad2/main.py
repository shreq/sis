# sieć neuronowa typu wielowarstwowy perceptron
# nauczaną metodą wstecznej propagacji błędu
# ma nauczyć się obliczania pierwiastka drugiego stopnia liczby
# nauczyć przy użyciu wejściowego wektora liczb losowych z zakresu 1-100

from Network import Network
import numpy


def mean_square_error(func, xinput, xoutput):
    ans = 0
    for x in range(len(xoutput)):
        ans += ((func(xinput[x]).T - xoutput[x]) ** 2)
    return numpy.sum(ans) / len(xoutput)


input_list = []
target_list = []

for i in range(100):
    r = numpy.random.randint(1, 100)
    input_list.append(r)
    target_list.append(numpy.sqrt(r))

i_nodes = 1
h_nodes = 10
o_nodes = 1
lr = 0.3
bias = 1
momentum = 0.1
network = Network(i_nodes, h_nodes, o_nodes, lr, bias, momentum)
error_ar = [0]
error = 1

i = 0
while error/len(error_ar) > 0.1 and i < 200:
    error_ar = []
    error = 0
    for j in range(len(input_list)):
        network.train(input_list[j], target_list[j])
        f = network.query
        error_test = mean_square_error(f, input_list, target_list)
        error += error_test
        error_ar.append(error)
    i += 1
    print(str(i) + '\terror ' + str(error/len(error_ar)))
