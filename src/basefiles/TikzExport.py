#!/usr/bin/python2
# -*- coding: utf-8 -*-

## @package TikzExport
# Provides two Classes
# (#TikzExport::ClassTikzExport and #TikzExport::ClassSpara2Tikz)
# to export Latex Tikz files.\n
#
# Tested with files exported from CST Microwave Studio 2017 SP2
#
# @date Created on 28.03.2017\n
#      Last edited 27.08.2017 by lukasl93
#
# @author lukasl93

import time
import os
from collections import OrderedDict
from string import Template
from ClassDataStructs import ClassData2D, ClassRequirements
from tikzhelpers import get_path_data_string


## @class ClassTikzExport
# [pgfplot]: http://ftp.uni-erlangen.de/ctan/graphics/pgf/contrib/pgfplots/doc/pgfplots.pdf "Latex pgfplot documentation"
# [din461]: https://de.wikipedia.org/wiki/DIN_461 "DIN 461"
# This Class provides the basic functions to create a [Latex pgfplot][pgfplot]
# line graph conform to [DIN 461][din461].
class ClassTikzExport(object):

    # Class Variables and Templates -------------------------------------------

    ## Possible Colors in one plot
    __tikzcol = [                   # Alternative
        '0.00000,0.44700,0.74100',  # RAL 5013
        '0.85000,0.32500,0.09800',  # RAL 2004
        '0.49400,0.18400,0.55600',
        '0.46600,0.67400,0.18800',  # RAL 6001
        '0.30100,0.74500,0.93300',  # RAL 5015
        '0.63500,0.07800,0.18400',
        '0.92900,0.69400,0.12500'   # RAL 3007
    ]   # Add: RAL 4006
    # replace yellow, change dark green to smaragdgreen

    ## Legendpositions in Mathematical Quarters of Graph\n
    # 1 | 0\n
    # -----\n
    # 2 | 3
    __tikzlegendpos = [
        ('(0.97,0.97)', 'north east'),  # top right [0]
        ('(0.03,0.97)', 'north west'),  # top left [1]
        ('(0.03,0.05)', 'south west'),  # bottom left [2]
        ('(0.97,0.05)', 'south east')   # bottom right [3]
    ]

    ## Tikz data lineend (linefeed in Latex)
    __tikzle = r'\\'

    ## Tikz data separator (tabulator in Latex)
    __tikzsep = '\t'

    ## Tikz graph styles (continuous, doted, line dot,...)
    __tikzgs = OrderedDict([
        ('', 'solid'),
        ('--', 'densely dashed'),
        ('-.-', 'densely dashdotted'),
        ('-..-', 'densely dashdotdotted'),
        ('- -', 'loosely dashed'),
        ('- .', 'loosely dashdotted'),
        ('- . .', 'loosely dashdotdotted'),
        ('-', 'dashed'),
        ('-.', 'dashdotted'),
        ('-..', 'dashdotdotted'),
        ('..', 'densely dotted'),
        ('.', 'dotted'),
        ('. .', 'loosely dotted')
    ])

    ## Header template for Tikzpicture
    __tikzheader = Template(
        r"""% This file was created by ClassTikzExport on ${date}.
%
% Created from the following input data files:
% ${filelist}
%
% The creation of uniform documentation is the main goal of this project.
% The author worked on his Master thesis during the creation of this framework.
%
% Tested header for the created Tikz files:
% \usepackage{tikz}
% \usepackage{pgfplots}
% add support for patterns for requirement
% \usetikzlibrary{patterns}
% \usepgfplotslibrary{fillbetween} % used for more noticeable requirements
% Addition for German number style in plots and small legend font:
% \pgfplotsset{compat=newest,every axis legend/.append style={font=\small},
%     x tick label style={/pgf/number format/.cd, set thousands separator={}}
% }
%
% Helpful command to include tikz files:
% \newcommand{\instikz}[2]{
%    \begin{figure}[hbtp]
%        \centering
%        \input{tikz/#1.tikz}
%        \caption{#2}
%        \label{plot:#1}
%    \end{figure}    
% }
%
% You need to set for example:
% \newlength\figureheight 
% \newlength\figurewidth 
% \setlength\figureheight{7cm} 
% \setlength\figurewidth{\textwidth}
% \addtolength{\figurewidth}{-2cm}
% before the inclusion of the first of these graphs in the latex document!
%
% Including then works like this:
% \instikz{<tikzfilename>}{<Description for the Picture>}

% Referencing the picture works with:
% \ref{plot:<tikzfileame>}
%""")

    ## Color template for Tikzpicture
    __tikzcolor = Template(r"\definecolor{${colorname}}{rgb}{${rgbval}}%")

    ## Config template for Tikzpicture
    __tikzconfig = Template(r"""\begin{tikzpicture}
%
\begin{axis}[%
width=0.951\figurewidth,
height=\figureheight,
at={(0,0)},
scale only axis,
xmin=${xmin},
xmax=${xmax},
ymin=${ymin},
ymax=${ymax},
xlabel={$$${xparam}/\mathrm{${xunit}} \rightarrow$$},
ylabel={$$\overset{\uparrow\vspace{0.5em}}{\cfrac{${yparam}}{\mathrm{$yunit}}}$$},
xmajorgrids,
xminorgrids,
ymajorgrids,
yminorgrids,
axis background/.style={fill=${bgcolor}},
axis x line*=bottom,
axis y line*=left,
legend style={at={${legendpos}},anchor=${legendanchor},
legend cell align=left,align=left,draw=${legendcolor}},
${addoptions}
]""")

    ## Plot template for Tikzpicture
    __tikzplot = Template(r"""\addplot [color=$plotcolor,style=$linestyle,$addopt]
table[row sep=crcr]{%""")

    ## Data template for Tikzpicture
    __tikzdata = Template(r"""$data
};""")

    ## Legend template for Tikzpicture
    __tikzlegend = Template(r"\addlegendentry{$label$desc};")

    ## Footer template for Tikzpicture
    __tikzfooter = Template(r"""\end{axis}
\end{tikzpicture}%""")

    ## Requirement template for Tikzpicture
    __tikzreq = Template(r"""\path[name path=$reqname1]
$reqdata1;
\path[name path=$reqname2]
$reqdata2;
\addplot[pattern=north west lines, pattern color=$reqcolorname]
fill between[
of=$reqname1 and $reqname2,
];""")

    # Class Functions --------------------------------------------------------

    ## Constructor
    def __init__(self):
        self.__fulltikzstring = ''

    ## Getter for linestyle list
    def get_linestyles(self):
        ## Helper to have a indexable form of the line styles
        return list(self.__tikzgs.keys())

    ## Getter for color list
    def get_collist(self):
        return self.__tikzcol

    ## Getter for list of legend positions
    def get_legendpositions(self):
        return self.__tikzlegendpos


    ## Debug function to view intermediate Tikzfile content
    def printtikz(self):
        print(self.__fulltikzstring)

    ## Helper function to add any Latex Code contained in section to the Tikzfile
    # @param section String which is added to the Tikzfile without checks
    def addsection(self, section):
        self.__fulltikzstring += '\n' + section

    ## Add the header with the current date\n
    # First add function to be called
    # @param filenames A List of source files to be added to the header
    # @param date Overwrites the current date by your date Sting
    # in the Format '2017-03-29' when passed
    def addheader(self, filenames='',
                  date=time.strftime('%Y-%m-%d', time.localtime())):
        self.__fulltikzstring += \
            self.__tikzheader.substitute({'date': date, 'filelist': filenames})

    ## Add color definition to be used for a graph
    # @param colorname Name of color to be used in one of the graphs
    # for example 'colorS11'
    # @param rgbval RGB values between 0 and 1 of color with name colorname
    # for example '0.00000,0.44700,0.74100'
    def addcolor(self, colorname, rgbval):
        self.__fulltikzstring += '\n' + self.__tikzcolor.substitute({
            'colorname': colorname, 'rgbval': rgbval})

    ## Add config definition to be used for the whole image
    # @param xmin Xaxis minimum value - String '0'
    # @param xmax Xaxis maximum value - String '1200'
    # @param ymin Yaxis minimum value - String '-90'
    # @param ymax Yaxis maximum value - String '0'
    # @param xparam Xaxis label symbol - String 'f' for Frequency
    # @param xunit Xaxis unit of [xparam] - String 'GHz' for Gigahertz
    # @param yparam Yaxis label symbol - String 'S_{mn}' for S-Parameters
    # @param yunit Yaxis unit of [yparam] - String 'dB' for Dezibel
    # @param legendpos The position of the legend anchor -
    # String default: '(0.03,0.97)'
    # @param legendanchor Anchor position of the legend -
    # String default: 'north west'
    # @param legendcolor Color of the legend - String default: 'white!15!black'
    # @param bgcolor Backgroundcolor of the plotting area -
    # String default: 'white'
    # @param addoptions Additional options for the Tikzpicture
    # for example 'thick' -
    # String default 'ylabel style={rotate=-90}'
    def addconf(self, xmin, xmax, ymin, ymax,
                xparam='f', xunit='GHz', yparam='S_{mn}', yunit='dB',
                legendpos='(0.03,0.97)', legendanchor='north west',
                legendcolor='white!15!black', bgcolor='white',
                addoptions='ylabel style={rotate=-90}'):
        self.__fulltikzstring += '\n' + self.__tikzconfig.substitute({
            'xmin': xmin, 'xmax': xmax, 'ymin': ymin, 'ymax': ymax,
            'xparam': xparam, 'xunit': xunit, 'yparam': yparam, 'yunit': yunit,
            'legendpos': legendpos, 'legendanchor': legendanchor,
            'legendcolor': legendcolor,
            'bgcolor': bgcolor, 'addoptions': addoptions
        })

    ## Add plot header with the properties to be used for this graph
    # @param colorname Name of color to be used in the graph -
    # has to be defined by addcolor earlier
    # @param linestyle Style of the graphline - String default '' solid\n
    # Examples: '', '-', '.', '-.', '..', '. .', '--', '- -',
    # '-.-', '- .', '-..', '-..-', '- . .'
    # @param addoptions Additional Options to be added to the plot axis -
    # String default ''\n
    # Examples: 'thick', 'ultra thick'
    def addplot(self, colorname, linestyle='', addoptions=''):
        self.__fulltikzstring += '\n' + self.__tikzplot.substitute({
            'plotcolor': colorname,
            'linestyle': self.__tikzgs[linestyle],
            'addopt': addoptions})

    ## Add data section to the Tikzplot
    # @param data Has to be an array with ClassData2D elements.
    def adddata(self, data):
        datastring = ''
        for date in data:
            datastring += '\n' + str(date.xvalue) + self.__tikzsep + \
                str(date.yvalue) + self.__tikzle

        self.__fulltikzstring += \
            self.__tikzdata.substitute({'data': datastring})

    ## Add plot legend to be used for a graph
    # @param index Index of the plots sparameter -
    # String default '11' for $S_{11}$
    # @param description Description in the legend -
    # String default ''
    # @param label Alternative Symbol if the plot doesn't show S-Parameters -
    # String or Template with $index\n
    # If label variable is passed and does not contain a Template
    # with $index in it, the @parname{index} variable will be ignored
    def addlegend(self, index='11', description='',
                  label=Template('$$S_{$index}$$')):
        if type(label) is Template:
            self.__fulltikzstring += '\n' + self.__tikzlegend.substitute({
                'desc': description,
                'label': label.substitute({'index': index})})
        elif type(label) is str:
            self.__fulltikzstring += '\n' + self.__tikzlegend.substitute({
                'desc': description, 'label': label})
        else:
            raise TypeError('You passed an unexpected type to the label variable. Must be eigther String or Template!')

    ## Add requirement type indicator
    # @param requirement ClassRequirements object
    # for which to add the type indicator\n
    # dependent on the
    # @parname{requirement}.reqtype and @parname{requirement}.reqscale
    # @param reqname Name of requirements color to be used,
    # must be unique in one plot,
    # ideally it's the same color the requirement line has already
    def add_req_type_ind(self, requirement, reqname):
        self.__fulltikzstring += '\n' + self.__tikzreq.substitute({
            'reqname1': reqname + '+' + str(requirement.get_reqdir()[0]),
            'reqname2': reqname + '+' + str(requirement.get_reqdir()[1]),
            'reqcolorname': reqname,
            'reqdata1': get_path_data_string(requirement + requirement.get_scale_offset()[0]),
            'reqdata2': get_path_data_string(requirement + requirement.get_scale_offset()[1])})

    ## Add the footer to the Tikzpicture
    # Last add function to be called
    def addfooter(self):
        self.__fulltikzstring += '\n' + self.__tikzfooter.template

    ## Export function to write Tikzfile
    # @param filename String - Exports Tikzfile to filename in local path,
    # or to specified location if full path is given
    def createTikzFile(self, filename='test.tikz'):
        if not os.path.isabs(filename):
            tikzfile = \
                open(os.path.join(os.path.dirname(__file__), filename), 'w')
        elif os.path.isabs(filename):
            if os.path.isdir(os.path.dirname(filename)):
                tikzfile = open(filename, 'w')
            else:
                raise IOError('Path not existent. Please create the Folders and run again!\nPath: ' + filename)
        else:
            raise ValueError('Variable filename contains no valid type, value or whatever!')
        tikzfile.write(self.__fulltikzstring)
        tikzfile.close()


