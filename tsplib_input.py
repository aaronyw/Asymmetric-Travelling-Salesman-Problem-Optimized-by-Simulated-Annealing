import sys, atsp


def tsplib(content, learning_plot=True):
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

    _atsp = atsp.SA(data, learning_plot=learning_plot)
    return _atsp.solve()


if len(sys.argv) == 2:
    with open(sys.argv[1], 'r') as fp:
        file_content = fp.read().split()
        res = tsplib(file_content)
        print('OPTIMIZED COST:', res[1])
        print(' '.join(map(str, res[0])))
