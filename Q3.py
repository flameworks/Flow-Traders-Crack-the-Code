import numpy as np
from itertools import permutations as p, combinations as c, product as pp
import math
import copy
import time

def orderingSystem(order, grid, shares):
    orderSet, cost = [], 0
    for idx, node in enumerate(order):
        if node not in orderSet:
            if idx == 0: minDisc = 0
            else: minDisc = min( grid[ order[:idx] , node] )
            cost += shares[node] + minDisc
            orderSet.append(node)
    return cost, orderSet

def leastCost(refChart, shares):
    # Process Data
    n = len(refChart)
    grid = np.array(list(map(lambda x: list(x), refChart))).astype(int)
    grid = np.where(grid > 1, grid, 1) # floor everything to 1 EUR / share
    np.fill_diagonal(grid,1)
    basicSeeds = set(np.where( grid.sum(axis=0) == n)[0]) # Unavoidable investors

    grid = np.ceil(shares/grid).astype(int) - shares # cost saved if chosen

    gridMins = grid.min(axis=0)
    minHash = {} # Know which additions are variable mins
    for i in range(n):
        for j in range(n):
            if grid[i,j] == gridMins[j]:
                minHash[i] = minHash.setdefault(i,[]) + [j]

    # Start off with buying unavoidable shares then force buy from nth investor
    resultsArr = []
    for seed in range(n):
        road = list(basicSeeds)
        if seed not in basicSeeds: 
            road = list(basicSeeds) + [seed]
        roadLen = len(road) - 1
        while roadLen != len(road):
            roadLen = len(road)
            refs = set()
            for node in road:
                refs.update( minHash.setdefault(node,[]) )
            if len(refs) == 0: break
            for node in refs:
                if node not in road: road.append(node)
        resultsArr.append(road)

    # Front back merging
    if len(resultsArr) == 0: return 0
    finalRoad = resultsArr.pop(0)
    uniqLen = len(finalRoad)
    for road in resultsArr:
        cost1, r1 = orderingSystem( finalRoad + road , grid, shares)
        cost2, r2 = orderingSystem( road + finalRoad , grid, shares)
        if cost1 > cost2: r1,cost1  = r2,cost2
        if len(r1) >= uniqLen:
            finalRoad = r1
            uniqLen = len(finalRoad)
    return orderingSystem( finalRoad , grid, shares) [0]


refChart = ['1542','7935','1139','8882']
shares = [150,150,150,150] #205

tic = time.perf_counter()
x = leastCost(refChart, shares)
print(x, 205)
toc = time.perf_counter()


refChart = ['070','500','140']
shares = [150,150,150] #218

tic = time.perf_counter()
x = leastCost(refChart, shares)
print(x, 218)
toc = time.perf_counter()

refChart = ['07','40']
shares = [150,10] #48

tic = time.perf_counter()
x = leastCost(refChart, shares)
print(x, 48)
toc = time.perf_counter()

refChart = ['198573618294842',
            '159819849819205',
            '698849290010992',
            '000000000000000',
            '139581938009384',
            '158919111891911',
            '182731827381787',
            '135788359198718',
            '187587819218927',
            '185783759199192',
            '857819038188122',
            '897387187472737',
            '159938981818247',
            '128974182773177',
            '135885818282838']
shares = [157,1984,577,3001,2003,2984,5988,190003,9000,102930,5938,1000000,1000000,5892,38]
#260445


tic = time.perf_counter()
x = leastCost(refChart, shares)
print(x, 260445)
toc = time.perf_counter()
'''
refChart = ['02111111',
            '10711111',
            '11071111',
            '11104111',
            '41110111',
            '11111012',
            '11111301',
            '11111170']
shares = [28,28,28,28,28,28,28,28] #92
'''

refChart = ['1']
shares = [131]

tic = time.perf_counter()
x = leastCost(refChart, shares)
print(x, 92)
toc = time.perf_counter()

print(f'Completed in {toc - tic:0.5f}s')
print()
