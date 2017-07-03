# Asymmetric Travelling Salesman Problem Optimized by Simulated Annealing
**A python implementation for simulated annealing algorithm to optimize ATSP (Asymmetric Travelling Salesman Problem)**

Asymmetric TSP is a type of TSP that is on a directed graph which means paths may not exist in both directions between nodes or the distances might be different. Based on simulated annealing, this algorithm uses specific neighbouring candidate generation function designed for ATSP and is able to output a very good result in a reasonable time.

---
### Data preparation
There are 2 types of accepted data format:

1. full distance matrix as in TSPLIB - 
[check here for details about TSPLIB](http://elib.zib.de/pub/mp-testdata/tsp/tsplib/tsplib.html)

Please note only ATSP type of TSPLIB95 file can be accepted. Check the example file: ft53.atsp

2. as an array contains all edge information:

if there is n nodes and m edges in ATSP graph, this array will be 1 + m*3 long started with n like this **_[n, U1, V1, W1, U2, V2, W2, ..., Um, Vm, Wm]_** which represents:

```
edge 1 is from U1 to V1 weighted W1

edge 2 is from U2 to V2 weighted W2

...

edge m is from Um to Vm weighted Wm
```

Check the example file: case_101.txt

---
### Testing examples

1. TSPLIB input example:

```
python tsplib_input.py ft53.atsp
```

Check ATSP_sol_ft53.txt for the best results I get so far. According to [TSPLIB](http://elib.zib.de/pub/mp-testdata/tsp/tsplib/sop-sol.html) this is the best known solution.

Plotted learning curve (a single red dot represents a temper):
![ft53](http://i.imgur.com/nLlVhPX.png)

Please note that since simulated annealing is randomized algorithm each run may have different result and the best known solution is not guaranteed. Multi-threading version can normally find better solution:

```
python tsplib_multiprocess.py ft53.atsp
```

2. array input example:

```
python console_input.py case_101.txt
```

Check ATSP_sol_101.txt as an sample results.

Plotted learning curve:
![101](http://i.imgur.com/qRFqjAV.png)

The best solution (4756) I get is from multi-threading version: 0 4 45 53 66 2 1 42 43 3 75 76 37 7 35 51 86 97 49 95 88 54 36 31 8 41 17 55 77 78 62 59 22 48 29 100 9 74 44 28 23 47 63 96 87 89 98 50 32 13 12 33 21 20 34 83 93 6 92 99 91 84 79 94 14 82 16 11 81 46 90 10 27 57 40 39 15 24 18 80 56 25 61 19 67 73 72 85 60 58 30 71 64 68 65 69 52 26 5 38 70 0

Try it yourself:

```
python console_multiprocess.py case_101.txt
```

---
## Adjusting the parameters

Please refer to the comments of atsp.py for the details of the each parameter.

Note that regularization_bound parameter (especially the lower bound) has very big impact on the algorithm behavior. Each data set may require different setting for this parameter and it is strongly recommended that to set learning_plot=True to see the graph to adjust lower bound.

This is an example that the lower bound is set too low that each temper seems random without descending:
![Ramdom](http://i.imgur.com/VNP3V3T.png)
