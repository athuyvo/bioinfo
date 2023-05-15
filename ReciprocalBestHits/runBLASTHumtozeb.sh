#!/bin/bash 

#SBATCH --partition=bgmp                ### Partition (like a queue in PBS)
#SBATCH --job-name=BlastHumtoZeb        ### Job Name
#SBATCH --output=SlurmHumtoZeb-%j.out   ### File in which to store job output
#SBATCH --error=SlurmHumtoZeb-%j.err    ### File in which to store job error messages
#SBATCH --nodes=1                       ### Number of nodes needed for the job
#SBATCH --cpus-per-task=8               ### Number of cpus needed per task
#SBATCH --ntasks-per-node=1             ### Number of tasks to be launched per Node
#SBATCH --nodelist=n226
#SBATCH --account=bgmp                  ### Account used for job submission
#SBATCH --mail-user=anhthuyv@uoregon.edu    ### Send email when job is done

# Align Human long protein sequences to Zebra fish long protein sequences

module load easybuild
module load eb-hide/1
module load BLAST+/2.2.31

dir="/projects/bgmp/anhthuyv/bioinformatics/Bi621/PS7"

/usr/bin/time -v \
blastp -query HumanLongProtein.fa -db $dir/DanioLongProteinDB/DanioLongProteinDB -evalue 1e-6 -use_sw_tback -out HumantoDanioResults2.txt -outfmt 6


