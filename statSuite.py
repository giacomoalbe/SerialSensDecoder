#! *_* coding: UTF-8 *_*

import sys

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
            timeAvg(suffix)
        else:
            spatialAvg(suffix)



# 0. GP Functions

def avg(items):

    if type(items[0]) != type(2):
        items = [int(item) for item in items]

    return sum(items) / float(len(items))

def scartoTipo(items):

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

def spatialAvg(suffix):

    outString = ""

    for firstNumb in range(1,6):
        for secondNumb in range(1,7):

            try:

                logsFile = open('logs/%d%d%s.dat' % (firstNumb, secondNumb, suffix))

                # Read the file's row (every is a photo)
                logs = logsFile.read().split("\n")[:-1]
                logsFile.close()

                mainAvgs = [avg(a.split(",")) for a in logs]

                mainAvg = sum(mainAvgs) / float(len(mainAvgs))

                outString += "%d\n" %  (mainAvg)

                print "Processing file: %d%d%s" % (firstNumb, secondNumb, suffix)
            except: 
                pass

    writeFile = open(resFolder + 'avgs%s.csv' % (suffix,), 'w')
    print "Written file %savgs%s.csv" % (resFolder, suffix)
    writeFile.write(outString)
    writeFile.close()

# 2. Time Average

# Use only 22

def timeAvg(suffix):

    # Set the suffix for decoding the correct 
    # series of logs

    for a in range(2,6):
        for b in range(1,7):

            try: 

                readFile = open('logs/%d%d%s.dat' % (a,b, suffix), 'r')
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
                fileOut = open(resFolder + 'time_res_%d%d%s.tsv' % (a,b,suffix), 'w')
                fileOut.write(outputString(pixelHist))
                fileOut.close()
                print "File: %d%d%s written!" % (a,b,suffix)

            except:
                pass

if __name__ == '__main__':

    main()
    

