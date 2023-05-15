
# PROBLEM SET PS7.

### ****************************************************************** 
### Finding the longest protein Human and Zebrafish using fasta files. 
### ******************************************************************

see ```longest2.py``` script. 

Used python version 3.10.4

# Writing script # 

 Find longest protein given fasta file and output the longest protein sequence to a fasta file. The output fasta file will then be used to align Human longest protein to Zebrafish longest protein and vis versa using BLASTp.

Ue

*************************** PROBLEM*******************************************
* WAS GETTING DUPLICATE GENE IDS IN OUTPUT FASTA FILE. EACH GENE SHOULD ONLY HAVE
ONE LONGEST PROTEIN SEQUENCE
* GENE IDS ARE ASSOCIATED WITH DIFFERENT PROTEIN IDS 
  EG ONE GENE ID CAN HAVE MULTIPLE PROTEIN IDS. 
************************* PLAN ON HOW TO FIX ********************************
* USE PROTEIN ID AS THE UNIQUE IDENTIFIER. FIND PROTEIN ID INSTEAD OF 
  GENE ID (STARTS WITH ENSP; GENE ID STARTS WITH ENSG). USE THIS PROTEIN ID 
  TO STORE AS KEY IN DICTIONARY WITH FASTA SEQUENCES. THEN GO BACK & CHANGE KEY 
  IN PROTEIN DICTIONARY TO PROTEIN ID. THEN USE PROTEIN ID TO WRITE OUT RECORDS ******************************************************************************


NOPE. DID NOT WORK WHEN I TRIED THAT. 

#### RESULTS:

Used gene ID as key in dictionary and protein sequence as value because each proteinID could be associated many of the same gene ID, which gave expected resultls. When using the protein ID as key, got more than ~190000 long protein records in human protein sequences instead expected 23,506 records.  


 *************** PROBLEM & SOLUTION ****************

DanioLongProtein should have 30,313 longest proteins, but only getting 30,312


 **************** Problem solved. ***************** 

Script wasn't checking the very last protein sequence. Moved the protein check point to the end of ```"if newline.startswith(">"): ... else : protein += len(newLine)"``

Instead, got rid of the hum mart dictionary and just stored all protein ID, gene ID and gene name in a dictionary. 


Run script to find longest protein in Human fasta file:
```./longest2.py -f Homo_sapiens.GRCh38.pep.all.fa -o HumanLongProtein.fa```

Run script to find longest protein in Danio (zebrafish) fasta file:
```./longest2.py -f Danio_rerio.GRCz11.pep.all.fa -o DanioLongProtein.fa```


### Analyzed results on Talapas using spider and bbmap modules.
```
/usr/bin/time -v stats.sh in=DanioLongProtein2.fa out=Zfish_LP_stats.txt
        Command being timed: "stats.sh in=DanioLongProtein2.fa out=Zfish_LP_stats.txt"
        User time (seconds): 0.41
        System time (seconds): 0.02
        Percent of CPU this job got: 63%
        Elapsed (wall clock) time (h:mm:ss or m:ss): 0:00.69
        Average shared text size (kbytes): 0
        Average unshared data size (kbytes): 0
        Average stack size (kbytes): 0
        Average total size (kbytes): 0
        Maximum resident set size (kbytes): 44848
        Average resident set size (kbytes): 0
        Major (requiring I/O) page faults: 0
        Minor (reclaiming a frame) page faults: 11428
        Voluntary context switches: 141
        Involuntary context switches: 30
        Swaps: 0
        File system inputs: 0
        File system outputs: 64
        Socket messages sent: 0
        Socket messages received: 0
        Signals delivered: 0
        Page size (bytes): 4096
        Exit status: 0
```

```/usr/bin/time -v stats.sh in=HumanLongProtein2.fa out=Human_LP_stats.txt
        Command being timed: "stats.sh in=HumanLongProtein2.fa out=Human_LP_stats.txt"
        User time (seconds): 0.36
        System time (seconds): 0.02
        Percent of CPU this job got: 76%
        Elapsed (wall clock) time (h:mm:ss or m:ss): 0:00.51
        Average shared text size (kbytes): 0
        Average unshared data size (kbytes): 0
        Average stack size (kbytes): 0
        Average total size (kbytes): 0
        Maximum resident set size (kbytes): 45216
        Average resident set size (kbytes): 0
        Major (requiring I/O) page faults: 0
        Minor (reclaiming a frame) page faults: 10861
        Voluntary context switches: 112
        Involuntary context switches: 22
        Swaps: 0
        File system inputs: 0
        File system outputs: 64
        Socket messages sent: 0
        Socket messages received: 0
        Signals delivered: 0
        Page size (bytes): 4096
        Exit status: 0
```

