# LARRY

LARRY (**L**ineage **a**nd **R**NA **r**ecovery) is a tool for labeling cells with a unique lineage barcode that can be read out in single-cell RNA-seq. The instructions for generating and sequenciung the barcode library are available [HERE]. This repository contains a computational pipeline for transforming raw barcode sequencing data into clonal labels for each cell. 

The pipeline has two steps. Step (1) is built to work with the output of the [indrops pipeline](https://github.com/indrops/indrops), and is therefore not suitable for users of other single-cell RNA-seq methods such as 10X. These users can format the data in the appropriate fastq format (see below) and then apply step (2) from this pipeline. 

1. Sorting and filtering of raw sequencing reads
    * Input: Standard files generated from the [indrops pipeline](https://github.com/indrops/indrops)
    * Output: A fastq file with barcode sequences and headers indicating library name, cell barcode and UMI 

2. Clonal annotation of cells
    * Input: The output of step 1 (fastq file with barcodes and headers indicating library nane, cell barcode and UMI)
    * Output: NxM binary matrix, where entry (i,j) is 1 if cell i is in clone j, as well as several plots for evaluating parameter choices are also output. 


## Step 1: Sorting and filtering of barcode sequencing reads

The purpose of step 1 is to parse the standard output of the indrops pipeline and generate a single file that lists all the valid barcode reads with their associated metadata. The pipeline assumes that the reads were generated from targeted sequencing of the LARRY barcodes, using one of the following (forward) primers for targeting:

```
TCGTCGGCAGCGTCAGATGTGTATAAGAGACAGNNNNcaagtaacgaagagtaaccgttgcta
TCGTCGGCAGCGTCAGATGTGTATAAGAGACAGNNNNtaaccgttgctaggagagaccatatg
```

To perform step (1), copy the ```LARRY_sorting_and_filtering.py``` script (from this repository) into the ```output``` directory of the indrops pipeline, and then run it from the command line:

``` python LARRY_sorting_and_filtering.py```

The script assumes that the output of the indrops pipeline has the following file structure:

```
output
├──[Library_name_1]
│   ├──abundant_barcodes.pickle
│   └──filtered_parts
│        └──[Library_name_1]_[Index_1]_.fastq
└──Library_name_N
    ├──abundant_barcodes.pickle
    └──filtered_parts
         └──[Library_name_N]_[Index_N]_.fastq
```

The script will output a fastq file called ```LARRY_sorted_and_filtered_barcodes.fastq.gz```, which can be carried forward to step (2). Each entry of the fastq file includes a library name, cell barcode, UMI and LARRY barcode sequence, as follows:

```
>[Library name],[cell barcode],[UMI]
[LARRY barcode sequence]
```

For example, a typical entry might look like

```
>Sample1,bcEDSG,CGGATC
ACTATGTACACAGCGGACAATCGAACGAG
```

## Step 2: Clonal annotation of cells

The purpose of step 2 is to aggregate the barcode reads for each cell and perform a series of filtering and quality control steps to produce a final clonal annotation. 

The inputs are

1. A fastq file with the format described above for ```LARRY_sorted_and_filtered_barcodes.fastq.gz```
2. An ordered list of cell barcodes, corresponding to the rows of the gene expression counts matrix, having the form of a text file with one cell barcode per line
3. An ordered list of library names, corresponding to the rows of the gene expression counts matrix, having the form of a text file with one library name per line

Note that files (2) and (3) in the above list are output by the [SPRING data_prep pipeline for indrops data] (https://github.com/AllonKleinLab/SPRING_dev/blob/master/data_prep/spring_example_HPCs.ipynb) as ```cell_bcs_flat.txt``` and ```samp_id_flat.txt```. 

The output is a NxM binary matrix called ```clone_mat.csv```, where entry (i,j) is 1 if cell i is in clone j, as well as several plots for evaluating parameter choices.

The filtering step are:

1. Collapse the data into unique (Cell,UMI,barcode) triples, keeping track of their respective multiplicities
2. Merge barcode sequences that are highly similar, i.e. that have a hamming distance less than or equal to *H*
3. Filter out (Cell,UMI,BC) triples that are supported by fewer than _R_ reads
4. Make a final list of (Cell,BC) pairs, keeping those that are supported by at least _U_ UMIs

To run the clonal annotation pipeline, open the ```clonal_annotation.ipynb``` jupyter notebook (from this repository) and follow the instructions in the comments. 
