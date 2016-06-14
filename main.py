# main.py

import sys
from optparse import OptionParser
from thread import start_new_thread
from random import randint
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
    parser.add_option('-n', '--number', dest='number', type='int', default=10)
    parser.add_option('-z', '--zoom', dest='size', type='int', default=16)
    parser.add_option('-d', '--delay', dest='delay', type='float', default=0.2)
    parser.add_option('--no_display', action='store_false', dest='display', default=True)

    (options, otherjunk) = parser.parse_args(argv)
    if len(otherjunk) != 0:
        raise Exception('Command line input not understood: ' + str(otherjunk))

    arguments = {}

    arguments['layout'] = getLayout(options.layout)
    if arguments['layout'] is None: raise Exception('The layout ' + options.layout + " can't be found.")

    arguments['display'] = options.display
    arguments['number'] = options.number
    arguments['size'] = options.size
    arguments['delay'] = options.delay

    return arguments

def run():
    print(simulation.run(args['display'], args['delay']))
    app.quit()

def randomStartEndPoint(number=5):
    pos = {}
    for _ in range(number):
        while True:
            r = randint(0, len(carmap.roads) - 1)
            i = randint(0, carmap.roads[r].getDistance() - 1)
            if not (r, i) in pos:
                pos[(r, i)] = carmap.roads[r].getPosByIndex(i)
                break
    result = []
    for (ri, p) in pos.iteritems():
        while True:
            r = randint(0, len(carmap.roads) - 1)
            i = randint(0, carmap.roads[r].getDistance() - 1)
            if ri != (r, i):
                result.append((p, carmap.roads[r].getPosByIndex(i)))
                break
    return result

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
    cars = randomStartEndPoint(args['number'])
    simulation = Simulation(cars, carmap)
    app = Graphic(mapLayout.mapInfo, carmap.cars, carmap.trafficlights, args['size'])

    if args['display'] is True:
        start_new_thread(run, ())
        app.run()
    else:
        run()