Start an interactive session on Talapas:
```srun --account=bgmp --partition=bgmp --nodes=1 --ntasks-per-node=1 --time=1:00:00 --cpus-per-task=1 --pty bash```

```module load bbmap``` to run ```stats.sh``` on fasta files of longest human proteins and longest zebrafish proteins

See ```Human_LP_stats.txt``` and ```Zfish_LP_stats.txt```



## RUNNING BLAST
##########################

Used BLAST+ version 2.2.31

```module spider BLAST+/2.2.31``` # information about blast
```module load easybuild``` # need to load this before loading blast 
```module load BLAST+/2.2.31``` # load blast 
  
makeblastdb referernce: https://www.ncbi.nlm.nih.gov/books/NBK569841/

```
makeblastdb [-h] [-help] [-in input_file] [-input_type type]
    -dbtype molecule_type [-title database_title] [-parse_seqids]
    [-hash_index] [-mask_data mask_data_files] [-mask_id mask_algo_ids]
    [-mask_desc mask_algo_descriptions] [-gi_mask]
    [-gi_mask_name gi_based_mask_names] [-out database_name]
    [-max_file_sz number_of_bytes] [-logfile File_Name] [-taxid TaxID]
    [-taxid_map TaxIDMapFile] [-version]
```

```makeblastdb -in "HumanLongProtein.fa" -input_type fasta -title "Human Long Protein Database" -hash_index -dbtype prot -out "HumanLongProteinDB" ```


```makeblastdb -in "DanioLongProtein.fa" -input_type fasta -title "Danio Long Protein Database" -hash_index -dbtype prot -out "DanioLongProteinDB"```


blastp reference: https://angus.readthedocs.io/en/2016/running-command-line-blast.html


See ```runBLASTHumtozeb.sh``` and ```runBLASTZebtoHum.sh``` for blastp script.


##########################
##                      ##  
## BLAST run completed. ##
##                      ## 
##########################

Getting error for both Danio and Human:
example: 

```
Warning: [blastp] lcl|Query_26000 ENSDARP00000137608 ENSDARG00000099664 selenof: Warning: One or more U or O characters replaced by X for alignment score calculations at positions 83 
```
Warning is normal per Leslie.


**BLAST output format** in ```HumantoDanioResults2.txt``` and ```DaniotoHumanResults2.txt```: 

```
BLAST tabular output format 6
Column headers:
qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore
 
1.  qseqid      query or source (e.g., gene) sequence id
2.  sseqid      subject  or target (e.g., reference genome) sequence id
3.  pident      percentage of identical matches
4.  length      alignment length (sequence overlap)
5.  mismatch    number of mismatches
6.  gapopen     number of gap openings
7.  qstart      start of alignment in query
8.  qend        end of alignment in query
9.  sstart      start of alignment in subject
10.  send        end of alignment in subject
11.  evalue      expect value
12.  bitscore    bit score 
 ```

Create summary information for each comparison. See ```output_summary.md```


########################
##                    ## 
##      E-values      ##
##                    ##     
########################

Expectation values are corrected bit-score adjusted to the *sequence database size*. Therefore, E-values cannot not be compared acoss databases since the value depends on the sequence database.

**When comparing E-value:** the smaller, the better the match.
Small E-value: low number of hits, but of high quality. 
Blast hits with an E-value smaller than **1e-50** includes database of very high quality.
<0.01: still considered good hit for homology matches. 
<10: Large E-value. Many hits, partly of low quality. Cannot be considered significant, but may give an idea of potential relations. 


########################
##                    ## 
##      Bit-score     ##
##                    ##     
########################


The bit-score is the *required size of a sequence database* in which the current match could be found just by chance. 
The higher the bit-score, the better sequence similarity.
A bit score of 50 is almost always significant.
Can be used for searching in a constantly increasing database. 


**See ```output_summary.md``` for summary of results.**


### Questions

1. By eye, look at a couple of hits from human to zebrafish and zebrafish to human that have similar e-values. How do the bitscores compare? Why would the bitscores be different?

```
The bit scores differ significantly when the evalue are at 0. The bit scores will differ if the alignments done with different databases eg. human protein sequences were aligned with the zebrafish database while the zebrafish were aligned with the human data base. E-scores are dependent on the size of the database and the size of these two databases differ. 
```

2. What is the ```-use_sw_tback``` parameter and why would you want to include it?

```
This uses the Smith-Waterman local alignment in order to determine the difference between sequences. This is useful when interested in the shift in the sequence of the gene to determine the divergence of time. Eg. divergence of zebrafish to human.
```
