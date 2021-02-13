#import packages and change directory
import os
os.chdir("collected_phages")


file_count = 0
for phage_file in os.listdir():				#Perform a gene prediction on all the colelcted phages
	if phage_file.endswith(".fna"):
		file_count += 1
		command = "prokka --kingdom Viruses --quiet --prefix {} --outdir prokka_{} {}".format(phage_file[:-4], str(file_count), phage_file)
		print("Performing a gene prediction on all matches found.")
		os.system(command)
		
#Make ending indicator
os.chdir("..")
os.mknod("Prokka_collected_done")
