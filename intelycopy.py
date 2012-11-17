import os, shutil, hashlib, datetime, pickle, sys, time, math

##Version 2

##RealServer Paths
##make sure paths end in /
#source = '/srv/samba/'
#destination = '/home/mark/SambaMount/squirtle-backup/'
#logfile = '/home/mark/intelydata.dat'

##windows debug paths...
source = 'D:\\Debug\\'
destination = 'D:\\Target\\'
logfile = 'D:\\data.dat'

#set at what percentages between each backup
percentbetweenbackups = 5#%

#are object for holding a entry of a file
class entry:
	path = ""
	md5 = ""
	size = 0

#generate a md5 hash for a file. taken from libxenons ecc generation code
def md5Checksum(filePath):
    fh = open(filePath, 'rb')
    m = hashlib.md5()
    while True:
        data = fh.read(8192)
        if not data:
            break
        m.update(data)
    return m.hexdigest()

#add a new entry to are list for use to refer back to later
def addEntry(filepath):
	#create a new tempory object
	tempentry = entry()
	#add are info
	tempentry.path = currentfile
	tempentry.size = os.path.getsize(source + currentfile)
	tempentry.md5 = md5Checksum(source +currentfile)
	#add it to the list
	list.append(tempentry)

#simple method for copying files
def copyfile(filepath):
	#if the file already exists in the destination then we remove it
	if os.path.isfile(destination+currentfile):
		print "Delete old file"
		#removing the file
		os.remove(destination + currentfile)
	
	#create are path to save to
	destpath = destination + currentfile
	#remove the filename from the path
	destpath = destpath.replace(os.path.basename(destpath),"")
	#if that path dosnt exist 
	if not os.path.exists(destpath):
		print "Making Directories"
		#we make them
		os.makedirs(destpath)
		
	print "Copying file : " + source + currentfile
	#finaly we copy the file to the destination
	shutil.copy2(source + currentfile, destination + currentfile)

#saving the log/list of files
def savelog():
	filewriter = open(logfile,'wb')
	pickle.dump(list, filewriter)
	filewriter.close()
	
def progress(width, percent):
	marks = math.floor(width * (percent / 100.0))
	spaces = math.floor(width - marks)
	loader = '[' + ('=' * int(marks)) + (' ' * int(spaces)) + ']'
	sys.stdout.write("%s %d%%\r" % (loader, percent))
	if percent >= 100:
		sys.stdout.write("\n")
	sys.stdout.flush()


#create are variables for later fuck python for not having types...
numberoffileprocessed = 0
numbertoprocess =0
lastsaveper = -1
newfiles = 0
updatedfiles = 0
nonupdatedfiles =0
starttime = datetime.datetime.now().replace(microsecond=0)

#print the start info with time and contact info
print "Version : 2.3"
print "\nIntely Copy Started : " + str(starttime)
print "\nReport any bugs to Tom Rosier Tom.Rosier92@gmail.com\n"

##starting the acctual program here
#we check if a log already exists
if not os.path.isfile(logfile) or os.path.getsize(logfile) == 0:
	#if not we create a new blank file ready to be written to
	f = open(logfile,'w')
	#then close are filewriter
	f.close()
	#create a new blank list
	list = []
else:
	#open are filereader
	filereader = open(logfile,'rb')
	#use pickle to dump log file back into are list
	print "\nLoading Log - Please Wait!"
	list = pickle.load(filereader)
	#close the file reader
	filereader.close()
	#debug really kinda shows theres entries from before
	print "Current Log Contains : " + str(len(list)) + " Entries"

#go through all directories
print "Discovering Files - Please Wait!"
for dirname, dirnames, filenames in os.walk(source):
	#for each file in the directory
    for filename in filenames:
		#countthem see how many files we have...
		numbertoprocess += +1

#print how many files we have just becuse its useful
print "We have to process : " + str(numbertoprocess) + " files!\n"

