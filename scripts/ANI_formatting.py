#!/usr/bin/env python3
import os

def get_fastani(filename):
	import numpy as np
	""" Make an ANI matrix file"""
	#Get half matrix
	with open(filename,"r") as matrix:
		start = matrix.readline()
		ani_matrix = []
		headers = []
		for line in matrix:
			row = line.split("\t")
			headers += [row[0]]
			ani_matrix += [[float(i) for i in row[1:]]]

	#Format accordingly
	for pos in range(1,len(ani_matrix[-1])+2):
		ani_matrix[-pos]+=[0]*pos
	x = np.array(ani_matrix)
	x = x + x.T -np.diag(np.diag(x))
	
	#Add a full diagonal
	for row_num in range(0,len(x)):
		for column_num in range(0,len(x)):
			if row_num == column_num:
				x[row_num][column_num] = 100
				
	#Get headers right
	headers[0] = headers[0][:-1]
	headers = [item[2:] for item in headers]
	headers.insert(0,"  ")
	
	#Write output files
	with open("ANI_matrix.txt","a") as outfile:
		outfile.write("\t".join(headers))
		outfile.write("\n")
		for row in range(0,len(x)):
			outfile.write(headers[row+1] +"\t")
			outfile.write("\t".join(str(v) for v in x[row]))
			outfile.write("\n")
			

get_fastani('./ANI/ANI_output.matrix')

