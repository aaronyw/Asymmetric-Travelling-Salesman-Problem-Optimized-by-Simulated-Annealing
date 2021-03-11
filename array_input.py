import atsp, sys


if len(sys.argv) == 2:
    with open(sys.argv[1], 'r') as fp:
        content = fp.read().split()
        print(content)
        atsp = atsp.SA(list(map(int, content)), learning_plot=True)
        res = atsp.solve()
        if res[1]:
            print('OPTIMIZED COST:', res[1])
            print(' '.join(map(str, res[0])))
        else:
            print('NO SOLUTION')
