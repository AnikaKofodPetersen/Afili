# Afili
The following is a bioinformatic workflow designed to find related phages and phage remnants. 
The workflow is not restricted to phages by any phage database.


### INSTALLATION
First, clone the repository:

$ git clone https://github.com/AnikaKofodPetersen/Afili.git

Second, make Afili executable:

$ chmod -R 755 Afili/*

Third, move to the Afili folder and initiate installation of all necessary dependencies and environments:

$ cd /path/to/Afili

$  ./Install.sh

$ conda activate afili_env

Lastly, run a test with the available test file as follows:

$ ./afili.sh -F test_fasta --genus bacillus

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

#### MANUAL DATABASE ALTERATIONS
One can delete and add genomes in the databases by deleting or adding database files in the db/folders


### SPECIFICATIONS
[-h --help Help menu]

Necesarry input

[-G --genus Genus of investigation]

[-F --fasta Folder containing a minimal of 1 fasta file for analysis]

Possible inputs

[-T --type Only uses the typestrains of the specified genus]

[-a Run add-on in the pipeline (Not yet available)]

[-i --identity (float) Percent identity threshold used in BLAST]

[-c --coverage (float) Percent query coverage threshold used in BLAST]

[--max (float) Maximal percent length relative to average of original samples]

[--min (float) Minimal percent length relative to average of original samples]

[--genes (float) Minimal amount of the orignial genes that should be present in a putative phage]

[--gap (float) Minimal percent of unknown genes in a phage that in a continous stretch would indicate a gap]

