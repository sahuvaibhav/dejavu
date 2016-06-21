import sys, getopt, time, os
import warnings
warnings.filterwarnings("ignore")
import json
from dejavu import Dejavu
from dejavu.recognize import FileRecognizer
import urllib2
import shutil
from multiprocessing import Process
import httplib
import subprocess

def main(argv):   
    global configFile, tempFile, tempCopy
    limit = None
    configFile = None 
    try:
        opts, args = getopt.getopt(argv,"hc:t:l:d:a:",["cfile=","ifolder=","limit=","url=","aac="])
        print opts
    except getopt.GetoptError:
        print 'realTimeCommDetect.py -c <configfile> -t <ifolder> -l <limit> -d <url> -a <aac>'
        sys.exit(2)
        
   
    for opt, arg in opts:
        if opt == "-h":
            print 'realTimeCommDetect.py -c <configfile> -t <ifolder> -l <limit> -d <url> -a <aac>'
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
            tempFile = "/tmp/"+liveURL.split("/")[-1]+".mp3"
            tempCopy = "/tmp/"+liveURL.split("/")[-1]+"_temp.mp3"
            if os.path.isfile(tempFile):
                os.remove(tempFile)
            if os.path.isfile(tempCopy):
                os.remove(tempCopy)
            if not configFile:
                print "Please provide config file"
                sys.exit()
            if not limit:
                print "Please provide time limit in seconds to records live stream"
                sys.exit()
            try:
                p1 = Process(target=recordProcess,args=(liveURL,limit))
                p1.start()
                p2 = Process(target=detectProcess)
                p2.start()
                p1.join()
                p2.join()
            except (KeyboardInterrupt, SystemExit):
                raise
                
        if opt in("-a","--aac"):
            aacURL = arg
            print aacURL
            tempFile = "/tmp/"+aacURL.split("/")[-1].split(".")[0]+".mp3"
            tempCopy = "/tmp/"+aacURL.split("/")[-1].split(".")[0]+"_temp.mp3"
            if os.path.isfile(tempFile):
                os.remove(tempFile)
            if os.path.isfile(tempCopy):
                os.remove(tempCopy)
            if not configFile:
                print "Please provide config file"
                sys.exit()
            if not limit:
                print "Please provide time limit in seconds to records live stream"
                sys.exit()
            
            print "connecting to " + aacURL
            m,s = divmod(int(limit),60)
            h,m = divmod(m, 60)
            time  = str(h) + ":" + str(m) + ":" + str(s)
            command = "ffmpeg -y -i "+ aacURL + " -t " + time + " " + tempFile
            try:
                p1 = Process(target=aacRecord, args = (command,))
                p1.start()
                p2 = Process(target=detectProcess)
                p2.start()
                p1.join()
                p2.join()
            except (KeyboardInterrupt, SystemExit):
                raise
                

def aacRecord(command):
    while True:
        s = time.time()
        subprocess.call(command, shell =True)
        print "time to record: " + str(time.time() - s)
        shutil.copy2(tempFile, tempCopy)
    

def recordProcess(liveURL,limit):
    print "Connecting to "+liveURL
    result =None
    while result is None:
        try:
            response = urllib2.urlopen(liveURL, timeout=float(limit))
            result = False
        except (IOError, httplib.HTTPException):
            print "Bad Connection! Don't Worry Connecting Again"
            continue
    #response = urllib2.urlopen(liveURL, timeout=float(limit))
    while True:
        recordLive(response,limit)
    
def detectProcess():
    with open(configFile) as f:
         config = json.load(f)	
    djv = Dejavu(config)
    recognizer = FileRecognizer(djv)
    while True:
        time.sleep(1)
        if os.path.isfile(tempCopy):
            print "Detecting \n"
            s = time.time()
            detect(recognizer)
            print "time to detect: " + str(time.time()-s)
            os.remove(tempCopy)
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
    
    f = open(tempFile, 'wb')
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
    shutil.copy2(tempFile,tempCopy)
    sys.stdout.flush()
    print ""
    print "Audio Stream recorded in "+tempFile


def detect(recognizer):
    filename = tempCopy
    song = recognizer.recognize_file(filename = filename)
 
    if song["confidence"] >=100:
        print "*************ad detected!****************\n"
        print "ad name: %s\n" % song["song_name"]
        print "confidence: %s\n" % song["confidence"]
        print "ad detected at time " + str(time.ctime())


if __name__ == "__main__":
	main(sys.argv[1:])
