#!/usr/bin/env python


# This script takes the genome assembly contig fasta files produced
# velvetg and measures the assembly accuracy. Outputs a table and 
# graph of the contig length distribution.

import argparse 
from matplotlib import pyplot as plt
import re


# set global variables 

def get_args():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-k", "--kmer", required=True, type=int, help="kmer size")
    parser.add_argument("-f", "--filename", required=False, type=str, help="input filename")
    parser.add_argument("-o", "--output", required=False, type=str, help="output filename")
    parser.add_argument("-g", "--graph", required=False, type=str, help="output graph filename")

    return(parser.parse_args())

args = get_args()
f = args.filename
output = args.output
graph = args.graph
kmer_size = args.kmer

with open(f, "r") as file:
    
    contig_count = 0 # number of contigs velvet outputted 
    max_contig_len = 0 # max contig found 
    gen_length = 0 # total length of genome assembly  
    contig_bucket = {} # dictionary containing distribution of contig lenth in groups of 100bps
    contig_list = [] # list of all contig length

    # variables used to find contig average 
    contig_cov_len = 0 # contig coverage multiplied by contig length
    sum_contig_cov_len = 0 # sum contig coverage that was multiplied by contig length 
    

    # read through each line in velvet fasta file 
    while True:
        line = file.readline().strip()
        if line == "":
            break
        # grab header line  
        if line.startswith(">") == True:
           
            contig_count += 1
           
           # grab contig length
            len_exp = re.search(r'(?<=_length_)\d+', line) # regex to find contig length
            klen = int(len_exp.group(0)) # contig length from contig fasta file

            # grab kmer coverage for contig 
            cov_exp = re.search(r'(?<=_cov_)\d.+', line) # regex to find kmer converage in contig fasta file
            #print(cov_exp.group(0))

            kcov = float(cov_exp.group(0)) # kmer coverage
            
            # find the actual physical contig length 
            # adjust length of contig = header + kmer size) -1
            # add contig length to list 
            contig_len = klen + kmer_size - 1
            contig_list.insert(0, contig_len)

            # bucket each contig length into groups of 100bps using floor division
            
            if (contig_len // 100) in contig_bucket:
                contig_bucket[contig_len // 100] += 1
            else: 
                contig_bucket[contig_len // 100] = 1
            
            # sum up contig lengths to find genome assembly length
            gen_length += contig_len

            # find max contig length
            if contig_len > max_contig_len: 
                max_contig_len = contig_len
            
            # Calculate the mean depth of coverage for each contig by multiplying
            # kmer coverage found in velvet output file with calculated contig len 
            # found in steps above. 
            # Then divide by contig len minus kmer length found in velvet output file plus 1.
            # Sum up each calculated contig length that's multplied by its length 
    
            contig_cov = (kcov * contig_len) / (contig_len - kmer_size+1)
            contig_cov_len = contig_cov * contig_len 
            sum_contig_cov_len += contig_cov_len

    # mean contig length using sum of contig length divided total number of contigs 
    mean_contig_len = gen_length/contig_len

# plot distribution of contigs in groups of 100bps

plt.bar(list(contig_bucket.keys()), list(contig_bucket.values()))
#plt.yscale("log")      
plt.title("Contig Distribution")     
plt.xlabel("Contig length")
plt.ylabel("Num of contigs")
#plt.ylim(0,30)
plt.savefig(graph)

with open(output, "w") as output_file: 
    output_file.write("Contig length\t" + "Number of contigs in this category\n")

    for keys in sorted(contig_bucket):
        output_file.write(str(keys) + "\t" + \
             str(contig_bucket[keys]) + "\n")

              
# calculate average contig coverage by taking sum of each contig coverage and divide by gene length
    
contig_avg = sum_contig_cov_len/gen_length

# calculate N50 
# reverse sort contig list then sum each length to find the first 
# contig length that is > N50 using half of the genome assembly length 

n50 = 0
sum_find_50 = 0
contig_list.sort(reverse=True)

for con in contig_list: 
    sum_find_50 += con
    if (sum_find_50 > gen_length/2):
        n50 = con
        break

print("Num of contigs", "Max contig len", "Mean contig len", "Genome len", "Mean dep cov for contigs", "N50", sep="\t", end ="\n")
print(contig_count, max_contig_len, mean_contig_len, gen_length, contig_avg, n50, sep="\t", end="\n")