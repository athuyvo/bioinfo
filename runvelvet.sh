#!/bin/bash 

#SBATCH --partition=bgmp        ### Partition (like a queue in PBS)
#SBATCH --job-name=Velvet       ### Job Name
#SBATCH --output=slurm-%j.out   ### File in which to store job output
#SBATCH --error=slurm-%j.err    ### File in which to store job error messages
#SBATCH --time=0-00:30:00       ### Wall clock time limit in Days-HH:MM:SS
#SBATCH --nodes=1               ### Number of nodes needed for the job
#SBATCH --cpus-per-task=2       ### Number of cpus needed per task
#SBATCH --mem=3G                ### Number of ram memory per task
#SBATCH --ntasks-per-node=1     ### Number of tasks to be launched per Node
#SBATCH --account=bgmp          ### Account used for job submission
 
conda activate bgmp-velvet
conda install matplotlib

mydir="/projects/bgmp/anhthuyv/bioinformatics/Bi621/PS6/"
fq1="/projects/bgmp/shared/Bi621/800_3_PE5_interleaved.fq_1"
fq2="/projects/bgmp/shared/Bi621/800_3_PE5_interleaved.fq_2"
fq_unm="/projects/bgmp/shared/Bi621/800_3_PE5_interleaved.fq.unmatched"

kmer_list="31 41 49"
cov_list="20 60"

cd $mydir

# run velveth for each kmer length in kmer list  
for kmer in $kmer_list
    do 
    velveth k$kmer $kmer -fastq -interleaved $fq_unm -fastq -separate $fq1 $fq_2
    done

# velveth k31 31 -fastq $fq_unm -fastq -separate $fq1 $fq_2

# copy velveth output directories for kmer length to new directories 
# for each coverage in coverage list 
# then run velvetg on kmer length with an auto coverage cut-off

for kmer in $kmer_list
    do 
    cp k$kmer k$kmer.cov_auto.len.default -r
    velvetg k$kmer.cov_auto.len.default -exp_cov auto -cov_cutoff auto -ins_length auto
done


# run velvetg with different coverages with a kmer size of 31

for cov in $cov_list
    do 
    cp k31 k31.cov_$cov.len.default -r
    velvetg k31.cov_$cov.len.default -exp_cov auto -cov_cutoff $cov -ins_length auto
done

# run velvetg with kmer size 31, min contig length 500bp and auto coverage cutoff 

cp k31 k31.cov_auto.len.500 -r
velvetg k31.cov_auto.len.500 -exp_cov auto -cov_cutoff auto -ins_length auto -min_contig_lgth 500


filename="k31*/contigs.fa"
ls -1 $filename | while read line
    do ./P6.py -f $line -o $line.tsv -g $line.png -k 31
    done
exit 