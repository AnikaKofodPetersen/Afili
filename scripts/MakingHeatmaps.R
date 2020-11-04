r = getOption("repos")
r["CRAN"] = "http://cran.us.r-project.org"
options(repos = r)

if(!require(pheatmap)){
  install.packages("pheatmap")
  library(pheatmap)
}


#Making heatmap 
coverage_table <- read.table("ANI_matrix.txt")
fontsize_pre = 10 - nrow(coverage_table) / 4
if (fontsize_pre < 1){
  row <- FALSE
  col <- FALSE
} else {
  row <- TRUE
  col <- TRUE
}
fontsize = 10
title <- "ANI"
pheatmap(coverage_table, fontsize = fontsize,show_rownames = row, show_colnames = col, filename="ANI.pdf",main=title,border_color = NA)
