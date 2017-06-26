import math, random, matplotlib.pyplot as plt
from heapq import heappush, heappop


class ATSP:
    '''
    https://github.com/aaronyw/Asymmetric-Travelling-Salesman-Problem-Optimized-by-Simulated-Annealing.git
    '''
    def __init__(self, data, infinity=0, initial_t=0, rate=0.999, stopping_t=0.0001, initial_fitness=1, iteration_bound=None, regularization_bound=None, learning_plot=False):
        '''
        :param data: as full edge distance matrix or single line input (refer to README.md file)
        :param infinity: a large integer number that is larger than the cost of all possible solutions
        :param initial_t: initial temperature
        :param rate: the rate temperature decreases each iteration
        :param stopping_t: the final temperature accepted by algorithm
        :param initial_fitness: increase this number if algorithm failed to descend in early stage
        :param iteration_bound: the (minimal, maximum) iteration number accepted by algorithm; higher minimal iteration will increase the chance to find better solution
        :param regularization_bound: as (lower_bound, upper_bound) to regularize self.regulator
               - lower_bound affects how high each Tempering can go; the algorithm might fail to descend if this number is too small or fail to jump out of local minimal if this number is too large
               - upper_bound affects how flat the learning line can be; the Temper might lose its magic if this number is too large
        :param learning_plot: setting this as True will also output the detail info for each Temper
        '''
        self.INF = 99999 if not infinity else infinity
        self.rate = rate
        if isinstance(data[0], list):
            self.n = len(data)
            self.M = []
            for row in data:
                self.M.append([self.INF if x == infinity else x for x in row])
        else:
            self.n = data.pop(0)
            self.M = [[self.INF] * self.n for _ in range(self.n)]
            while data:
                u = data.pop(0)
                v = data.pop(0)
                weight = data.pop(0)
                if u != v:
                    self.M[u][v] = weight
        self.T_initial = self.T = math.sqrt(self.n) if not initial_t else initial_t
        self.T_stopping = stopping_t
        self.regularization_bound = (0.1, 7) if not regularization_bound else regularization_bound
        self.iteration_bound = [1 << 17, 1 << 24] if not iteration_bound else iteration_bound
        self.regulator = 1
        self.fitness = initial_fitness
        self.control = self.fitness + 1
        self.current_solution = self.initialization()
        self.current_cost = self.trip_cost(self.current_solution)
        self.initial_cost = self.current_cost
        self.best_solution = list(self.current_solution)
        self.best_cost = self.worst_cost = self.current_cost
        self.cost_list = [self.current_cost]
        self.reheat_x = []
        self.reheat_y = []
        self.detailed_info = learning_plot

    def trip_cost(self, candidate):
        array = candidate + [candidate[0]]
        res = 0
        for u, v in zip(array[:-1], array[1:]):
            res += self.M[u][v]
        return res

    def initialization(self):
        node = 0
        res = [node]

        array = list(range(1, self.n))

        while array:
            _array = list(self.M[node])
            _h = []
            for idx, val in enumerate(_array):
                heappush(_h, (val, idx))
            node = None
            while node not in array:
                node = heappop(_h)[1]

            array.remove(node)
            res.append(node)

        return res

    def accept(self, candidate, random_acceptance=True):
        res = False
        candidate_cost = self.trip_cost(candidate)
        if candidate_cost < self.current_cost:
            self.current_cost = candidate_cost
            self.current_solution = candidate
            if candidate_cost < self.best_cost:
                self.best_cost = candidate_cost
                self.best_solution = candidate
                res = True
        elif random_acceptance:
            if random.random() < math.exp((self.current_cost - candidate_cost)*self.regulator/self.T):  # probability function
                self.current_cost = candidate_cost
                self.current_solution = candidate
                res = True
            else:
                if self.current_cost > self.worst_cost:
                    self.worst_cost = self.current_cost

        self.T *= self.rate
        self.cost_list.append(self.current_cost)
        return res

    def anneal(self):
        def cycle(_idx):
            if _idx < 0:
                return self.n + _idx
            elif _idx < self.n:
                return _idx
            else:
                return _idx - self.n

        def transform(last):
            _shift = list(range(self.n - 1))
            random.shuffle(_shift)
            candidate = list(self.current_solution)
            for _i in _shift:
                if candidate[_i] not in last:
                    pivot = _i
                    X = candidate[pivot]
                    _shift.remove(pivot)
                    break
            a_idx = cycle(pivot - 1)
            b_idx = cycle(pivot + 1)
            A = candidate[a_idx]
            B = candidate[b_idx]
            for _i in _shift:
                c_idx = cycle(pivot + _i)
                C = candidate[c_idx]
                y_idx = cycle(c_idx + 1)
                Y = candidate[y_idx]
                d_idx = cycle(y_idx + 1)
                D = candidate[d_idx]
                if self.M[A][B] + self.M[Y][X] + self.M[X][D] < self.INF:
                    part_a = list(candidate[:d_idx])
                    part_b = list(candidate[d_idx:])
                    if X in part_a:
                        part_a.remove(X)
                    if X in part_b:
                        part_b.remove(X)
                    if self.accept(part_a + [X] + part_b):
                        return [X]
                if _i and self.M[A][Y] + self.M[Y][B] + self.M[C][X] + self.M[X][D] < self.INF:
                    new_c = list(candidate)
                    new_c[pivot], new_c[y_idx] = new_c[y_idx], new_c[pivot]
                    if self.accept(new_c):
                        return [X, Y]
            self.T *= self.rate
            self.cost_list.append(self.current_cost)
            return []

        nodes = []
        while self.T > self.T_stopping:
            nodes = transform(nodes)
            # if not nodes:
            #     self.T *= self.rate
            #     self.cost_list.append(self.current_cost)

    def solve(self):
        def sort_order(array):
            idx = array.index(0)
            return array[idx:] + array[0:idx + 1]

        def display(percentage, number):
            print('\r', end='')
            bar = [':']
            space = [' ']
            bar_n = math.ceil(percentage * 50)
            space_n = 50 - bar_n
            print(''.join(bar*bar_n + space*space_n) + '%s' % number, flush=True, end='')

        if self.detailed_info:
            print('Initialized: ', self.best_cost, '| Fitness:', self.fitness, '/', self.control)
        else:
            print(''.join(['FITNESS'] + [' ']*42), 'COST')
        last_best = self.current_cost + 1
        while self.current_cost < last_best and len(self.cost_list) < self.iteration_bound[1] and self.fitness > 0:
            if len(self.cost_list) > 1:
                self.T = self.T_initial
                self.regulator = max(self.regulator/(self.control - self.fitness), self.regularization_bound[0])
                if self.detailed_info:
                    print('Temper from', self.current_cost, 'at', len(self.cost_list), '| Fitness:', self.fitness, '/', self.control)
                else:
                    display(self.fitness/self.control, self.current_cost)
                # print(self.normalization)
                self.reheat_x.append(len(self.cost_list))
                self.reheat_y.append(self.current_cost)
            last_best = self.current_cost
            last_worst = self.worst_cost
            self.anneal()
            if self.current_cost < last_best:
                self.fitness += 1
                self.control += 1
                if self.current_cost == self.best_cost:
                    self.fitness += 1
                    # self.control += 1
                    # alternative:
                    if self.control <= self.fitness:
                        self.control = self.fitness + 1
                self.regulator = min(self.n/(last_best - self.current_cost), self.regularization_bound[1])
            else:
                self.fitness -= 1
                if self.worst_cost > last_worst:
                    self.fitness += 1
                    self.control = self.fitness + 1
                last_best = self.current_cost + 1
                if not self.fitness and len(self.cost_list) < self.iteration_bound[0]:
                    self.fitness = 3
                    if self.control <= 3:
                        self.control = 4
        if self.best_cost > self.INF:
            return sort_order(self.best_solution), 0  # indication that there might be NO solution for the problem
        if self.detailed_info:
            self.plot_learning()
        else:
            print()
        return sort_order(self.best_solution), self.best_cost

    def plot_learning(self):
        print(len(self.cost_list), 'iterations from', self.initial_cost, 'to', self.best_cost)
        plt.plot(list(range(len(self.cost_list))), self.cost_list)
        plt.plot(self.reheat_x, self.reheat_y, 'ro')
        plt.ylabel('Trip Cost')
        plt.xlabel('Iteration')
        plt.show()


def tsplib(content, f=1, r=None, learning_plot=False):
    idx = content.index('DIMENSION:') + 1
    n = int(content[idx])
    idx = content.index('EDGE_WEIGHT_FORMAT:') + 1
    if content[idx] != 'FULL_MATRIX':
        return ([], 0), 'ONLY ATSP WITH FULL_MATRIX IS ACCEPTED'
    idx = content.index('EDGE_WEIGHT_SECTION') + 1
    inf = int(content[idx])
    data = []
    for i in range(n):
        if len(content) > idx + n:
            data.append(list(map(int, content[idx:idx + n])))
        else:
            return ([], 0), 'TSPLIB FILE DOES NOT HAVE FULL_MATRIX'
        idx += n

    _atsp = ATSP(data, initial_fitness=f, infinity=inf, regularization_bound=r, learning_plot=learning_plot)
    res = _atsp.solve()
    if res[1]:
        return res, 'OPTIMIZED SUCCESSFULLY'
    else:
        return res, 'NO SOLUTION'