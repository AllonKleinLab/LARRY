# LARRY

LARRY (**L**ineage **a**nd **R**NA **r**ecovery) is a tool for labeling cells with a unique lineage barcode that can be read out in single-cell RNA-seq. The instructions for generating and sequenciung the barcode library are available [HERE]. This repository contains a computational pipeline for transforming raw barcode sequencing data into clonal labels for each cell. 

The pipeline has two steps. Step (1) is built to work with the output of the [indrops pipeline](https://github.com/indrops/indrops), and is therefore not suitable for users of other single-cell RNA-seq methods such as 10X. These users can format the data in the appropriate fastq format (see below) and then apply step (2) from this pipeline. 

1. Sorting and filtering of raw sequencing reads
    * Input: Standard files generated from the [indrops pipeline](https://github.com/indrops/indrops)
    * Output: A fastq file with barcode sequences and headers indicating library name, cell barcode and UMI 

2. Assignment of clonal labels to each cell
    * Input: The output of step 1 (fastq file with barcodes and headers indicating library nane, cell barcode and UMI)
    * Output: NxM binary matrix, where entry (i,j) is 1 if cell i is in clone j, as well as several plots for evaluating paramnter choices are also output. 


## Sorting and filtering of raw sequencing reads

To perform step (1), copy the ```LARRY_sorting_and_filtering.py``` script (from this repository) into the ```output``` directory of the indrops pipeline, and then run it from the command line:

``` python LARRY_sorting_and_filtering.py```

The script assumes that the output of the indrops pipeline has the following file structure:

```
output
├──[Library_name_1]
│   ├──abundant_barcodes.pickle
│   └──filtered_parts
│        └──[Library_name_1]_[Index_1]_.fastq.sorted.fastq.gz
└──Library_name_N
    ├──abundant_barcodes.pickle
    └──filtered_parts
         └──[Library_name_N]_[Index_N]_.fastq.sorted.fastq.gz
```

The script will output a fastq file called ```LARRY_sorted_and_filtered_barcodes.fastq```, which can be carried forward to step (2). Each entry of the fastq file includes a library name, cell barcode, UMI and LARRY barcode sequence, as follows:

```
>[Library name],[cell barcode],[UMI]
[LARRY barcode sequence]
```

For example, a typical entry might look like

```
>Sample1,CTATCG-GTTCAT,CGGATC
ACTATGTACACAGCGGACAATCGAACGAG
```


