from network import Network
from common import mean_square_error, save, load_args
import numpy
from sys import argv
from time import time

acceptable_error, learning_rate, momentum, hidden_size, bias_switch, lower_limit, upper_limit, set_size, path = load_args(argv)
print('acceptable error:\t' + str(acceptable_error) + '\n' +
      'learning rate:   \t' + str(learning_rate) + '\n' +
      'momentum:        \t' + str(momentum) + '\n' +
      'hidden size:     \t' + str(hidden_size) + '\n' +
      'bias switch:     \t' + str(bias_switch) + '\n' +
      'lower limit:     \t' + str(lower_limit) + '\n' +
      'upper limit:     \t' + str(upper_limit) + '\n' +
      'set size:        \t' + str(set_size) + '\n')

# start
input_list = []
target_list = []
network = Network(1, hidden_size, 1, learning_rate, bias_switch, momentum)

# generate training sets
for epoch in range(set_size):
    r = numpy.random.randint(lower_limit, upper_limit + 1)
    input_list.append(r)
    target_list.append(numpy.sqrt(r))

# train
epoch = 0
error = 10
error_ar = []
start = time() * 1000
while epoch < 100000 and error > acceptable_error:
    error_ar.clear()
    for j in range(len(input_list)):
        r = numpy.random.randint(0, len(input_list))
        network.train(input_list[r], target_list[r])
        error_ar.append(mean_square_error(network.query, input_list, target_list))
    error = numpy.sum(error_ar) / len(error_ar)
    if epoch % 100 == 0:
        print(str(epoch) + '\t\terror = ' + str(error))
    epoch += 1
stop = time() * 1000

print('\n' + str(epoch) + '\t\terror = ' + str(error))

# save
save(network, path + '.ser')
# save(network.w_ih.tolist(), 'w_ih.ser')
# save(network.w_ho.tolist(), 'w_ho.ser')
# save(network.b_ih.tolist(), 'b_ih.ser')
# save(network.b_ho.tolist(), 'b_ho.ser')

with open(path + '.txt', 'w', encoding='utf-8') as f:
    f.write(str(error) + '\n')
    f.write(str(epoch) + '\n')
    f.write(str(format(stop - start, '.3f')))
