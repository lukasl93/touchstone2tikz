#!/usr/bin/python2
# -*- coding: utf-8 -*-

## @package ClassDataStructs
# Provide all data structures in classes for 2D plot data and Requirements.
#
# @date Created on 28.03.2017\n
#      Last edited 27.08.2017 by lukasl93
#
# @author lukasl93


## Dataformat Class for 2D Data Tuple - currently unused
class ClassGraphData(object):
    ## Constructor
    def __init__(self):
        self.xquant = 'f'
        self.yquant = "S_{mn}"
        self.xunit = 'GHz'
        self.yunit = 'dB'
        self.data = []


    ## Add data in the ClassData2D format
    # @param data Format is data.xvalue,data.yvalue
    # subkeys must be float or int types
    def addData2D(self, data):
        if type(data[0]) is [ClassData2D]:
            self.data.append(data)
        else:
            raise TypeError('Variable data must be a list of type ClassData2D!')

    ## Add list of data in the ClassData2D format
    # @param xdata Must be float or int type
    # @param ydata Must be float or int type
    def addDataList(self, xdata, ydata):
        if len(xdata) == len(ydata):
            data = []
            for i in range(0, len(xdata), 1):
                data.append(ClassData2D(xdata[i], xdata[i]))
            self.data.append(data)


## Dataformat Class for 2D Data Tuple
class ClassData2D(object):
    ## Constructor
    def __init__(self, xval, yval):
        self.xvalue = xval
        self.yvalue = yval

    ## Definition of addition of ClassData2D and Number
    # to add the number to the y value.
    # @param other Numerical value to be added to the data y value
    # @return Return a copy of the ClassData2D object
    # with @parname{other} added to the y value
    def __add__(self, other):
        result = ClassData2D(self.xvalue, self.yvalue)
        result.yvalue += other
        return result

    ## Print data stored in ClassData2D Object as tuple,
    # when print(ClassData2Dobject) is called.
    def __str__(self):
        return str((self.xvalue, self.yvalue))

    ## If a list of ClassData2D objects should be printed
    # call __str()__ for each element in the list
    def __repr__(self):
        return self.__str__()


## Dataformat Class for Requirements
class ClassRequirements(object):
    ## Possible Types of requirement
    __reqtypes = {
        '': (0, 0),
        'max': (0, 1),
        'min': (0, -1),
        'is': (-1, 1)}

    ## Constructor
    # @param legend Legendstring - String default: 'Requirements'
    # @param reqtype Type of the Reqirement one of ('','max','min','is')
    # @param style Stylestring - String default '- . .'
    # All possibilities see TikzExport::ClassTikzExport::__tikzgs
    # @param color Colorstring with RGB value -
    # String default '0.63500,0.07800,0.18400'
    # @param reqscale Scaling factor in y direction
    # for the requirements type indicator
    # @param data List of ClassData2D points defining the requirement
    def __init__(self, legend='Requirements', reqtype='', style='- . .',
                 color='0.63500,0.07800,0.18400', reqscale=1, data=[]):
        # Graph parameters
        self.legendentry = legend
        self.graphcolor = color
        self.linestyle = style
        self.reqscale = reqscale
        if reqtype in self.__reqtypes:
            self.reqtype = reqtype
        else:
            self.reqtype = ''
            print('Unnown Type of Requirement given! Must be one of max,min,is or empty')
        # Graphdata array
        if not data:    # if list is empty
                self.data = []
        else:
            if type(data[0]) is ClassData2D:
                self.data = data
            else:
                raise TypeError('Variable data must be of type list(ClassData2D)!')

    ## Definition of addition of ClassRequirements and Number
    # to add the number to all yvalues of the data array.
    # @ param other Numerical value to add to y data values
    # @return Warning: Does not return an object copy,
    # but a copy of the objects data list plus @parname{other}
    def __add__(self, other):
        return [x + other for x in self.data]

    ## Print all properties of ClassRequirements Object,
    # when print(ClassRequirements) is called.
    def __str__(self):
        return '''ClassRequirements:
    Legendentry: \'%s\',
    Graphcolor: \'%s\',
    Linestyle: \'%s\',
    Scale: \'%i\',
    Type: \'%s\',
    Curvedata: %s''' % (self.legendentry, self.graphcolor,
                        self.linestyle, self.reqscale, self.reqtype,
                        str(list((x.xvalue, x.yvalue) for x in self.data)))

    ## If a list of ClassRequirements objects should be printed
    # call __str()__ for each element in the list
    def __repr__(self):
        return self.__str__()

    ## Length of requirement is one
    # Just a trick to be able to use len() on the requirements list and
    # the requirement directly
    def __len__(self):
        return 1

    ## Add one ClassData2D point to the data list
    # @param point ClassData2D object
    def add_datapoint(self, point):
        if type(point) is ClassData2D:
            self.data.append(point)
        else:
            raise TypeError('Variable point must be of type ClassData2D!')

    ## Function to create complex Requirementcurves
    # @param datatuples Tuplelist in format [(xval1,yval1),(xval2,yval2),...]
    # with type number xval und yval
    def set_comp_data(self, datatuples):
        for date in datatuples:
            self.add_datapoint(ClassData2D(date[0], date[1]))

    ## Mostly just a linear requirement graph is needed with two endpoints.\n
    # This is a convenience function to configure a linear requirement.
    # @param lowerx Often the lower Frequency value - Type number
    # @param upperx Often the upper Frequency value - Type number
    # @param lowery The Requirement for y at the lower Frequency value -
    # Type number
    # @param uppery The Requirement for y at the upper Frequency value -
    # Type number\n
    # You don't have to pass @parname{uppery} if its the same as @parname{lowery}
    def set_data(self, lowerx, upperx, lowery, uppery=None):
        self.data = []
        # you don't have to pass uppery if its the same as lowery
        if uppery is None:
            uppery = lowery
        self.data.append(ClassData2D(lowerx, lowery))
        self.data.append(ClassData2D(upperx, uppery))

    ## Return the offset direction tuple of the requirement type indicator
    # @return Offset direction tuple for this requirementtypes
    def get_reqdir(self):
        return self.__reqtypes[self.reqtype]

    ## Return the offset for the type indicators of the requirement type indicator
    # @return Tuple of scaled offset direction
    def get_scale_offset(self):
        return tuple(self.reqscale * x for x in self.__reqtypes[self.reqtype])


## @cond Prevents doxygen from scanning the following
if __name__ == '__main__':
    # Testcode for requirement class
    requirement11 = \
        ClassRequirements(r'Anforderungen Anpassung ($S_{11}$)', 'is', '')
    requirement11.set_data(0.4, 6, -20)
    print(requirement11)

    print(requirement11 + requirement11.get_scale_offset()[0])
    # result = requirement11.data[:]
    pass
## @endcond Prevents doxygen from scanning the code above
