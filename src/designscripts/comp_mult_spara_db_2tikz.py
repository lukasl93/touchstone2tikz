#!/usr/bin/python2
# -*- coding: utf-8 -*-

## @package mult_comp_spara_db_2tikz
# Function for Tikz File Creation via ClassTikzExport from the Sparameters
# of a Network from Scikit-RF
#
# Based on scikit-rf (skrf) http://scikit-rf-web.readthedocs.io/ \n
# Documentation at http://scikit-rf.readthedocs.io/en/latest/index.html
#
# Implementation of network can be found at:\n
# https://github.com/scikit-rf/scikit-rf/blob/master/skrf/network.py
#
# Currently reading Touchstone files and creating Tikz files by comparing
# this data is supported. You can also add own requirements to the plot.
#
# @date Created on 28.06.2017\n
# Last edited on 27.08.2017
#
# @author lukasl93


from skrf import Network
# import sys
# import os
# sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'basefiles'))
from TikzExport import ClassTikzExport
from ClassDataStructs import ClassData2D, ClassRequirements
from tikzhelpers import mean, get_frequnits


## Create Comparison Sparameter plot from multiple networks
# and multiple indexes
# @param networks Contains a list of the full Sparameterset
# of the DUT in a Network Object from scikit-rf
# @param frequnit The unit of the frequency to be plotted -
# String default 'GHz'
# @param indexes Tuplelist with the Parametersets to be plotted -\n
# Example [(2,1),(3,1)] equals plot S21 and S31 - Default [(1,1)] plot S11
# @param descriptions String array that contains the legenddescription
# for the plots specified in @parname{networks} in the same order
# @param requirements Requirements Object to be plotted last
# @param filename Contains the name or fullpath of the file to export to.
# @param linestyles String array with the linestyles
# (all options see ClassTikzExport::__tikzgs) for the graphs;\n
# Must be in the same order as the @parname{indexes} array.
# If not passed a sequence of predefined linetypes is used.
# Example: ['','-']
# @param colors String array with the color rgb values
# (regularly used options see ClassTikzExport::__tikzcol) for the graphs;
# Must be in the same order as the @parname{indexes} array.
# If not passed a sequence of predefined colors is used.
# Example: ['0.00000,0.44700,0.74100','0.85000,0.32500,0.09800']
def comp_mult_spara_db_2tikz(networks, frequnit='GHz', indexes=[(1, 1)],
                             descriptions=[''], requirements=[],
                             filename='test.tikz', linestyles=[], colors=[]):
    if not type(networks[0]) is Network:
        raise TypeError(
            "Wrong data type for sparam! Must be skrf Network.")
    networknames = ''
    colornames = []
    max_values = []
    min_values = []
    # Used for legend positioning in the right quarter
    lmeans = []     # lower mean values
    hmeans = []     # higher mean values
    # default options for yaxis label and thick graphs
    addopt = r'ylabel style={rotate=-90}'
    # additional options for graph settings
    graphopt = r''
    # if supplied with an empty indexes list:
    # show all sparams and adjust legend to matrix format
    if indexes:
        # if indexes list is very long use multicolum in legend
        if len(networks) + len(indexes) + len(requirements) > 5:
            addopt += r',legend columns=2,/tikz/column 2/.style={column sep=5pt}'
        elif len(networks) + len(indexes) + len(requirements) > 11:
            addopt += r',legend columns=3,/tikz/column 2/.style={column sep=5pt},/tikz/column 4/.style={column sep=5pt}'
        else:
            pass
    else:
        raise ValueError('indexes must not be empty!')

    for network in networks:
        networknames += network.name + ', '
        # just three entrys per line
        # if not (networks.index(network) + 1) % 3:
        #     networknames += '\n% '

    # create a new tikzplot
    tikzplot = ClassTikzExport()
    # add the header to the tikzfile with the current date
    tikzplot.addheader(filenames=networknames)
    # Temporary solution because i = networks.index(network)
    # causes an error, whyever ...
    i = 0
    t = 0
    for network in networks:
        j = 0
        for index in indexes:
            # i = networks.index(network)
            # define a color for each graph to be added
            colornames.append('colorNetw' + str(i) + str(j))
            # Use colors if given else use own defaults
            if len(colors) == len(networks):
                tikzplot.addcolor(colornames[t], colors[t])
            else:
                tikzplot.addcolor(
                    colornames[t],
                    tikzplot.get_collist()[t % len(tikzplot.get_collist())]
                )

            element = \
                [s[int(index[0]) - 1][int(index[1]) - 1] for s in network.s_db]
            # required for graph y boundaries
            max_values.append(max(element))
            min_values.append(min(element))
            # required for optimal legend positioning
            lmeans.append(mean(element[0:len(element) / 2]))
            hmeans.append(mean(element[len(element) / 2:len(element)]))
            # Temporary solution because i = networks.index(network)
            # causes an error, whyever ...
            j += 1
            t += 1
        i += 1

    if requirements:
        if type(requirements) is ClassRequirements:
            tikzplot.addcolor('requirement', requirements.graphcolor)
            max_values.append(max(requirements.data).yvalue)
            min_values.append(min(requirements.data).yvalue)
            lmeans.append(max(requirements.data).yvalue)
            hmeans.append(max(requirements.data).yvalue)
        else:
            for requirement in requirements:
                if not type(requirement) is ClassRequirements:
                    raise TypeError('Variable requirements must be of type ClassRequirements or a list with ClassRequirements Objects!')
                tikzplot.addcolor(
                    'requirement' + str(requirements.index(requirement)),
                    requirement.graphcolor
                )
                max_values.append(max(requirement.data).yvalue)
                min_values.append(min(requirement.data).yvalue)
                lmeans.append(max(requirement.data).yvalue)
                hmeans.append(max(requirement.data).yvalue)

    max_value = max(max_values)
    min_value = min(min_values)

    # Values below -40 dB will be cut off
    # due to non validity of measurement values for S-Parameters
    if min_value < -40:
        min_value = -40

    # range to add above and below the graph in y direction
    yaddr = int((max_value - min_value) * 0.1)
    if yaddr < 0.5:
        yaddr = 0.5

    # value of the middle of the y axis
    ymid = min_value + (max_value - min_value) / 2
    # chose quarter of the plot for the legendposition where the graphs
    # have the minimum mean distance to the middle of the plot
    # 1 | 0
    # ----- plotmiddle
    # 2 | 3
    legenddec = \
        [max(hmeans) - ymid, max(lmeans) - ymid,
            ymid - min(lmeans), ymid - min(hmeans)]
    legendposind = legenddec.index(min(legenddec))

    # Add plot optimized for S-Paramter plotting
    tikzplot.addconf(
        str(min(network.f) / get_frequnits()[frequnit]),
        str(max(network.f) / get_frequnits()[frequnit]),
        str(min_value - yaddr), str(max_value + yaddr),
        xunit=frequnit, yunit='dB', addoptions=addopt,
        legendpos=tikzplot.get_legendpositions()[legendposind][0],
        legendanchor=tikzplot.get_legendpositions()[legendposind][1])

    # Variable to keep track of amount of Graphs added
    t = 0
    i = 0
    # Add all the graphs to the plot
    for network in networks:
        for index in indexes:
            # Use linestyles if given else use own default
            if len(linestyles) == len(networks):
                tikzplot.addplot(colornames[t], linestyles[t],
                                 addoptions=graphopt)
            else:
                tikzplot.addplot(
                    colornames[t],
                    tikzplot.get_linestyles()
                    [t % len(tikzplot.get_linestyles())],
                    addoptions=graphopt
                )
            # Transform data to required format
            data = []
            for m in range(0, len(network.f), 1):
                data.append(
                    ClassData2D(
                        network.f[m] / get_frequnits()[frequnit],
                        network.s_db[m][int(index[0]) - 1][int(index[1]) - 1]
                    )
                )
            # Add data to plot
            tikzplot.adddata(data)
            # Add legend with description if given
            try:
                tikzplot.addlegend(str(index[0]) + str(index[1]),
                                   descriptions[i])
            except IndexError:
                tikzplot.addlegend(str(index[0]) + str(index[1]))
            # Temporary solution because i = networks.index(network)
            # causes an error, whyever ...
            t += 1
        i += 1

    # Add requirements if given:
    if requirements:
        if type(requirements) is ClassRequirements:
            tikzplot.addplot('requirement', requirements.linestyle,
                             addoptions='ultra thick')
            tikzplot.adddata(requirements.data)
            tikzplot.addlegend(label=requirements.legendentry)
            # filter empty string, beacuse then nothing is to do
            if requirements.reqtype:
                tikzplot.add_req_type_ind(requirements, 'requirement')
        else:
            for requirement in requirements:
                if not type(requirement) is ClassRequirements:
                    raise TypeError('Variable requirements must be of type ClassRequirements or a list with ClassRequirements Objects!')
                tikzplot.addplot(
                    'requirement' + str(requirements.index(requirement)),
                    requirement.linestyle, addoptions='ultra thick'
                )
                tikzplot.adddata(requirement.data)
                tikzplot.addlegend(label=requirement.legendentry)

            for requirement in requirements:
                # filter empty string, beacuse then nothing is to do
                if requirement.reqtype:
                    tikzplot.add_req_type_ind(
                        requirement,
                        'requirement' + str(
                            requirements.index(requirement))
                    )

    # Final thing to add to the Tikzpicture before export
    tikzplot.addfooter()
    # Export generated Tikzcode to file
    # in folder where this Classfile is located
    tikzplot.createTikzFile(filename)