#start looking through dirs again
for dirname, dirnames, filenames in os.walk(source):
	#loop through the files in a directory
    for filename in filenames:
	#might need some error exception just incase we get a read error
	try:
		os.system('clear')
		#make the current path for the file we are working on
		currentfile = os.path.join(dirname, filename)
		#remove the source path so we can do some swapping
		currentfile = currentfile.replace(source, "")
		#now we check the file actualy still exists at source
		if os.path.isfile(source+currentfile):
			#have a boolean flag to check if we have done stuff
			flag = False
			#loop through are imported list
			for item in list:
				#if the item path = are current file
				if item.path == currentfile:
					#print some stuff becuse i never knew if we hit it
					print "We Found the file : " + filename +" in the database"
					#quick fail checks if size is the same
					if item.size == os.path.getsize(source + currentfile):
						#print this if its the same
						print "Size is the same need to check further"
						#if size is the same then we do a checksum on the file
						if item.md5 == md5Checksum(source +currentfile):
							#if the file is not the same we incroment the non updated files, stats are nice at the end of the day
							nonupdatedfiles += +1
							#print things
							print "File is the same no need to copy"
							#set are flaggy so it dosnt continue
							flag = True
							#else
						else:
							#we incroment the updated files
							updatedfiles += +1
							print "Removing old entry"
							#remove are old entry
							list.remove(item)
							#reset the flag back not really necercery but best to be sure
							flag = False
					else:
						#same as above
						updatedfiles += +1
						print "Removing old entry"
						list.remove(item)
						flag = False
					#well if we found the file we dont need to keep looping do we...
					break
			#if are flag hasnt been set then 
			if flag == False:
				#we add a new entry for the new current file
				addEntry(currentfile)
				#we check if the file exists in the destination just to save us copying
				if os.path.isfile(destination+currentfile):
					#if it exists tell the user
					print "File exists but is not in the database we will add it now : " + currentfile
					#do a checksum on the file to be sure if its changed or not
					if not md5Checksum(source + currentfile) == md5Checksum(destination + currentfile):
						##if the checksum isnt the same then we replace it by copying the new one
						#incroment updated again
						updatedfiles += +1
						print "Replacing file as it is different"
						copyfile(currentfile)
					else:
						#if we are not updating it we incroment the nonupdatedfiles
						nonupdatedfiles += +1
						print "File is the same anyway"
				else:
					#else we do stuff for new files, like incromenting are stats and copying
					newfiles += +1
					print "Copying a new File"
					copyfile(currentfile)
			#incroment are files we have delt with	
			numberoffileprocessed += +1
			#print the percentage and how many files we processed so we know how far we are through the backup
			percentage = int(100 * float(numberoffileprocessed)/float(numbertoprocess))
			print "\n" + str(percentage) + "%\t:\t" + str(numberoffileprocessed) + "/" + str(numbertoprocess) + " Files"
			progress(60,percentage)
			#check if we are a percentage that entitles us to backup
			if int(percentage) % percentbetweenbackups == 0:
				#check if we have already backed up on this current percentage
				if not int(percentage) == lastsaveper:
					#if we havent then we save the log
					print "\n<<<----Saving Log---->>>"
					#save are loglist thingy
					savelog()
					#set are last save point
					lastsaveper = int(percentage)
			#thats basicly end of execusion of the script
		else:
			#if we cant find are file then print a error
			print "File not found"
	#close the error exception
	except IOError, e:
		#print a error message so we can debug later
		print "Error happened Handling and continue {0} {1}".format(e.errno, e.strerror)
#print are stats to make everyone happy
print "\nNew Files Added : " + str(newfiles)
print "Updated Files   : " + str(updatedfiles)
print "Files Unchanged : " + str(nonupdatedfiles)
#give time that we finished
print "\nIntely Copy Finished : " + str(datetime.datetime.now().replace(microsecond=0))  
print "\nTime Taken : " + str((datetime.datetime.now().replace(microsecond=0)-starttime))