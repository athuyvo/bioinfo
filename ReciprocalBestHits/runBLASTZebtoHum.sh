#!/bin/bash 

#SBATCH --partition=bgmp            ### Partition (like a queue in PBS)
#SBATCH --job-name=BlastZebtoHum    ### Job Name
#SBATCH --output=SlurmZebtoHum-%j.out     ### File in which to store job output
#SBATCH --error=SlurmZebtoHum-%j.err      ### File in which to store job error messages
#SBATCH --nodes=1                   ### Number of nodes needed for the job
#SBATCH --cpus-per-task=8           ### Number of cpus needed per task
#SBATCH --ntasks-per-node=1         ### Number of tasks to be launched per Node
#SBATCH --nodelist=n226
#SBATCH --account=bgmp              ### Account used for job submission
#SBATCH --mail-user=anhthuyv@uoregon.edu ### Send email when job is done

# Align Zebra fish long protein sequences to Human long protein sequences

module load easybuild
module load eb-hide/1
module load BLAST+/2.2.31

dir="/projects/bgmp/anhthuyv/bioinformatics/Bi621/PS7"

/usr/bin/time -v\
blastp -query DanioLongProtein.fa -db $dir/HumanLongProteinDB/HumanLongProteinDB -evalue 1e-6 -use_sw_tback -out DaniotoHumanResults2.txt -outfmt 6


