#!/bin/bash
eval "$(conda shell.bash hook)"
mv ./ANI/ANI_output.matrix .

small=6
lines=$(wc -l < "ANI_output.matrix")
if [[ "$lines" -lt "$small" ]];then
    echo -e "ERROR MESSAGE: No ANI.pdf heat map was produced. \nPossible reason: Amount of hits was too small.\nFor ANI matrix see ANI_matrix.txt"
else
    R < MakingHeatmaps.R --no-save
fi

touch heatmaps_done
