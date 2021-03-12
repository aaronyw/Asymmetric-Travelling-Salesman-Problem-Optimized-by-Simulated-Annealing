import atsp, sys, time, multiprocessing as mp

#################
cores = 12  # how many threads you want to use? at least 2 please
epoch = 50  # at least 1, more epoch takes more time but reaches closer to the best result
regb = (0.3, 3)  # regularization_bound
initf = 20  # initial fitness for multiprocessing, more fitness takes more time but reaches closer to the best result
initc = None  # initial solution in an array format
#################

def addajob(bestres, sil_mod=True):
    global processes, epoch, initf

    def tsplib(init_sol):
        _atsp = atsp.SA(data, regularization_bound=regb, initial_fitness=initf, initial_solution=init_sol, silent_mode=sil_mod)
        output.put(_atsp.solve())

    if epoch > 0:
        _job = mp.Process(target=tsplib, args=(bestres,))
        processes.append(_job)
        _job.start()
        epoch -= 1
        initf += 1

if len(sys.argv) == 2:
    with open(sys.argv[1], 'r') as fp:
        data = list(map(int, fp.read().split()))
        output = mp.Manager().Queue()
        res, processes = ([], float('inf')), []
        addajob(initc, False)
        time.sleep(1)
        n = 2
        while processes:
            _job = processes.pop(0)
            _job.join()
            _candidate = output.get()
            if _candidate[1] and _candidate[1] < res[1]:
                res = _candidate
            if epoch:
                for _ in range(min(n, cores) - len(processes)):
                    addajob(res[0])
            n += 1
        print(' OPTIMIZED COST:', res[1])
        print(' '.join(map(str, res[0])))
