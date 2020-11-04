#!/bin/bash
eval "$(conda shell.bash hook)"
mv ./ANI/ANI_output.matrix .
R < MakingHeatmaps.R --no-save
touch heatmaps_done