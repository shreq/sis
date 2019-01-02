import dill
import numpy


def mean_square_error(func, xinput, xoutput):
    ans = 0
    for x in range(len(xoutput)):
        ans += ((func(xinput[x]).T - xoutput[x]) ** 2)
    return numpy.sum(ans) / len(xoutput)


def save(obj, path):
    with open(path, 'wb') as f:
        dill.dump(obj, f)


def load(path):
    with open(path, 'rb') as f:
        return dill.load(f)


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def load_args(args):
    if len(args) > 1 and is_number(args[1]):
        acceptable_error = args[1]
    else:
        acceptable_error = 0.01

    if len(args) > 2 and is_number(args[2]):
        learning_rate = args[2]
    else:
        learning_rate = 0.0001

    if len(args) > 3 and is_number(args[3]):
        momentum = args[3]
    else:
        momentum = 0.0001

    if len(args) > 4 and is_number(args[4]):
        hidden_size = args[4]
    else:
        hidden_size = 5

    if len(args) > 5 and (is_number(args[5]) or args[5].lower() == 'true' or args[5].lower() == 'false'):
        if is_number(args[5]):
            if float(args[5]) > 0:
                bias_switch = 1
            else:
                bias_switch = 0
        elif args[5].lower() == 'true':
            bias_switch = 1
        else:
            bias_switch = 0
    else:
        bias_switch = 1

    if len(args) > 6 and is_number(args[6]):
        lower_limit = args[6]
    else:
        lower_limit = 1

    if len(args) > 7 and is_number(args[7]):
        upper_limit = args[7]
    else:
        upper_limit = 100

    if len(args) > 8 and is_number(args[8]):
        set_size = args[8]
    else:
        set_size = 100

    if len(args) > 9:
        path = args[9]
    else:
        path = "network"

    return float(acceptable_error), \
           float(learning_rate), float(momentum), \
           int(hidden_size), float(bias_switch), \
           int(lower_limit), int(upper_limit), int(set_size), \
           str(path)
