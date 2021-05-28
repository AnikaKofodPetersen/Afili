#!/bin/bash
fasta_folder="$/mnt/c/Users/anika/desktop/Afili/test_fasta"
scripts="$/mnt/c/Users/anika/desktop/Afili"


#Remove done files
cd ./scripts
rm all_done > /dev/null 2>&1
rm prokka_prophage_done > /dev/null 2>&1
rm blast_done > /dev/null 2>&1
rm filtering_done > /dev/null 2>&1
rm collection_host_done > /dev/null 2>&1
rm unique_lines_done > /dev/null 2>&1
rm collected_phages_done > /dev/null 2>&1
rm antismash_done > /dev/null 2>&1
rm Prokka_collected_done > /dev/null 2>&1
rm collected_analysis_done > /dev/null 2>&1
rm mlst_done > /dev/null 2>&1
rm phylogeny_display_done > /dev/null 2>&1
rm ANI_done > /dev/null 2>&1
rm heatmaps_done > /dev/null 2>&1
rm start_done > /dev/null 2>&1
rm -r add_on_done > /dev/null 2>&1
rm -r skip_phylogeny > /dev/null 2>&1
rm -r end_snakemake

#Move preliminary files
mkdir preliminary_files > /dev/null 2>&1
mv end_snakemake preliminary_files > /dev/null 2>&1
mv attachment.txt preliminary_files > /dev/null 2>&1
mv host_mlst.txt preliminary_files > /dev/null 2>&1
mv original_names.txt preliminary_files > /dev/null 2>&1
mv ThresholdPhageLog.txt preliminary_files > /dev/null 2>&1
mv ANI_output.matrix preliminary_files > /dev/null 2>&1


#remove preliminary scripts 
rm blast.py > /dev/null 2>&1
rm blast_pre.py > /dev/null 2>&1
rm collection_host.py > /dev/null 2>&1
rm filter.py > /dev/null 2>&1
rm phylogeny_display.py > /dev/null 2>&1

                                                                      
#Move originals and results back to starting position
mv *.fna $fasta_folder > /dev/null 2>&1
mv output.log ${fasta_folder:1}/ > /dev/null 2>&1
mv collected_phages/*.fna ${fasta_folder:1} > /dev/null 2>&1
for fasta in *.fna; do mv "$fasta" "${fasta:8}"; done
rm -r collected_phages > /dev/null 2>&1

#Remove altered snakefile
cd .. > /dev/null 2>&1
rm snakefile_run.py > /dev/null 2>&1

echo "A Cleanup has been performed. Find results in the RESULTS folder"
