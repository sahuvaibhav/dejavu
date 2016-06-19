import time, sys
import urllib2
url = "http://streaming.novaentertainment.com.au/nova969"
print "Connecting to "+url
response = urllib2.urlopen(url, timeout=10.0)
fname = "Sample"+str(time.clock())[2:]+".mp3"
f = open(fname, 'wb')
block_size = 1024
print "Recording roughly 10 seconds of audio Now - Please wait"
limit = 10
start = time.time()
while time.time() - start < limit:
    try:
        audio = response.read(block_size)
        if not audio:
            break
        f.write(audio)
        sys.stdout.write('.')
        sys.stdout.flush()
    except Exception as e:
        print ("Error "+str(e))
f.close()
sys.stdout.flush()
print ""
print "10 seconds from "+url+" have been recorded in "+fname

