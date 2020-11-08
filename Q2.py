import numpy as np
from itertools import permutations as p, combinations as c, product as pp
import math
import copy
import time

# Custom, ascending, bin insertion, specialPop features, key=1
class pqueue(): 
    def __init__(self, items = [], key = 1):
        self.q = items
        self.order = True
        self.key = key
    def size(self):
        return len(self.q)
    def peek(self):
        if self.q:
            if self.order: return self[0]
            else: return self[-1]
        else: return None
    def insert(self, item):
        if type(item) != list and type(item) != tuple: item = [item]
        lower = -1
        higher = self.size()
        k = self.key
        mid = (lower+higher) // 2
        while lower != mid:
            if self.q[mid][k] == item[k]: break
            elif self.q[mid][k] < item[k]: lower = mid
            else: higher = mid
            mid = (lower+higher) // 2
        self.q = self.q[:mid+1] + [item] + self.q[mid+1:]
    def pop(self, idx=0):
        return self.q.pop(idx)
    def sPop(self, boo):
        for idx,a,b,c in enumerate(self.q):
            if c == boo: return self.q.pop(idx)

def computeLowestCost(taxPerProduct, costPerTransaction, tests):
##    Create adj matrix
    n = len(taxPerProduct)
    adj = list(map(lambda x: [], [None]*(n+5)))
    taxList = list(map(lambda x: 0, [None]*(n+5)))
    for node, neigh, cost in costPerTransaction:
        adj[node].append( (neigh,cost) )
    for idx,tax in taxPerProduct:
        taxList[idx] = tax
    answer = []

    startSet, endSet = set(), set()
    testSet = set( list( map(lambda x: tuple(x),tests) ) )
    
    for startPt, endPt in testSet:
        startSet.add(startPt)
        endSet.add(endPt)
    workspace = pqueue()
    for startPt in startSet: # Road, Cost, RoadBool, (TaxPaid,CostofNode)
        workspace.insert( ([startPt],0,True) )
        workspace.insert( ([startPt],0,False) )

    answerHash = {}
    while len(testSet) > 0:
        road, roadCost, roadBool = workspace.pop()
        prevNode = road[-1]
        routeMap = (road[0],road[-1])
        if routeMap in testSet:
            testSet.remove(routeMap)
            answerHash[routeMap] = roadCost
            print(road, roadCost)
        if roadBool and len(road) > 1 and  road[-2] != None: # Pay tax
            tempRoad = road[:-1] + [None] + road[-1:]
            workspace.insert( (tempRoad, roadCost + taxList[prevNode], roadBool) )
            continue
        for neigh, cost in adj[prevNode]:
            workspace.insert( (road + [neigh], roadCost + cost , not roadBool) )
    return list(map( lambda x: answerHash[tuple(x)], tests))

'''
[[0, 0], [1, 9999], [2, 9999], [3, 5], [4, 3], [5, 1], [6, 9999]]
[[0, 3, 10], [0, 1, 2], [1, 3, 4], [1, 2, 1], [3, 4, 7], [3, 2, 2], [2, 4, 1], [2, 6, 5], [2, 5, 9], [4, 6, 3], [6, 5, 1]]
[[0, 6], [0, 5]]
output : 18 21
'''

taxPerProduct = [ (0,0),(1,1),(2,6),(3,900) ]
costPerTransaction = [ (0,2,10),(0,1,2),(1,2,4),(2,3,2) ]
tests = [ (0,3) ]

taxPerProduct = [[0, 0], [1, 9999], [2, 9999], [3, 5], [4, 3], [5, 1], [6, 9999]]
taxPerProduct = [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0]]
costPerTransaction = [[0, 3, 10], [0, 1, 2], [1, 3, 4], [1, 2, 1], [3, 4, 7], [3, 2, 2], [2, 4, 1], [2, 6, 5], [2, 5, 9], [4, 6, 3], [6, 5, 1]]
tests = [[1, 4],[0, 6], [0, 5]]
tic = time.perf_counter()
x = computeLowestCost(taxPerProduct, costPerTransaction, tests)
print(x)
toc = time.perf_counter()

print(f'Completed in {toc - tic:0.5f}s')
print()
