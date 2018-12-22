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
network = Network(1, 5, 1, 0.1, 1, 0.2)

# for i in range(100):
#     r = numpy.random.randint(1, 100)
#     input_list.append(r)
#     target_list.append(numpy.sqrt(r))

# input_list.append(81)
# target_list.append(9)
input_list.append(4)
target_list.append(2)

i = 0
e = 10
while i < 10 ** 10 and e > 0.00001:
    error_ar = []
    for j in range(len(input_list)):
        network.train(input_list[j], target_list[j])
        error_ar.append(mean_square_error(network.query, input_list, target_list))
    e = numpy.sum(error_ar) / len(error_ar)
    # if i % 5000 == 0:
    print(str(i) + '\terror = ' + str(e))
    i += 1
