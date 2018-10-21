# LARRY

LARRY (**L**ineage **a**nd **R**NA **r**ecovery) is a tool for labeling cells with a unique lineage barcode that can be read out in single-cell RNA-seq. The instructions for generating and sequenciung the barcode library are available [HERE]. This repository contains a computational pipeline for transforming raw barcode sequencing data into clonal labels for each cell. The pipeline has two steps. Step (1) is built to work with the output of the indrops pipeline, and is therefore not suitable for users of other single-cell RNA-seq methods such as 10X. These users can format the data in the appropriate fastq format (see below) and then apply step 2 from thios pipeline. 

1. Sorting and filtering of raw sequencing reads
    * Input: Files generated from the indrops pipeline, including...
      * Balh1
      * Blah2
    * Output: A fastq file with barcode sequences and headers indicating library nane, cell barcode and UMI, e.g. 

```
>Sample1,CTATCG-GTTCAT,CGGATC
ACTATGTACACAGCGGACAATCGAACGAG
```

2. Assignment of clonal labels to each cell
    * Input: The output of step 1 (fastq file with barcodes and headers indicating library nane, cell barcode and UMI
    * Output: NxM binary matrix, where entry (i,j) is 1 if cell i is in clone j, as well as several plots for evaluating paramnter choices are also output. 
