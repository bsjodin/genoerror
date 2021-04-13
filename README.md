## auto_genoerror.py
### Description
Script for calculating genotyping error among replicate samples in [PLINK](https://www.cog-genomics.org/plink/) format calculated as the percentage of discordant genotypes.

### Usage
```$ ./auto_genoerror.py input_PED input_IDs output_filename```

### Requirements
This script requires three input files:

1) PED file containing all replicate samples and their genotypes (can also included additional, non-replicated samples).
2) MAP file containing locus information
3) Tab-delimited file containing a list of replicate sample information (ie., <i>input_IDs</i>), one per line, with three columns:
   - Sample ID (for saving purposes; can be whatever you chooose)
   - Replicate ID #1 (as appears in PED file)
   - Replicate ID #2 (as appears in PED file)
  
See [*example_IDs.txt*](example_IDs.txt) for an example of this input file.

### Overview
This script has several steps:

1) First, it checks to see that both sample IDs are present in the input PED file. If one is missing, the script will end with the following error:\
```$ Error: ID sample_id not in input_PED!```
2) If all sample IDs are present, the script then parses out the replicate sample IDs.
3) The final step looks for discordant genotypes between the two sample IDs for every locus. Loci with missing data in either replicate sample are not included in the calculation. Allele order does not need to match between replicate samples (ie., a genotype of "GC" in replicate #1 and "CG" in replicate #2 will be considered a match). The information for mismatched loci are printed to file (good for looking for systematic bias at particular loci), as well as the genotyping error for this sample.
4) Mean error across all replicate samples is calculated and printed to file.

### Outputs
There are two output file types created with this script.

The main output file is specified with the *output_filename**. This file is a tab-delimited file containing six columns:
- **SampleID:** the sample ID given in the first column of the *input_IDs* file\
- **#SNPs:** total number of loci with data present in both replicate samples\
- **Matches:** number of loci with concordant genotypes\
- **Mismatches:** number of loci with discordant genotypes\
- **Missing:** number of loci with missing data in at least on replicate (not used in calculation)\
- **ErrorRate:** genotyping error rate (%) between replicates, calculated *Matches/#SNPs*

The second output file type will provide specific information for each set of replicate samples. One file per pair of replicates will be created. This file consists of:
- Line from the PED file for each replicate sample (containings all information
- Summary of mismatched SNPs with three columns:
  - Locus ID (from MAP file)
  - Genotype for the first replicate sample
  - Genotype for the second replicate sample
- Overall summary stats (*Note*: this is the same information found in the main output file)
