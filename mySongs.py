import time
from dejavu import Dejavu
from dejavu.recognize import FileRecognizer
config = {
     "database": {
         "host": "127.0.0.1",
         "user": "root",
         "passwd": "vahbiav", 
         "db": "comm_new",
		 
     }
 }
djv = Dejavu(config)

#djv.fingerprint_directory("/home/vaibhav/audio/commercials - mp3", [".mp3"], 4)
#print djv.db.get_num_fingerprints()

#song = djv.recognize(FileRecognizer, "/media/sf_C_DRIVE/Users/vsahu/Desktop/audio/train/3.mp3",limit=10)
#print "From file we recognized: %s\n" % song


recognizer = FileRecognizer(djv)
filename = "/home/vaibhav/audio/radio break - mp3/tafe.mp3"
#song = recognizer.recognize_file(filename = filename ,start = 30,limit=40)
#limit=5
for start in range(0,670,30):
#start =0
    s = time.time()
    song = recognizer.recognize_file(filename = filename ,start = start,limit=start+30)
#    #song = recognizer.recognize_file(filename = filename)
#    if song["confidence"] >=1000:
    if song["confidence"] > 100:
        print "song name: %s\n" % song["song_name"]
        print "confidence: %s\n" % song["confidence"]
    t = time.time() - s
    print t
        
