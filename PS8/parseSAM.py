#!/usr/bin/env python

__version__="0.1"

# This script parses through a SAM file and counts the number of reads that are 
# properly mapped to the reference genome and number of reads that are not mapped. 


filename="/projects/bgmp/anhthuyv/bioinfo/Bi621/PS/PS8/Danio_rerio.GRCz11.dna.alignedAligned.out.sam"

num_map = 0 # number of mapped reads
num_unmap =0 # number of unmapped reads 

with open(filename, "r") as file: 

    # parse through SAM file and reads only the alignment section 
    # and checks the bit-wise flag of each alignment 
    for line in file: 
    
        if not line.startswith("@"): # don't grab header lines
            newLine= line.split("\t")
            flag = int(newLine[1]) # read only the bit-wise flag 

            # check to see if read is mapped and only count primary alignment
            # (reads can be aligned more than once)
            # ampersand will compare numbers as bit-wise (refe4 to bit-wise documentation)
            # 4 bit encodes for the alignment segment is unmapped 
            # 256 bit encodes for secondary alignment
            
            if ((flag & 256) != 256): 
                if((flag & 4) != 4):  
                    mapped = True 
                    num_map +=1
            else:
                unmapped = True
                num_unmap +=1

                
print("Num reads mapped: ", num_map, end="\n")
print("Num reads unmapped: ", num_unmap, end="\n")
        

