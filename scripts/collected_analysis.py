#import packages
import os
import io 
from contextlib import redirect_stdout 
text_trap = io.StringIO()
																				#Collect all .gff files
os.mkdir("collected_analysis")
os.system("cp collected_phages/**/*.gff collected_analysis")
os.chdir("collected_analysis")

#define initial values
previous_threshold = 100
threshold = 95


while previous_threshold != threshold:
	command = "roary -cd 95 -i " + str(threshold) + " -p 4 -e --mafft *.gff > /dev/null 2>&1"		#Perform core alignments with 95% gene precense but a decreasing % identity threshold
	os.system(command)
	with open("summary_statistics.txt", 'r') as summary:
		cores = int(summary.readline().split()[-1])
		print("Amount of core genes: " + str(cores))
		print("at % identity threshold: " + str(threshold))
		if cores <= 2:														#if amount of core genes <= 2, lower %-identity threshold
			threshold -= 5
			previous_threshold -= 5
			if threshold == 55:												#if %-identity reaches 60%, make an error file to explain why the final output is might not be trusted
				previous_threshold = 55
				with open("Errors.txt",'a') as errors:
					errors.write("ERROR! For the collection of found prophages, no more than two genes were \n present in 95% of the prophages with 60% identity. \n A core gene alignment is thus not feasible or at least not fully trustworthy.")
		else:
			print("To perform a core alignment, the definition of core was set at " + str(threshold) + "percent identity between the genes")
			threshold = "stop"
			previous_threshold = "stop"

#Make and display a phylogenetic tree based on the core gene alignment, marked by a color scheme and ordnament map
os.system("fasttree -quiet -nt core_gene_alignment.aln > my_tree_collected_analysis.nw"),				
os.system("nw_reroot my_tree_collected_analysis.nw > my_tree_collected_analysis_rerooted.nw")	#reroot according to longest branch
os.system("mv my_tree_collected_analysis_rerooted.nw ../newick_trees")

#Make ending indicator
os.chdir(".."),
os.system("touch collected_analysis_done")
