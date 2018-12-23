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
network = Network(1, 5, 1, 0.001, 1, 0.00001)

for i in range(100):
    r = numpy.random.randint(1, 100)
    input_list.append(r)
    target_list.append(numpy.sqrt(r))

# for i in range(2):
#     target_list.append(i)
#     input_list.append(i ** 2)

i = 0
error = 10
error_ar = []
while i < 10 ** 5 and error > 0.001:
    error_ar.clear()
    for j in range(len(input_list)):
        network.train(input_list[j], target_list[j])
        error_ar.append(mean_square_error(network.query, input_list, target_list))
    error = numpy.sum(error_ar) / len(error_ar)
    if i % 100 == 0:
        print(str(i) + '\t\terror = ' + str(error))
    i += 1

print(str(i) + '\t\terror = ' + str(error))
