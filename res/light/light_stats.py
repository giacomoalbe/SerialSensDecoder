#! *_* coding: utf-8 *_*

avgs = []
prefolder = '02'

namespaces = ["%s%s" % (a,b) for a in range(1,6) for b in range(1,7)]

for name in namespaces:

    vals = []

    try:
        fopen = open('%s/smub1buffer0%s.csv' % (prefolder, name))
        lines = fopen.read().split('\n')[6:-1]
        fopen.close()

        print "Adding lines for %s-%s" % (prefolder, name)
        for line in lines:

            if len(line.split(';')) == 1:
                # File is comma formatted
                value = line.split(',')[1]
            else:
                value = line.split(';')[1].replace(',','.')
                
            vals.append(float(value))

        print "Processing avg for %s-%s" % (prefolder, name)
        avgs.append(sum(vals) / len(vals))
    except:
        pass

outString = ''
fwrite = open('%s/out.csv' % (prefolder,) , 'w')
filecontent = ""

for index, avg in enumerate(avgs):

    filecontent += str(avg).replace('.', ',') + '\n'

fwrite.write(filecontent)
fwrite.close()
print "Scritto file %s-out.csv" % prefolder
"""
    print str(avg).replace('.',',')

    outString += "%s\t%s\n" % (namespaces[index], avg)

print outString
"""

