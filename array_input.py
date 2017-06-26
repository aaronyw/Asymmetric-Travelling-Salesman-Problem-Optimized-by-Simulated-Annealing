import atsp, sys


if len(sys.argv) == 2:
    with open(sys.argv[1], 'r') as fp:
        content = fp.read().split()
        atsp = atsp.ATSP(list(map(int, content)), regularization_boundary=(0.33, 3.3))
        res = atsp.solve()
        if res[1]:
            print('OPTIMIZED COST:', res[1])
            print(' '.join(map(str, res[0])))
        else:
            print('NO SOLUTION')