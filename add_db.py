#import necessary packages
import os
import sys

#Get paths
curdir = str(os.getcwd())
arguments = sys.argv[1:]
num_arg = 0
for argument in range(0,len(arguments)):
	
	#Help menu
	if arguments[argument].startswith("-H") or arguments[argument].startswith("--help"):
		print("This helper-script will let you make a custom database\n")
		print("[-H --help\tShow this help menu]\n")
		print("[-F --fasta\tThe path to the folder with your fasta or fasta.gz files]\n")
		print("[-DB --database\tThe path to the Afili db folder]\n")
		print("[-N --name\tThe name of your custom database]\n")
		sys.exit(1)
		
	#Fasta files
	if arguments[argument].startswith("-F") or arguments[argument].startswith("--fasta"):
		fasta_folder = curdir +"/"+arguments[argument+1]
		num_arg += 1
	#Database folder
	if arguments[argument].startswith("-DB") or arguments[argument].startswith("--database"):
		db = curdir +"/"+arguments[argument+1]
		num_arg += 1
	#Name
	if arguments[argument].startswith("-N") or arguments[argument].startswith("--name"):
		genus = arguments[argument+1].lower()
		num_arg += 1

#Check arguments
if len(arguments) > 6:
	print("Too many arguments for add_db.py")
	sys.exit(1)
elif num_arg < 3:
	print("Too few arguments for add_db.py")
	sys.exit(1)


#Get the extension
gz_ext = False
for extension in os.listdir(fasta_folder):
	if extension.endswith("gz"):
		gz_ext = True
	else:
		extent = extension.split(sep=".")[-1]
		

#Collecting both individual fastas and all fastas in one filegz_ext = True
if gz_ext == True:
	try:
		os.system("cat " + fasta_folder + "/*.fna.gz >> " + str(genus) + "_DNA_cds.fna.gz")
		os.system("gunzip " + fasta_folder + "/*.gz")
	except Exception as error:
		print(error)
else:
	try:
		os.system("cat " + fasta_folder + "/*." + extent + " >> " + fasta_folder + "/" + str(genus) + "_DNA_cds.fna")
	except Exception as error:
		print(error)

#Prepare the database files
os.chdir(fasta_folder)
print("making database files")
for fasta in os.listdir():
	if fasta.endswith("fna"):
		command = "makeblastdb -in " + fasta + " -dbtype nucl -parse_seqids -out " + db + "/"+str(genus)+"/"+ fasta+"_DNA_DB 2> /dev/null"
		os.system(command)
		with open(db+"/"+str(genus)+"/database_names.txt",'a') as names:		#Make list with all individual database names
			if fasta != str(genus) + "_DNA_cds.fna":
				names.write(fasta + "_DNA_DB\n")

print("Your custom database have been added")
