import sys, atsp

if len(sys.argv) == 2:
    with open(sys.argv[1], 'r') as fp:
        content = fp.read().split()
        res = atsp.tsplib(content, learning_plot=True)
        print(res[1], res[0][1])
        print(' '.join(map(str, res[0][0])))
