import os
import random
import sys

import constructor
import districtingGraph
import initializer
import mergeSplit
import metropolisHastings
# import dataWriter

from importlib import reload

reload(constructor)
reload(districtingGraph)
reload(initializer)
reload(mergeSplit)
reload(metropolisHastings)

print('initializing run...')
state, args = initializer.setRunParametersFromCommandLine(sys.argv)

proposal, args = mergeSplit.define(args)
info = args

info = initializer.fillMissingInfoFields(info)
state = initializer.determineStateInfo(state, info)
state = constructor.contructPlan(state, info)
print('run initialized...')

print('starting chain...')
state = metropolisHastings.run(state, proposal, info)
print('finishing chain...')
