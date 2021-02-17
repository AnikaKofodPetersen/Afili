fasta_folder = "/mnt/c/Users/anika/desktop/Afili/test_fasta"
scripts = "/mnt/c/Users/anika/desktop/Afili"

import os
#Restarting for a new analysis
os.system("mv {}/scripts/*.fna {}/RESULT_fastas/. > /dev/null 2>&1".format(scripts,fasta_folder))
os.system("mv RESULTS {} > /dev/null 2>&1 ".format(fasta_folder))


#deleting uneccessary files
os.system("rm -r ./database_fastas/* > /dev/null 2>&1")
os.system("rm -r ./scripts/.snakemake > /dev/null 2>&1")
os.system("rm -r ./scripts/altered_scripts > /dev/null 2>&1")
os.system("rm -r ./scripts/ANI > /dev/null 2>&1")
os.system("rm -r ./scripts/blast_folder > /dev/null 2>&1")
os.system("rm -r ./scripts/collected_analysis > /dev/null 2>&1")
os.system("rm -r ./scripts/host_fastas > /dev/null 2>&1")
os.system("rm -r ./scripts/newick_trees > /dev/null 2>&1")
os.system("rm -r ./scripts/preliminary_files > /dev/null 2>&1")
os.system("rm -r ./scripts/prokka_[^a-zA-Z] > /dev/null 2>&1")
os.system("rm -r ./restart_prep.txt > /dev/null 2>&1")


print("Restart has been done")
