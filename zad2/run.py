import subprocess
import os

directory = './output/'
if not os.path.exists('output'):
    os.makedirs('output')

acceptable_error = [0.1, 0.01]
learning_rate = [0.001, 0.0001]
momentum = [0.001, 0.0001]
hidden_size = [1, 2, 3, 4, 5]
bias_switch = [0, 1]
lower_limit = 1
upper_limit = 100
set_size = [25, 50]

for ss in set_size:
    for ae in acceptable_error:
        for lr in learning_rate:
            for m in momentum:
                for hs in hidden_size:
                    for bs in bias_switch:
                        path = directory + str(ae) + '_' + str(lr) + '_' + str(m) + '_' + str(hs) + '_' + str(bs) + '_' + str(ss)
                        if not os.path.isfile(path + '.txt'):
                            subprocess.call(['python', 'main.py', str(ae), str(lr), str(m), str(hs), str(bs),
                                             str(lower_limit), str(upper_limit), str(ss), str(path)])
