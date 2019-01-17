from common import load, load_args
import numpy
import os
import matplotlib.pyplot as plt

input_list = []
target_list = []
for i in range(101):
    input_list.append(i)
    target_list.append(numpy.sqrt(i))

directory = os.fsencode('./output/saves/')
if not os.path.exists('./output/charts'):
    os.makedirs('./output/charts')

output = []
temp = []
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    filename_split = filename.split('_')
    if filename_split[0] == '0.01' and filename_split[5] == '50.ser':
        network = load('./output/saves/' + filename)
        output.clear()
        for number in input_list:
            temp.clear()
            temp.append(number)
            output.append(network.query(temp)[0][0])
        plt.figure(0)
        plt.suptitle('Aproksymacja funkcji')
        plt.title('lr=' + filename_split[1] + ', momentum=' + filename_split[2] + ', hidden size=' + filename_split[3] + ', bias=' + filename_split[4])
        plt.xlabel('x')
        plt.ylabel('√x')
        plt.grid()
        test, = plt.plot(input_list, target_list, 'blue', label='wartości oczekiwane')
        approx, = plt.plot(input_list, output, 'red', label='wartości otrzymane')
        plt.legend(handles=[test, approx])
        plt.savefig('./output/charts/plot_'+filename+'.png')
        plt.clf()
