import atsp

atsp = atsp.ATSP(list(map(int, input().split())), regularization_boundary=(0.3, 3))
res = atsp.solve()
if res[1]:
    print('OPTIMIZED COST:', res[1])
    print(' '.join(map(str, res[0])))
else:
    print('NO SOLUTION')