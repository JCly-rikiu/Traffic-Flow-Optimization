# main.py

import sys
from optparse import OptionParser
from thread import start_new_thread
from layout import getLayout
from car import CarMap
from graphic import Graphic
from simulate import Simulation
from ga import Gene, GeneInfo

def parseArgs(argv):
    """
    Parse the arguments.
    """

    parser = OptionParser()
    parser.add_option('-l', '--layout', dest='layout', type='str', default='single_cross')
    parser.add_option('--no_display', action='store_false', dest='display', default=True)

    (options, otherjunk) = parser.parse_args(argv)
    if len(otherjunk) != 0:
        raise Exception('Command line input not understood: ' + str(otherjunk))

    arguments = {}

    arguments['layout'] = getLayout(options.layout)
    if arguments['layout'] is None: raise Exception('The layout ' + options.layout + " can't be found.")

    arguments['display'] = options.display

    return arguments

def run():
    print(simulation.run(args['display'], 0.2))

if __name__ == '__main__':
    """
    > python main.py
    """

    args = parseArgs(sys.argv[1:])
    mapLayout = args['layout']
    gene = Gene(mapLayout.getTrafficLights())
    print(gene.geneStr)
    geneInfo = GeneInfo(gene)
    carmap = CarMap(mapLayout, geneInfo)
    simulation = Simulation([((7, 4), (10, 4)), ((6, 4), (10, 4)), ((21, 17), (21, 25)), ((5, 5), (25, 12))], carmap)
    app = Graphic(mapLayout.mapInfo, carmap.cars, carmap.trafficlights, 20)

    if args['display'] is True:
        start_new_thread(run, ())
        app.run()
    else:
        run()
