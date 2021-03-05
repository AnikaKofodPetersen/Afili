# Afili
The following is a bioinformatic workflow designed to find related phages and phage remnants. 
The workflow is not restricted to phages by any phage database.

##### Notice: Installing with conda environment is the preferred method of using Afili. You must have conda installed before using Afili.
#### Dependencies:
any2fasta

biopython

blast-legacy

conda

fastANI

fasttree

hmmer

mummer

mlst

ncbi-genome-download

newick_utils

prokka

parallel

perl

pip

Python 3.7 or higher

r-base

r-pheatmap

readline

roary

samtools

snakemake

tbl2asn



### INSTALLATION
First, clone the repository:

$ git clone https://github.com/AnikaKofodPetersen/Afili.git

Second, make Afili executable:

$ chmod -R 755 Afili/*

Third, move to the Afili folder and initiate installation of all necessary dependencies and environments:

$ cd /path/to/Afili

$ conda env create -f afili_env.yml

$ conda activate afili_env

$ prokka --setupdb

$ parallel --citation

Lastly, run a test with the available test file as follows:

$ ./afili.sh -F test_fasta --genus bacillus -O test_output

This might take a while, including the one-time database download.
The results are found in the RESULTS folder placed in the test_fasta folder.

### USE
To use the data analysis pipeline, please do the following:
1) place all prophage sequences in FASTA nucleotide format in a folder

2) call the program in your command line by calling afili.sh with specifications.
Example: $ /path/to/afili.sh -F /path/to/fasta_folder --genus enterococcus -i 80 -T

The example would run the program with the enterococcus genus type strain database while using 80 as the identity threshold for BLAST.
All specifications are listed below or found with the help menu

For visualization of the newick formatted tree, use your favorite tree visualizer, i.e. ITOL: https://itol.embl.de/
The metadata can manually be adapted to suit your tree visualizer. 
For the case of ITOL, please add your visualization type (LABEL, DATASET_BINARY etc.) followed by the seperator line(SEPERATOR TAB) and the data indicator (DATA).
The header should start with # to ensure proper reading by ITOL.

### Input 
Afili works with fasta formatted files og phages. 
Since Afili aims to compare somewhat related genomes, the filtering thresholds are calculated on mean values of the input genomes. 
If input genomes are of uncomparable lengths, it is suggested to run Afili several times, each on a subset of the input genomes, which indeed are comparable in lengths. 

#### Where do I find my results?
Your results will be placed in a folder called RESULTS inside the folder containing your fasta files

#### How do I know how many genes are in the core genome?
The number of core genes and the difinition of core genome can be seen lastly in the output.log file.

### OUTPUT
In the folder containing your fasta files, all new phage-like elements are found as seperate fasta files and an output.log file.
In the folder RESULTS are the following output files:
* phage_completeness.txt:	A file containing information of how many genes are shared between the phage-like element and the original phage
* phage_coordinates.txt:		A file containing information about the coordinates of the phage_like element in the original phage
* SpeciesMetadata.txt:		A file containing species specification (MLST) on the host in which the phage like element was found
* orginalsMetadata.txt:		A file containing the names of the original phage(s) for the sake of tree visualization
* ANI_matrix.txt:			A file containing the Average Nucleotide Identity matrix for the comparrision of all the phage_like elements
* ANI.pdf:					A picture of the Average Nucleotide Identity heat map
* my_tree_collected_analysis_rerooted.nw: 	A phylogenetic tree in newick format of all phage-like elements and original phage(s).


### SPECIFICATIONS
[-h --help Help menu]

Necesarry input

[-G --genus Genus of investigation]

[-F --fasta Folder containing a minimal of 1 fasta file for analysis]

Possible inputs

[-O --output Directory for output files]

[-T --type Only uses the typestrains of the specified genus]

[-a Run add-on in the pipeline (Not yet available)]

[-i --identity (float) Percent identity threshold used in BLAST]

[-cov --coverage (float) Percent query coverage threshold used in BLAST]

[-cor --cores (float) Max amount of cores used by Afili]

[--max (float) Maximal percent length relative to average of original samples]

[--min (float) Minimal percent length relative to average of original samples]

[--genes (float) Minimal amount of the orignial genes that should be present in a putative phage]

[--gap (float) Minimal percent of unknown genes in a phage that in a continous stretch would indicate a gap]


#### MANUAL DATABASE ALTERATIONS
The user can make a custom database by using the add_db.py script. This can be done by running the script and specify the path to the fasta files, the path to the Afili/db folder and the name of the database.

Example: $ python add_db.py -F path/to/my/customfolder/ -DB Afili/db/ -N customdatabase

This will create a custom database made from the fasta files in the folder customfolder. For using this custom database in Afili, use '--genus customdatabase'.


[-H --help  Show this help menu]

[-F --fasta The path to the folder with your fasta or fasta.gz files]

[-DB --database The path to the Afili db folder]

[-N --name  The name of your custom database]

