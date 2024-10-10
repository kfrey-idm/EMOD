#!/usr/bin/python

import argparse
import json
import matplotlib.pyplot as plt
import pylab
import sys


class PlottingError(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)


def loadJsonFromFile(filename):
    data = {}
    try:
        handle = open(filename)
        text = handle.read()
        handle.close()
    except Exception as ex:
        raise PlottingError("Error opening/reading file - '%s'" % ex)
    try:
        data = json.loads(text)
    except Exception as ex:
        raise PlottingError("Error '%s' parsing text from '%s'" % (ex, filename))

    return data


def start_plotting(title):
    figure = plt.figure(1, figsize=(11.0, 8.5))  # in inches
    axes = figure.add_subplot(111)
    if title:
        axes.set_title(title)
    return figure, axes
    

def finish_plotting(save):
    plt.legend(loc='upper right')
    if save:
        filename = save + '.png'
        print("Saving chart to '%s'" % filename)
        try:
            pylab.savefig( filename, bbox_inches='tight', orientation='landscape', dpi=128 )
        except Exception as ex:
            print("Error '%s' saving chart to '%s'" % (ex, filename))
    plt.show()


def main(filename, title, channels, save):
    json_data = loadJsonFromFile(filename)
    (figure, axes) = start_plotting(title)

    try:
        for channel in channels:
            print('Plotting %s...' % channel)
            values = json_data['Channels'][channel]['Data']
            axes.plot(values, label=channel)
    except KeyError as ex:
        raise PlottingError("Didn't find entry %s of ['Channels']['%s']['Data'] in '%s'" % (ex, channel, filename))

    finish_plotting(save)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help='channel data filename [InsertChart.json]', nargs='?', default='InsetChart.json')
    parser.add_argument('-c', '--channels', action='append', help='channel[s] to display [SEIRW]', nargs='?', default=[], type=str)
    parser.add_argument('-t', '--title', help='Chart Title', type=str)
    parser.add_argument('-s', '--save', help='save to filename', type=str)
    args = parser.parse_args()
    
    try:
        # channels = processChannels(args.channels)
        
        print("Plotting '%s'" % args.filename)
        print("Displaying channels '%s'" % args.channels)
        print("Chart Title = '%s'" % args.title)
        print("Save filename = '%s'" % args.save)

        main(args.filename, args.title, args.channels, args.save)
    except PlottingError as pe:
        print(pe)
    except Exception as e:
        print("Caught exception '%s' during execution." % e)