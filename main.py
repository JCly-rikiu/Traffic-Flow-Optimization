# main.py

import sys
import pickle
from optparse import OptionParser
from thread import start_new_thread
from random import randint
from layout import getLayout
from car import CarMap
from graphic import Graphic
from simulate import Simulation
from ga import Gene, GeneInfo
from generation import Generation

def parseArgs(argv):
    """
    Parse the arguments.
    """

    parser = OptionParser()
    parser.add_option('-l', '--layout', dest='layout', type='str', default='single_cross')
    parser.add_option('-n', '--number', dest='number', type='int', default=10)
    parser.add_option('-z', '--zoom', dest='size', type='int', default=16)
    parser.add_option('-d', '--delay', dest='delay', type='float', default=0.2)
    parser.add_option('-g', '--generation', dest='generation', type='int', default=20)
    parser.add_option('-a', '--amount', dest='amount', type='int', default=20)
    parser.add_option('-s', '--save', dest='save', type='str', default='save.p')
    parser.add_option('-r', '--load', dest='load', type='str', default='')
    parser.add_option('--no_display', action='store_false', dest='display', default=True)

    (options, otherjunk) = parser.parse_args(argv)
    if len(otherjunk) != 0:
        raise Exception('Command line input not understood: ' + str(otherjunk))

    arguments = {}

    arguments['layoutName'] = options.layout
    arguments['layout'] = getLayout(options.layout)
    if arguments['layout'] is None: raise Exception('The layout ' + options.layout + " can't be found.")

    arguments['display'] = options.display
    arguments['number'] = options.number
    arguments['size'] = options.size
    arguments['delay'] = options.delay
    arguments['generation'] = options.generation
    arguments['amount'] = options.amount
    arguments['save'] = options.save
    arguments['load'] = options.load

    return arguments

class Result(object):
    def __init__(self, layout, cars):
        self.layout = layout
        self.cars = cars

def save(obj, filename):
    pickle.dump(obj, open('saved/' + filename, 'wb'))

def load(filename):
    return pickle.load(open('saved/' + filename, 'rb'))

def run():
    print(simulation.run(args['display'], args['delay']))

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

    if args['load'] == '':
        mapLayout = args['layout']
        carmap = CarMap(mapLayout, None)
        cars = randomStartEndPoint(args['number'])
        g = Generation(mapLayout, carmap, cars, args['amount'], args['generation'])
        results = g.run()
        for r in results[::2]:
            (a, s) = r
            print('{0:.2f}'.format(a) + ' ' + s)
        print('---------------------------------')
        for r in results[1::2]:
            (a, s) = r
            print('{0:.2f}'.format(a) + ' ' + s)

        save(Result(args['layoutName'], cars), args['save'])
    else:
        r = load(args['load'])
        mapLayout = getLayout(r.layout)
        geneStr = raw_input('Input Gene String:')
        gene = Gene(mapLayout.getTrafficLights(), False, geneStr)
        geneInfo = GeneInfo(gene)
        carmap = CarMap(mapLayout, geneInfo)
        cars = r.cars
        simulation = Simulation(cars, carmap)

        if args['display'] is True:
            app = Graphic(mapLayout.mapInfo, carmap.cars, carmap.trafficlights, args['size'])
            start_new_thread(run, ())
            app.run()
        else:
            run()
