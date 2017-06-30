import sys, atsp


def tsplib(content, f=1, r=None, learning_plot=False):
    idx = content.index('DIMENSION:') + 1
    n = int(content[idx])
    idx = content.index('EDGE_WEIGHT_FORMAT:') + 1
    if content[idx] != 'FULL_MATRIX':
        return [], 0
    idx = content.index('EDGE_WEIGHT_SECTION') + 1
    inf = int(content[idx])
    data = []
    for i in range(n):
        if len(content) > idx + n:
            data.append(list(map(int, content[idx:idx + n])))
        else:
            return [], 0
        idx += n

    _atsp = atsp.SA(data, initial_fitness=f, infinity=inf, regularization_bound=r, learning_plot=learning_plot)
    return _atsp.solve()


if len(sys.argv) == 2:
    with open(sys.argv[1], 'r') as fp:
        file_content = fp.read().split()
        res = tsplib(file_content, learning_plot=True)
        print(res[1], res[0][1])
        print(' '.join(map(str, res[0][0])))
