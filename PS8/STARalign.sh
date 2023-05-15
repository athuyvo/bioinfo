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

/usr/bin/time -v STAR --runThreadN 9 \
--runMode alignReads \
--outFilterMultimapNmax 3 \
--outSAMunmapped Within KeepPairs \
--alignIntronMax 1000000 \
--alignMatesGapMax 1000000 \
--readFilesCommand zcat \
--readFilesIn "/projects/bgmp/shared/Bi621/dre_WT_ovar12_R1.qtrim.fq.gz" "/projects/bgmp/shared/Bi621/dre_WT_ovar12_R2.qtrim.fq.gz" \
--genomeDir $mydir"Danio_rerio.GRCz11.dna.ens104.STAR_2.7.1a/" \
--outFileNamePrefix "Danio_rerio.GRCz11.dna.aligned"