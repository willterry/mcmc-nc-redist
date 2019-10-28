import networkx as nx
import operator

import constraints
import initializer
import tree

import importlib

importlib.reload(constraints)
importlib.reload(initializer)
importlib.reload(tree)


def searchForDistrict(graph, rng, state, info, remainingPop, attemptPerDist, 
                      boolop):    
    for attempt in range(attemptPerDist):
        graphTree = tree.wilson(graph, rng)

        cutSet, edgeWeights = {}, {}
        try:
            cutSet, edgeWeights = tree.edgeCuts(graphTree, remainingPop, state, 
                                                info, boolop)
        except:
            state = initializer.determineStateInfo(state, info)
            cutSet, edgeWeights = tree.edgeCuts(graphTree, remainingPop, graph, 
                                                info, boolop)
        if cutSet:
            break
    return cutSet, edgeWeights, graphTree

def extractDistrictsFromCutTree(graphTree, graph, state, districts):
    distGraph = state["graph"]

    for conComp in nx.connected_components(graphTree):
        popConComp = sum([distGraph.nodes[n]["Population"] 
                          for n in conComp])
        if state["minPop"] <= popConComp <= state["maxPop"]:
            districts[len(districts)] = graph.subgraph(conComp).copy()
            graph.remove_nodes_from(conComp)
    return districts, graph

def assignDistricts(districts, state):
    state["districts"] = districts

    nodeToDistrict = {}
    for dist in districts:
        for n in districts[dist].nodes:
            nodeToDistrict[n] = dist
    state["nodeToDistrict"] = nodeToDistrict

    return state

def attemptMakePlan(state, info, attemptPerDist = 20):
    if "seedAttemptsByDist" in info["parameters"]:
        attemptPerDist = info["parameters"]["seedAttemptsByDist"]
    numDist = info["parameters"]["districts"]
    rng = info["rng"]
    distGraph = state["graph"]
    graph = distGraph.copy()

    districts = {}
    
    cuts = numDist - 1
    for distCut in range(cuts):
        boolop = operator.and_ if distCut == cuts-1 else operator.or_

        remainingPop = sum([distGraph.nodes[n]["Population"] 
                            for n in graph.nodes])
        
        cutSet, edgeWeights, graphTree = searchForDistrict(graph, rng, state, 
                                                           info, remainingPop,
                                                           attemptPerDist, 
                                                           boolop)
        if not cutSet:
            return state, False
    
        orderedCutSet = sorted(list(cutSet), 
                               key=lambda e:''.join(sorted(list(e))))
        e = rng.choice(orderedCutSet)
        
        graphTree.remove_edge(*e)

        districts, graph = extractDistrictsFromCutTree(graphTree, graph, state, 
                                                       districts)

    state = assignDistricts(districts, state)
    
    popCheck = constraints.checkPopulation(state)
    distCheck = len(districts) == numDist
    
    return state, popCheck and distCheck

def contructPlan(state, info, maxAttempts = 1000):
    '''Finds a random districting.'''

    for attempt in range(maxAttempts):
        state, success = attemptMakePlan(state, info)
        if success:
            break
    if not success:
        raise Exception("Could not find acceptable initial state")
    return state