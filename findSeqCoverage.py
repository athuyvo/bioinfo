#!/bin/env python

import argparse
import bioinfo

def get_args():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-f", "--filename", required=True, type=str, help="input fastq file")
    parser.add_argument("r", "--reads", required=True, type=str, help="number of sequencing reads") # fastq lines/4

    return(parser.parse_args())

args = get_args()
f = args.filename

with open(f, "r") as file: 
    line_count = 0
    num_nt = 0 # number of nucleotides
    total_nts = 0

    for line in file: 
        line = line.strip()
        line_count +=1
         
        if line_count % 4 == 2: # if at 2nd line in fastq record = sequence reads
            num_nt = len(line)

# for key in sorted(sum_kmer_dict):
#     print(key, sum_kmer_dict[key], sep="\t", end="\n")

# plt.bar(list(sum_kmer_dict.keys()), list(sum_kmer_dict.values()), width=1.0)
# plt.yscale("log")
# plt.xlim([0,10000])
# plt.title("Kmer Frequency")
# plt.xlabel("frequency")
# plt.ylabel("num of kmers")
# plt.show()