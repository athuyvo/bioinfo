#!/bin/bash 

#SBATCH --partition=bgmp        ### Partition (like a queue in PBS)
#SBATCH --job-name=STARdb        ### Job Name
#SBATCH --time=00-00:30:00       ### Wall clock time limit in Days-HH:MM:SS
#SBATCH --nodes=1               ### Number of nodes needed for the job
#SBATCH --cpus-per-task=8       ### Number of cpus needed per task
#SBATCH --ntasks-per-node=1     ### Number of tasks to be launched per Node
#SBATCH --account=bgmp          ### Account used for job submission
#SBATCH --output=results-%j.out    ### File in which to store job output
#SBATCH --error=results-%j.err     ### File in which to store job error messages

 
mydir="/projects/bgmp/anhthuyv/bioinfo/Bi621/PS/PS8/"

/usr/bin/time -v STAR --runThreadN 8 --runMode genomeGenerate \
--genomeDir $mydir"Danio_rerio.GRCz11.dna.ens104.STAR_2.7.1a/" \
--genomeFastaFiles $mydir"dre/Danio_rerio.GRCz11.dna.primary_assembly.fa" \
--sjdbGTFfile $mydir"Danio_rerio.GRCz11.106.gtf" 