## @cond Prevents doxygen from scanning the following
if __name__ == '__main__':
    # Basic ClassTikzExport usage example
    # Data Creation Example
    data1 = []
    date = ClassData2D(0, -25)
    data1.append(date)
    date = ClassData2D(8000, -20)
    data1.append(date)

    # Produce parallel sample data graphs
    data2 = [x + 1 for x in data1]
    data3 = [x + 2 for x in data1]
    data4 = [x + 3 for x in data1]
    data5 = [x + 4 for x in data1]
    data6 = [x + 5 for x in data1]
    data7 = [x + 6 for x in data1]
    data8 = [x + 7 for x in data1]
    data9 = [x + 8 for x in data1]

    # Define some Requirements
    requirement1 = ClassRequirements(r'Requirement 1', 'min', '', '1,0,0')
    requirement1.set_data(400, 6000, -10)
    requirement2 = ClassRequirements(r'Requirement 2', 'max', '', '0,0,1')
    requirement2.set_data(400, 6000, -5)
    requirement3 = ClassRequirements(r'Requirement 3', 'is', '', '0,1,0', 0.5)
    requirement3.set_data(400, 6000, -7.5)

    # Configure three colums in legend
    addopt = r'ylabel style={rotate=-90},legend columns=3,/tikz/column 2/.style={column sep=5pt},/tikz/column 4/.style={column sep=5pt}'
    graphopt = r'ultra thick'

    # Usage Example - Sequence is mandatory
    tikzplot = ClassTikzExport()

    colors = tikzplot.get_collist()
    linestyles = tikzplot.get_linestyles()

    # or tikzplot.addheader('TikzExport.py', '2017-05-21')
    tikzplot.addheader('TikzExport.py')
    # define a color for each graph to be added
    # use default colors
    tikzplot.addcolor('color1', colors[0])
    tikzplot.addcolor('color2', colors[1])
    tikzplot.addcolor('color3', colors[2])
    tikzplot.addcolor('color4', colors[3])
    tikzplot.addcolor('color5', colors[4])
    tikzplot.addcolor('color6', colors[5])
    tikzplot.addcolor('color7', colors[6])
    # Add colors for the requrements
    tikzplot.addcolor('requirement1', requirement1.graphcolor)
    tikzplot.addcolor('requirement2', requirement2.graphcolor)
    tikzplot.addcolor('requirement3', requirement3.graphcolor)

    # Add plot with default options
    # and additional options defined in addopt
    tikzplot.addconf('0', '8000', '-26', '6', xunit='MHz', addoptions=addopt)
    # Add plot with default options and additional option
    # to have also horizontal yaxis label
    # tikzplot.addconf('0', '1200', '-80', '0',
    #                  addoptions='ylabel style={rotate=-90}')
    tikzplot.addplot('color1', linestyles[0], graphopt)
    tikzplot.adddata(data1)
    tikzplot.addlegend('1', ' - Test 1')
    tikzplot.addplot('color2', linestyles[1], graphopt)
    tikzplot.adddata(data2)
    tikzplot.addlegend('2', ' - Test 2')
    tikzplot.addplot('color3', linestyles[2], graphopt)
    tikzplot.adddata(data3)
    tikzplot.addlegend('3', ' - Test 3')
    tikzplot.addplot('color4', linestyles[3], graphopt)
    tikzplot.adddata(data4)
    tikzplot.addlegend('4', ' - Test 4')
    tikzplot.addplot('color5', linestyles[4], graphopt)
    tikzplot.adddata(data5)
    tikzplot.addlegend('5', ' - Test 5')
    tikzplot.addplot('color6', linestyles[5], graphopt)
    tikzplot.adddata(data6)
    tikzplot.addlegend('6', ' - Test 6')
    tikzplot.addplot('color7', linestyles[6], graphopt)
    tikzplot.adddata(data7)
    tikzplot.addlegend('7', ' - Test 7')
    tikzplot.addplot('color1', linestyles[7], graphopt)
    tikzplot.adddata(data8)
    tikzplot.addlegend('8', ' - Test 8')
    tikzplot.addplot('color2', linestyles[8], graphopt)
    tikzplot.adddata(data9)
    tikzplot.addlegend('9', ' - Test 9')
    # Add requirements to the plot
    tikzplot.addplot('requirement1', requirement1.linestyle,
                     addoptions='ultra thick')
    tikzplot.adddata(requirement1.data)
    tikzplot.addlegend(label=requirement1.legendentry)
    tikzplot.addplot('requirement2', requirement1.linestyle,
                     addoptions='ultra thick')
    tikzplot.adddata(requirement2.data)
    tikzplot.addlegend(label=requirement2.legendentry)
    tikzplot.addplot('requirement3', requirement3.linestyle,
                     addoptions='ultra thick')
    tikzplot.adddata(requirement3.data)
    tikzplot.addlegend(label=requirement3.legendentry)
    # Add the reqirement type indicators to the plot
    tikzplot.add_req_type_ind(requirement1, 'requirement1')
    tikzplot.add_req_type_ind(requirement2, 'requirement2')
    tikzplot.add_req_type_ind(requirement3, 'requirement3')
    # Legendentry for ADC Measurements
    # tikzplot.addlegend('', 'AD9689 Evalboard', 'NSD')
    # Final thing to add to the Tikzpicture before export
    tikzplot.addfooter()
    # Show generated Tikzcode in console
    # tikzplot.printtikz()
    # Export generated Tikzcode to file test.tikz
    # in folder where this Classfile is located
    tikzplot.createTikzFile(
        os.path.join(
            os.path.dirname(__file__), '..', '..',
            'LatexTest', 'tikz', 'test.tikz'
        )
    )
## @endcond Prevents doxygen from scanning the code above
