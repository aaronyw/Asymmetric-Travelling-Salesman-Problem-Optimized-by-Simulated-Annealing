import sys, atsp

if len(sys.argv) == 2:
    res = atsp.tsplib(sys.argv[1], learning_plot=True)
    print(res[1], res[0][1])
    print(' '.join(map(str, res[0][0])))
