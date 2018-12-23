from network import Network
from common import mean_square_error, load, load_args
import numpy
from sys import argv

acceptable_error, learning_rate, momentum, hidden_size, bias_switch, lower_limit, upper_limit, set_size = load_args(argv)
print('lower limit:     \t' + str(lower_limit) + '\n' +
      'upper limit:     \t' + str(upper_limit) + '\n' +
      'set size:        \t' + str(set_size) + '\n')

# start
input_list = []
target_list = []
# network = Network(1, hidden_size, 1, learning_rate, bias_switch, momentum)

# load last setup
network = load('network.ser')
# network.w_ih = load('w_ih.ser')
# network.w_ho = load('w_ho.ser')
# network.b_ih = load('b_ih.ser')
# network.b_ho = load('b_ho.ser')

# generate testing sets
for i in range(set_size):
    r = numpy.random.randint(lower_limit, upper_limit + 1)
    input_list.append(r)
    target_list.append(numpy.sqrt(r))

# test
error = 10
error_ar = []
for j in range(len(input_list)):
    error_ar.append(mean_square_error(network.query, input_list, target_list))
error = numpy.sum(error_ar) / len(error_ar)

print('error = ' + str(error))
