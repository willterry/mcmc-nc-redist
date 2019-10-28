import tree

import importlib

importlib.reload(tree)

def setExtensionData(state, info):
    state["extensions"] = set([])
    if info["proposal"] == "mergeSplit":
        state["extensions"].add("spanningTrees")
        if info["parameters"]["gamma"] != 0:
            state["extensions"].add("spanningTreeCounts")
    return state

def extendState(state, info, computeE):
    state = setExtensionData(state, info)

    rng = info["rng"]

    if "spanningTrees" in state["extensions"]:
        state["districtTrees"] = {}
        for di in state["districts"]:
            district = state["districts"][di]
            state["districtTrees"][di] = tree.wilson(district, rng)
    if "spanningTreeCounts" in state["extensions"]:
        state["spanningTreeCounts"] = {}
        for di in state["districts"]:
            district = state["districts"][di]
            state["spanningTreeCounts"][di] = tree.nspanning(district)

    state["energy"] = computeE(state, info)

    return state

def updateState(newdistricts, state, info):

    for di in newdistricts["districts"]:
        district = newdistricts["districts"][di]
        state["districts"][di] = district

    state["nodeToDistrict"] = newdistricts["nodeToDistrict"]
    
    if "spanningTrees" in state["extensions"]:
        for di in newdistricts["districtTrees"]:
            districtTree = newdistricts["districtTrees"][di]
            state["districtTrees"][di] = districtTree
    if "spanningTreeCounts" in state["extensions"]:
        for di in newdistricts["spanningTreeCounts"]:
            spanningTreeCount = newdistricts["spanningTreeCounts"][di]
            state["spanningTreeCounts"][di] = spanningTreeCount
    state["energy"] = newdistricts["energy"]
    return state
