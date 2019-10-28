import importlib
import math

import constructor
import energy
import mergeSplit
import stateExt 
import tree
import writer

importlib.reload(constructor)
importlib.reload(energy)
importlib.reload(mergeSplit)
importlib.reload(stateExt)
importlib.reload(tree)
importlib.reload(writer)

exp = lambda x: math.exp(min(x, 700)) #>~700 overflows

################################################################################

def run(state, proposal, info):
    '''General MCMC districting. Energy function is (global) ENERGY_LOOKUP[i]
       if i is int, else energy function is i. Proposal function is (inputted) 
       proposal_f.'''
    rng = info["rng"]
    computeEnergy = energy.getEnergyFunction(info)
    state = stateExt.extendState(state, info, computeEnergy)
    writer.setupOutputs(state, info)
    initialStep = info["parameters"]["step"]
    finalStep = info["parameters"]["steps"]
    writer.recordState(initialStep, state, info)
    writer.recordStateData(initialStep, state, info)
    
    for step in range(initialStep, finalStep):
        (newdistricts, p, d1, d2) = proposal(state, info)
        if newdistricts == None:
            continue
        newdistricts["energy"] = computeEnergy(state, info, newdistricts)
        p *= exp(state["energy"] - newdistricts["energy"])
        if rng.random() < p:
            state = stateExt.updateState(newdistricts, state, info)
            writer.recordState(step, state, info)
            writer.recordStateData(step, state, info)

    return state
