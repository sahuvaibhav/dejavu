import sys, getopt, time
import warnings
warnings.filterwarnings("ignore")
import json
from dejavu import Dejavu
from dejavu.recognize import FileRecognizer, MicrophoneRecognizer
import urllib2

def main(argv):
    
    limit = None
    configFile = None 
    try:
        opts, args = getopt.getopt(argv,"hc:t:l:d:",["cfile=","ifolder=","limit=","url="])
        print opts
    except getopt.GetoptError:
        print 'realTimeCommDetect.py -c <configfile> -t <ifolder> -l <limit> -d <url>'
        sys.exit(2)
        
        
    for opt, arg in opts:
        if opt == "-h":
            print 'realTimeCommDetect.py -c <configfile> -t <ifolder> -l <limit> -d <url> '
            sys.exit()
        if opt in ("-c" ,"--cfile"):
            configFile = arg
        if opt in ("-l" ,"--limit"):
            limit = arg
        if opt in ("-t" ,"--ifolder"):
            trainFolder	 = arg
            if not configFile:
                print "Please provide config file"
                sys.exit()
            train(configFile,trainFolder)
        if opt in ("-d", "--url"):
            liveURL = arg
            print liveURL
            if not configFile:
                print "Please provide config file"
                sys.exit()
            if not limit:
                print "Please provide time limit in seconds to records live stream"
                sys.exit()
            recordLive(liveURL,limit)
            #detect(configFile)

def train(configFile,trainFolder):
	with open(configFile) as f:
	    config = json.load(f)	

	# create a Dejavu instance
	djv = Dejavu(config)

	# Fingerprint all the mp3's in the directory we give it
	djv.fingerprint_directory(trainFolder, [".mp3"])

def recordLive(liveURL,limit):
	url = liveURL
	print "Connecting to "+url
	response = urllib2.urlopen(url, timeout=float(limit))
	fname = "/tmp/temp.mp3"
	f = open(fname, 'wb')
	block_size = 1024
	print "Recording roughly 10 seconds of audio Now - Please wait"
	#limit = 10
	start = time.time()
        print int(limit)
	while time.time() - start < int(limit):
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


def detect(configFile):
	with open(configFile) as f:
	    config = json.load(f)	
	# create a Dejavu instance
	djv = Dejavu(config)
	recognizer = FileRecognizer(djv)
	filename = "/tmp/temp.mp3"
	#limit=5
	song = recognizer.recognize_file(filename = filename)
	#    if song["confidence"] >=1000:
	print "song name: %s\n" % song["song_name"]
	print "confidence: %s\n" % song["confidence"]


if __name__ == "__main__":
	main(sys.argv[1:])
