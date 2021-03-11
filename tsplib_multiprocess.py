import sys, atsp, multiprocessing as mp

#################
cores = 16  # How many threads you want to use?
regb = (0.3, 3)  # regularization_bound
initf = 16  # initial fitness for multiprocessing
#################


def tsplib(data, init_sol):
    _atsp = atsp.SA(data, infinity=inf, regularization_bound=regb, initial_fitness=initf, initial_solution=init_sol, silent_mode=True)
    output.put(_atsp.solve())


if len(sys.argv) == 2:
    with open(sys.argv[1], 'r') as fp:
        content = fp.read().split()
        res = ([], float('inf'))
        idx = content.index('DIMENSION:') + 1
        n = int(content[idx])
        idx = content.index('EDGE_WEIGHT_FORMAT:') + 1
        flag = True
        if content[idx] != 'FULL_MATRIX':
            print('ATSP FILE MUST BE FULL MATRIX')
            flag = False
        idx = content.index('EDGE_WEIGHT_SECTION') + 1
        inf = int(content[idx])
        data = []
        for i in range(n):
            if len(content) > idx + n:
                data.append(list(map(int, content[idx:idx + n])))
            else:
                print('ATSP FILE FORMAT ERROR')
                flag = False
            idx += n
        
        if flag:
            print('Initializing:')
            init = atsp.SA(data, regularization_bound=regb).solve()
            print('Calculating:')
            output = mp.Manager().Queue()
            _processes = []
            for _ in range(cores):
                _processes.append(mp.Process(target=tsplib, args=(data, init[0],)))
            for _p in _processes:
                _p.start()
            for _p in _processes:
                _p.join()
            for _ in _processes:
                candidate = output.get()
                if candidate[1] and candidate[1] < res[1]:
                    res = candidate

            print(res[1])
            print(' '.join(map(str, res[0])))
