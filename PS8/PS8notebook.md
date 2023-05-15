# Problem set 8

### Getting started 
***

We will be working with RNA-seq data obtained from zebrafish ovaries. 

Location of fastq files:
*Reference the data, don't copy it!*

```
/projects/bgmp/shared/Bi621/dre_WT_ovar12_R1.qtrim.fq.gz
/projects/bgmp/shared/Bi621/dre_WT_ovar12_R2.qtrim.fq.gz
```

Directory that holds the zebrafish genome assembly files:
```
/projects/bgmp/anhthuyv/bioinfo/Bi621/PS/PS8/dre
```

Download zebrafish reference genome by chromsome (FASTA) and gene set (GTF) on Ensemble website:
```
Danio_rerio.GRCz11.dna.primary_assembly.fa.gz
Danio_rerio.GRCz11.106.gtf.gz
```

Install STAR and Samtools:
```
$ conda activate bgmp_py310
$ conda install star -c bioconda
$ STAR --version
$ conda install samtools -c bioconda
$ samtools --version
```
Use ensembl version 106 and STAR 2.7.10a.

***
## Building a STAR database and aligning
***


Building a star database out of the reference sequence using the STAR program ```--runMode genomeGenerate.```
* Does not take compressed file. Must unzip.

This will kmerize the genome to build a STAR database. To build database see ```STARdb.sh``` script. 

Run STAR to align the reads to the reference genome. Use the queueing system and request 8 cores on 1 node. See ```STARalign.sh``` script. 

```
ERROR:
gzip: /projects/bgmp/anhthuyv/bioinfo/Bi622/QAA/22_3H_both_S16_L008_R1_001.trimmedpaired.fastq.gz: not in gzip format
```

SOLVED: changed ```--readFilesCommand zcat ``` to ```--readFilesCommand cat ```

View the results of the alignment with ```less```. 
Aligned output file:
```
Danio_rerio.GRCz11.dna.alignedAligned.out.sam
```

Use ```samtools``` (enter ```samtools``` on the command line with no options to get help screen), convert the SAM file to BAM format. Then sort the bam file and extract all reads from chromosome 1 into a new SAM file. Report how many alignments are on chromosome 1.

```
samtools view -S -b Danio_rerio.GRCz11.dna.alignedAligned.out.sam > Danio_rerio.GRCz11.dna.alignedAligned.out.bam

samtools sort Danio_rerio.GRCz11.dna.alignedAligned.out.bam -o Danio_rerio.GRCz11.dna.alignedAligned.out.sorted.bam

samtools index Danio_rerio.GRCz11.dna.alignedAligned.out.sorted.bam samtools view Danio_rerio.GRCz11.dna.alignedAligned.out.sorted.bam 1 > chromosome1.sam

wc -l chromosome1.sam
```

***
## Parse through SAM file
***

Write a python program to parse the contents of the SAM file. The program will count up the number of reads that are properly mapped to the reference genome and the number of reads that are not mapped the to genome. 
* Note- You may encounter each read in a file more than once. This willo ccur when you hve multiple aligntments for a single read. Be careful not to count reads as aligned more than once. 

Use the bit-wise flag in SAM file header to check if reads are mapped and if they've aligned more than once. 

https://user-images.githubusercontent.com/1646180/178063344-9b215b6a-343a-4792-a31f-58bd5914716a.png

Use the original SAM file: ```Danio_rerio.GRCz11.dna.alignedAligned.out.sam```

See ```parseSAM.py``` script.

Output: 
```
Num reads mapped:  21851108
Num reads unmapped:  1646070
```


