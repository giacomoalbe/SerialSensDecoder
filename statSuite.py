#! *_* coding: UTF-8 *_*

import sys
from matplotlib import pyplot as plt

"""

Import all the data from the logs 
and process them in order to 
get the result I need

"""

# Set the folder in whitch to store the results
resFolder = "res/"
suffix = ""

def main():

    """
    Function for switching between different
    operations this script can do
    """

    args = sys.argv[1:]

    if len(args) >= 2: 
        # Set the suffix
        suffix = '_' + args[1] 

    print "Suffix is %s" % (suffix,)

    if len(args) > 0:

        if int(args[0][0]) == 2:

            timeSpaceAvg(suffix)
         
        else:
            spatialAvg(suffix)



# 0. GP Functions

def avg(items):

    if type(items[0]) != type(2):
        items = [int(item) for item in items]

    return sum(items) / float(len(items))

def scartoTipo(items, mean = None):

    if not mean:
        mean = avg(items)

    return (sum([(item - mean)**2 for item in items]) / float(len(items)))**0.5

def printPhotoScarto(hist):

    """
    Print a matrix repr of the scarto
    """

    grid = ""

    for index in hist:

        ext = "\t"

        if (index+1) % 6 == 0: 
            # A capo!
            ext = "\n"

        var = scartoTipo(hist[index]) / avg(hist[index]) 

        grid += "{0:.2f}{1}".format(var, ext)

    print grid

def outputString(hist):

    """
    Creates the string to be written to a file
    """

    outputStr = "Index\tAverage\tScarto\n"

    for index in hist:

        outputStr += "{0}\t{1:.4f}\t{2:.4f}\n".format(index, avg(hist[index]), scartoTipo(hist[index]))

    return outputStr


# 1. Average of Spacial Average of all Logs

def spatialAvg(suffix, filename):

    try:

        logsFile = open('logs/%s%s.dat' % (filename, suffix))

        # Read the file's row (every is a photo)
        logs = logsFile.read().split("\n")[:-1]
        logsFile.close()

        mainAvgs = [avg(a.split(",")) for a in logs]

        mainAvg = sum(mainAvgs) / float(len(mainAvgs))

        return mainAvg

    except:
        
        pass
        return None

# 2. Time Average

# Use only 22

def timeAvg(suffix, filename):

    # Set the suffix for decoding the correct 
    # series of logs
    try: 

        readFile = open('logs/%s%s.dat' % (filename, suffix), 'r')
        images = readFile.read().split("\n")[:-1]

        pixelHist = {}

        for image in images:
            for index, pixel in enumerate(image.split(",")):

                pixel = int(pixel)

                if pixelHist.get(index):
                    pixelHist.get(index).append(pixel) 
                else:
                    pixelHist[index] = [pixel]


        #printPhotoScarto(pixelHist)
        #fileOut = open(resFolder + 'time_res_%d%d%s.tsv' % (a,b,suffix), 'w')
        #fileOut.write(outputString(pixelHist))
        #fileOut.close()
        #print "File: %d%d%s written!" % (a,b,suffix)

    except:
        pass

    return pixelHist

def timeSpaceAvg(suffix):

    namespaces = ["%d%d" % (a,b) for a in range(1,6) for b in range(1,7)]
    outString = ""
    y = []

    for filename in namespaces:

        pixelHist = timeAvg(suffix, filename)
        spatial = spatialAvg(suffix, filename)

        pixelAvg = [avg(pixelHist[key]) for key in pixelHist]

        scarto = scartoTipo(pixelAvg, spatial)
        y.append(scarto)

        outString += "{0},{1:.03f}\n".format(filename, scarto)

        print "Processing {0}...".format(filename)

    fileOutName = "{0}spatial{1}.csv".format(resFolder, suffix)
    fileOut = open(fileOutName, 'w')
    fileOut.write(outString)
    fileOut.close()

    print "Written file: {0}".format(fileOutName)
    plt.plot([int(name) for name in namespaces],y)
    plt.show()

if __name__ == '__main__':

    main()
    

