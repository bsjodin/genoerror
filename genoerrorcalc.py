#!/usr/bin/env python3
#This script automatically generates genotyping error a series of replicate samples within a single input file. 
#Call this script using "python genoerrorcalc.py input_ped input_ids output_filename"

import sys
import re
import time
import os

#Import .ped file, sample IDs
File = sys.argv[1] #a PED file (aka. plink)
InFile = open(File,'r')
SampIDs = sys.argv[2] #tab-delim, first column is for saving to file, columns 2 and 3 are for the replicate sample IDs
SampIDs = open(SampIDs,'r')
MeanError = open(sys.argv[3],'w') #output file for overall error across the library
MeanError.write("#Gentoyping error for %s\nSampleID\t#SNPs\tMatches\tMismatches\tMissing\tErrorRate" % File)
MAP = open(sys.argv[1].replace('ped','map'),"r")
Loci = MAP.readlines()

error_num = 0
num_samps = 0

#Check if sample IDs are present in the InFile
for Line in SampIDs:
	num_samps = num_samps + 1
	Line = Line.strip('\r\n')
	List = Line.split()
	rep_1 = List[1]
	rep_2 = List[2]
	out = List[0]+".txt"
	OutFile = open(out,'w')
	with open(sys.argv[1],'r') as check:
		if rep_1 not in check.read():
			print("\nError: ID %s not in InFile!" % (rep_1))
			quit()
		check.seek(0)	
	with open(sys.argv[1],'r') as check:
		if rep_2 not in check.read():
			print("\nError: ID %s not in InFile!\n" % (rep_2))
			quit()
	print("\nChecking discordance between %s and %s" % (rep_1,rep_2))
	time.sleep(3)

	#parse out gentoypes for replicates
	idcheck = 0
	InFile.seek(0)
	for Line in InFile:
		idcheck = idcheck + 1
		Line = Line.strip('\r\n')
		ElementList = Line.split()
		if rep_1 in ElementList:
			rep_1 = rep_1+'\t'+Line
			print("Found a match for replicate 1!")
			OutFile.write(rep_1+'\n')
		elif rep_2 in ElementList:
			rep_2 = rep_2+'\t'+Line
			print("Found a match for replicate 2!")
			OutFile.write(rep_2+'\n')
		else:
			print("Scanned %d samples" % (idcheck), end ="\r\r")
	
	#look for discordant matches and write to file
	OutFile.write('\nMismatched SNPs\n')
	allele_1 = 6
	allele_2 = 7
	rep_1 = rep_1.split()
	rep_2 = rep_2.split()
	num_snps = len(rep_1)
	Matches = 0
	MisMatches = 0
	Missing = 0
	Locus_num = 0
	total_loci = 0
	while allele_2 < num_snps:
			Locus_num = Locus_num + 1
			ind1_gen1 = rep_1[allele_1]+rep_1[allele_2]
			ind1_gen2 = rep_1[allele_2]+rep_1[allele_1]
			ind2 = rep_2[allele_1]+rep_2[allele_2]
			allele_1 = allele_1 + 2
			allele_2 = allele_2 + 2
			missing1 = ind1_gen1.count("0")
			missing2 = ind2.count("0")
			if missing1 > 0 or missing2 > 0:
				Missing = Missing + 1
				continue
			elif  ind1_gen1 == ind2 or ind1_gen2 == ind2:
				Matches = Matches + 1
				total_loci += 1
			else:
				Locus = Loci[Locus_num - 1]
				Locus = Locus.strip("\r\n")
				Locus = Locus.split()
				OutFile.write("%s:\tGenotype_1=%s\tGenotype_2=%s\n" % (Locus[1],ind1_gen1,ind2))
				MisMatches = MisMatches + 1
				total_loci += 1
			print("Processed %d loci." % (Locus_num), end="\r")
	error_rate = MisMatches/total_loci*100
	print("\nThere were %d mismatches out of %d comparisons. Overall genotyping error rate = %s percent" % (MisMatches,total_loci,(str(round(error_rate,2)))))
	OutFile.write("\nTotal loci = %d\nThere were %d matches, %d mismatches, and %d missing genotypes\nOverall genotyping error = %f percent" % (total_loci,Matches,MisMatches,Missing,error_rate))
	OutFile.close()
	MeanError.write('\n'+str(List[0])+'\t'+str(total_loci)+'\t'+str(Matches)+'\t'+str(MisMatches)+'\t'+str(Missing)+'\t'+str(error_rate))
	error_num = error_num + error_rate
mean_error = round(error_num/num_samps,2)
print("\n\nOverall error rate for this library: %s percent" % (str(mean_error)))

InFile.close()
MeanError.close()
