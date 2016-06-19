from dejavu import Dejavu
from dejavu.recognize import FileRecognizer
config = {
     "database": {
         "host": "127.0.0.1",
         "user": "root",
         "passwd": "vahbiav", 
         "db": "commercialsdb",
		 
     },
	"fingerprint_limit": "1"
 }
djv = Dejavu(config)

#djv.fingerprint_directory("/media/sf_C_DRIVE/Users/vsahu/Desktop/audio/train", [".mp3"], 3)
#print djv.db.get_num_fingerprints()

#song = djv.recognize(FileRecognizer, "/media/sf_C_DRIVE/Users/vsahu/Desktop/audio/train/3.mp3",limit=10)
#print "From file we recognized: %s\n" % song


recognizer = FileRecognizer(djv)
filename = "/home/vaibhav/dejavu/Sample045788.wav"
#limit=5

song = recognizer.recognize_file(filename = filename ,start = 1,limit=5)
#song = recognizer.recognize_file(filename = filename)
#    if song["confidence"] >=1000:
print "song name: %s\n" % song["song_name"]
print "confidence: %s\n" % song["confidence"]
        