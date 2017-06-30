import atsp, sys, multiprocessing as mp

#################
cores = 8  # How many threads you want to use?
#################


def atsp_array(array):
    _atsp = atsp.SA(list(map(int, array)), regularization_bound=(0.3, 3), silent_mode=True)
    output.put(_atsp.solve())


if len(sys.argv) == 2:
    with open(sys.argv[1], 'r') as fp:
        content = fp.read().split()
        output = mp.Manager().Queue()
        res = ([], float('inf'))
        _processes = []
        for _ in range(cores):
            _processes.append(mp.Process(target=atsp_array, args=(content, )))
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
