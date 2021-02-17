
#To know when a run is done and to ensure that there are no wildcards in the target rule
rule all:
    input:
    	"{}/all_done".format(scripts)
 
#Move all fasta files into scripts directory
rule start:
	input:
	output:
		"{}/start_done".format(scripts)
	run:
		os.system("mv {}/../*.fna {}/".format(scripts,scripts))
		os.system("touch {}/start_done".format(scripts))
		
#Uses script1 to perform a gene prediction on the ppBGCs
rule PROKKA_original_ppBGCs:
	input: 
		"{}/start_done".format(scripts)
	output:
		"{}/prokka_prophage_done".format(scripts)
	run:
		os.chdir("{}/".format(scripts)),
		os.system("python {}/prokka_prophage.py >> output.log".format(scripts)),
		os.system("mkdir {}/blast_folder".format(scripts)),
		os.system("mv {}/**/*.ffn blast_folder".format(scripts)),
		os.system("touch {}/prokka_prophage_done".format(scripts))



#Perform a BLAST search for each gene in each .ffn file against the downloaded database using script2
#settings: %-identity = 25, %-query coverage = 30
rule BLAST_ppBGCs_against_database:
	input: 
		"{}/prokka_prophage_done".format(scripts)
	output:
		"{}/blast_done".format(scripts)
	run:
		os.chdir("{}/".format(scripts)),
		os.system("python {}/blast.py >> output.log".format(scripts))
	

#Parsing the results from the BLAST search with script3
rule Filter_results_from_BLAST:
	input:
		"{}/blast_done".format(scripts)
	output:
		"{}/filtering_done".format(scripts)
	run:
		os.chdir("{}/".format(scripts)),
		os.system("python {}/filter.py ".format(scripts))


#Collecting fasta files for bacterial prophage hosts with script4
rule collecting_host_fastas:
	input:
		"{}/filtering_done".format(scripts)
	output:
		"{}/collection_host_done".format(scripts)
	run: 
		os.chdir("{}/".format(scripts)),
		os.system("python {}/collection_host.py >> output.log".format(scripts))

#Making a list of phages at unique positions in all hosts using script6
rule list_of_phages_w_unique_host_or_position:
	input:
		"{}/collection_host_done".format(scripts)
	output:
		"{}/unique_lines_done".format(scripts)
	run:
		os.chdir("{}/".format(scripts)),
		os.system("python {}/unique_phage.py >> output.log".format(scripts))

#Actually collecting phage fastas with script7
rule collect_phage_fastas_from_phage_list:
	input:
		"{}/unique_lines_done".format(scripts)
	output:
		"{}/collected_phages_done".format(scripts)
	run:
		os.chdir("{}/".format(scripts)),
		os.system("python {}/unique_phage_fasta.py >> output.log ".format(scripts))


#Performing an add_on analysis on the collected phages
rule add_ons:
	input:
		"{}/collected_phages_done".format(scripts)
	output:
		"{}/add_on_done".format(scripts)
	run:
		os.chdir("{}/".format(scripts)),
		os.mkdir("{}/ANI".format(scripts))
		os.system("cp {}/collected_phages/*.fna ANI".format(scripts)),
		if add_on == True:
			pass
		else:
			pass
		os.system("touch {}/add_on_done".format(scripts))


#Gene predict the collected phages with script8
rule Prokka_all_phages_from_list:
	input:
		"{}/collected_phages_done".format(scripts)
	output:
		"{}/Prokka_collected_done".format(scripts)
	run:
		os.chdir("{}/".format(scripts)),
		os.system("python {}/prokka_putative_phage.py >> output.log".format(scripts))

#Copy the gff files from the gene prediction of the collected phages and perform a roary 
# core gene alignment with decreasing %-identity threshold with script14
#And display the phylogenetic trees
rule roary_fasttree_on_all_phages:
	input:
		"{}/Prokka_collected_done".format(scripts),
		"{}/phylogeny_display_done".format(scripts)
	output:
		"{}/collected_analysis_done".format(scripts)
	run:
		os.chdir("{}/".format(scripts)),
		os.system("python {}/collected_analysis.py >> output.log".format(scripts))
	
#Perform an MLST analysis on the hosts
rule MLST_check_hosts:
	input:
		"{}/collection_host_done".format(scripts)
	output:
		"{}/mlst_done".format(scripts)
	run:
		os.chdir("{}/".format(scripts)),
		os.system("mlst {}/host_fastas/*.fna --quiet > {}/host_mlst.txt".format(scripts,scripts)),
		os.system("touch {}/mlst_done".format(scripts))

#Make metadata for the phylogenetic trees
rule display_phylogeny:
	input:
		"{}/mlst_done".format(scripts),
		"{}/collected_phages_done".format(scripts),
		"{}/add_on_done".format(scripts)
	output:
		"{}/phylogeny_display_done".format(scripts)
	run:
		os.chdir("{}/".format(scripts)),
		os.system("python {}/phylogeny_display.py >> output.log".format(scripts))
	
#Perform an average nucleotide identity analysis with FastANI
rule ANI:
	input:
		"{}/phylogeny_display_done".format(scripts),
		"{}/add_on_done".format(scripts)
	output:
		"{}/ANI_done".format(scripts)
	run:
		os.chdir("{}/".format(scripts)),
		os.system("python {}/ANI.py".format(scripts)),
		os.system("python {}/ANI_formatting.py".format(scripts)),
		os.system("touch {}/ANI_done".format(scripts))


#Making heatmaps with R
rule Heatmaps:
	input:
		"{}/ANI_done".format(scripts)
	output:
		"{}/heatmaps_done".format(scripts)
	run:
		os.chdir("{}/".format(scripts)),
		os.system("{}/RHeatmaps.sh >> output.log".format(scripts)),

#Collect all results in a result folder
#GET R HEAT MAPS
rule collect_all_results:
	input:
		"{}/heatmaps_done".format(scripts),
		"{}/phylogeny_display_done".format(scripts),
		"{}/collected_analysis_done".format(scripts)
	output:
		"{}/all_done".format(scripts)
	run:
		os.chdir("{}/".format(scripts)),
		os.mkdir("{}/RESULTS".format(scripts))
		if add_on == True:
			pass
		os.system("mv {}/newick_trees/originalsMetadata.txt {}/RESULTS".format(scripts,scripts))
		os.system("mv {}/newick_trees/SpeciesMetadata.txt {}/RESULTS".format(scripts,scripts))
		os.system("mv {}/newick_trees/my_tree_collected_analysis_rerooted.nw {}/RESULTS".format(scripts,scripts))
		os.system("mv {}/collected_phages/collected_analysis/Errors.txt {}/RESULTS > /dev/null 2>&1".format(scripts,scripts))
		if "ANI.pdf" in os.listdir(scripts):
			os.system("mv {}/ANI.pdf {}/RESULTS".format(scripts,scripts))
			os.system("mv {}/ANI_matrix.txt {}/RESULTS".format(scripts,scripts))
		else:
			print("##############################################################")
			print("ERROR MESSAGE: No ANI heat map was produced. \n Possible reason: Identity < 80%")
			print("##############################################################")
		os.system("mv {}/phage_coordinates.txt {}/RESULTS".format(scripts,scripts))
		os.system("mv {}/phage_completeness.txt {}/RESULTS".format(scripts,scripts))
		os.system("mv {}/RESULTS {}".format(scripts, fasta_folder))
		os.system("touch {}/all_done".format(scripts))
