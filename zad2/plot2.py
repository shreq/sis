from common import load, load_args
import numpy
import os
from sys import argv

#acceptable_error, learning_rate, momentum, hidden_size, bias_switch, lower_limit, upper_limit, set_size, path = load_args(argv)

# start
input_list = []
target_list = []
for i in range(101):
    input_list.append(i)
    target_list.append(numpy.sqrt(i))

directory = os.fsencode('./output/saves/')
if not os.path.exists('./output/numbers'):
    os.makedirs('./output/numbers')

output = []
filenames = []
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    filenames.append(filename)
    filename_split = filename.split('_')
    if filename_split[0] == '0.01' and filename_split[5] == '50.ser':
        network = load('./output/saves/' + filename)
        #for j in range(len(input_list)):
        output.append(network.query)

for file, o in zip(filenames, range(len(input_list))):
    with open('./output/numbers/' + file + '.txt', 'w') as f:
        for i in range(len(input_list)):
            f.write(str(target_list[i]) + '\t' + str(output[o][i]) + '\n')
