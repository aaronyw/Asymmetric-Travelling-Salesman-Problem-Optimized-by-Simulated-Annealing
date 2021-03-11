import atsp, sys, multiprocessing as mp

#################
cores = 16  # How many threads you want to use?
regb = (0.3, 3)  # regularization_bound
initf = 16  # initial fitness for multiprocessing
#################


def atsp_array(array, init_sol):
    _atsp = atsp.SA(list(map(int, array)), regularization_bound=regb, initial_fitness=initf, initial_solution=init_sol, silent_mode=True)
    output.put(_atsp.solve())


if len(sys.argv) == 2:
    with open(sys.argv[1], 'r') as fp:
        content = fp.read().split()
        output = mp.Manager().Queue()
        res = ([], float('inf'))
        print('Initializing:')
        init = atsp.SA(list(map(int, content)), regularization_bound=regb).solve()
        print('Calculating:')
        _processes = []
        for _ in range(cores):
            _processes.append(mp.Process(target=atsp_array, args=(content, init[0],)))
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
