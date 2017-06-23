# Asymmetric Travelling Salesman Problem Optimized by Simulated Annealing
**A python implementation for simulated annealing algorithm to optimize ATSP (Asymmetric Travelling Salesman Problem)**

Asymmetric TSP is a type of TSP that is on a directed graph which means paths may not exist in both directions between nodes or the distances might be different. Based on simulated annealing, this algorithm uses specific neighbouring candidate generation function designed for ATSP and is able to output a good enough result in a reasonable time.

---
### Data preparation
There are 2 types of data format:

1. full distance matrix as in TSPLIB - 
[check here for details about TSPLIB](http://elib.zib.de/pub/mp-testdata/tsp/tsplib/tsplib.html)

⋅⋅⋅Please note only ATSP type of TSPLIB file can be accepted. There is an example in the project file: ft53.atsp

2. as an array contains all edge information:

⋅⋅⋅if there is n nodes and m edges in ATSP graph, this array will be 1 + m*3 long started with n like this [n, U1, V1, W1, U2, V2, W2, ..., Um, Vm, Wm]. It represents:

⋅⋅*edge 1 is from U1 to V1 weighted W1
⋅⋅*edge 2 is from U2 to V2 weighted W2
⋅⋅⋅...
⋅⋅*edge m is from Um to Vm weighted Wm

⋅⋅⋅There is an example in the project file: case_101.txt

### Testing Examples

---
1. TSPLIB input example:

⋅⋅⋅```python tsplib_input.py ft53.atsp```

⋅⋅⋅Check ATSP_sol_ft53.txt for the best results I get so far. According to [TSPLIB](http://elib.zib.de/pub/mp-testdata/tsp/tsplib/sop-sol.html) this is the best known solution.

![ft53](http://i.imgur.com/nLlVhPX.png)

2. array input example:

⋅⋅⋅copy all content inside case_101.txt file, than run

⋅⋅⋅```python console_input.py```

⋅⋅⋅and paste everything inside the console

⋅⋅⋅Check ATSP_sol_101.txt for the best results I get so far.

![101](http://i.imgur.com/qRFqjAV.png)

## Adjusting the parameters

Please refer to the comments of atsp.py for the details of the each parameter.

Note that regularization_boundary parameter (especially the lower boundary) has very big impact on the algorithm behavior. Each data set may require different setting for this parameter and it is strongly recommended that to set learning_plot=True to see the graph to adjust lower boundary.

This is an example that the lower boundary is set too high that each temper seems random without descending:

![Ramdom](http://i.imgur.com/VNP3V3T.png)