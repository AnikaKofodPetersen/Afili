#!/bin/bash
#Save command line arguments and path 
add="${@}"
afili_path="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
if [[ $add == *"--cores"* ]]; then
	search="--cores "
	end="${add#*$search}"
	cores="$(cut -d' ' -f 1 <<< $end)"
elif [[ $add == *"-cor"* ]]; then
	search="-cor "
	end="${add#*$search}"
	cores="$(cut -d' ' -f 1 <<< $end)"
else
	cores="$(nproc)"
fi
#Check command line arguments and print help
if [[ $add == *"-h"* ]] || [[ $add == *"--help"* ]]; then
	echo "The help menu for Afili:"
	echo "[-h --help help menu]"
	echo "Necesarry input"
	echo "[-G --genus Genus of investigation]"
	echo "[-F --fasta Folder containing a minimal of 1 fasta file for analysis]"
	echo "Possible inputs"
	echo "[-O --output Directory for output files]"
	echo "[-T --type only uses the typestrains of the specified genus]"
	echo "[-a run add-ons in the pipeline (Not yet available)]"
	echo "[-i --identity (float) Percent identity threshold used in BLAST]"
	echo "[-cov --coverage (float) Percent query coverage threshold used in BLAST]"
	echo "[-cor --cores (float) Max amount of cores used by Afili]"
	echo "[--max (float) Maximal percent length relative to average of original samples]"
	echo "[--min (float) Minimal percent length relative to average of original samples]"
	echo "[--genes (float) Minimal amount of the orignial genes that should be present in a putative phage]"
	echo "[--gap (float) Minimal percent of unknown genes in a phage that in a continous stretch would indicate a gap]"
	exit 1
fi

python $afili_path/initializing.py $add $cores
#Check for errors
errors=$?
if [ $errors -ne 0 ]; then
	./cleanup.sh
    python restart.py
	exit 1
fi
#Running the actual data analysis
snakemake -s $afili_path/snakefile_run.py --cores $cores
#Running clean up
cd $afili_path
#./cleanup.sh
#python restart.py
