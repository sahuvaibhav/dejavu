import sys, getopt, time, os
import warnings
warnings.filterwarnings("ignore")
import json
from dejavu import Dejavu
from dejavu.recognize import FileRecognizer
import urllib2
import shutil
from multiprocessing import Process

def main(argv):   
    global configFile
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
            try:
               
	# create a Dejavu instance
                
                while True:
                    p1 = Process(target=recordProcess,args=(liveURL,limit))
                    p1.start()
                    p2 = Process(target=detectProcess)
                    p2.start()
                    p1.join()
                    p2.join()
            except (KeyboardInterrupt, SystemExit):
                raise

def recordProcess(liveURL,limit):
    print "Connecting to "+liveURL
    response = urllib2.urlopen(liveURL, timeout=float(limit))
    while True:
        recordLive(response,limit)
    
def detectProcess():
    with open(configFile) as f:
         config = json.load(f)	
    djv = Dejavu(config)
    recognizer = FileRecognizer(djv)
    while True:
        time.sleep(1)
        if os.path.isfile("/tmp/temptemp.mp3"):
            print "Detecting \n"
            s = time.time()
            detect(recognizer)
            print "time to detect: " + str(time.time()-s)
            os.remove("/tmp/temptemp.mp3")
            print "file removed"
        else:
            #print "File not ready \n"
            pass

def train(configFile,trainFolder):
	with open(configFile) as f:
	    config = json.load(f)	
     
	djv = Dejavu(config)
	djv.fingerprint_directory(trainFolder, [".mp3"])

def recordLive(response,limit):
    fname = "/tmp/temp.mp3"
    f = open(fname, 'wb')
    block_size = 1024
    print "Recording audio Now - Please wait"
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
    shutil.copy2("/tmp/temp.mp3","/tmp/temptemp.mp3")
    sys.stdout.flush()
    print ""
    print "Audio Stream recorded in "+fname


def detect(recognizer):
    filename = "/tmp/temptemp.mp3"
    song = recognizer.recognize_file(filename = filename)
 
	#if song["confidence"] >=100:
    print "*************ad detected!****************\n"
    print "ad name: %s\n" % song["song_name"]
    print "confidence: %s\n" % song["confidence"]


if __name__ == "__main__":
	main(sys.argv[1:])
