# main.py

import sys
from optparse import OptionParser
from thread import start_new_thread
from layout import getLayout
from car import CarMap
from graphic import Graphic
from simulate import Simulation

def parseArgs(argv):
    """
    Parse the arguments.
    """

    parser = OptionParser()
    parser.add_option('-l', '--layout', dest='layout', type='str', default='single_cross')
    parser.add_option('--no_display', action='store_false', dest='display')

    (options, otherjunk) = parser.parse_args(argv)
    if len(otherjunk) != 0:
        raise Exception('Command line input not understood: ' + str(otherjunk))

    arguments = {}

    arguments['layout'] = getLayout(options.layout)
    if arguments['layout'] is None: raise Exception('The layout ' + options.layout + " can't be found.")

    arguments['display'] = options.display

    return arguments


if __name__ == '__main__':
    """
    > python main.py
    """

    args = parseArgs(sys.argv[1:])
    carmap = CarMap(args['layout'])
    simulation = Simulation([((7, 4), (10, 4)), ((6, 4), (10, 4))], carmap)
    print(carmap.getDirection((7, 4), (10, 4)))
    app = Graphic(args['layout'].mapInfo, carmap.cars)

    start_new_thread(simulation.run, ())
    app.run()
