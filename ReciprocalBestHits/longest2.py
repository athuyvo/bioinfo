#!/bin/env python



import re
import argparse

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", required=True, type=str, help= "input filename")
   # parser.add_argument("-t", "--table", required=True, type=str, help= "input data table")
    parser.add_argument("-o", "--output", required=True, type=str, help= "out filename")

    return(parser.parse_args())

args = get_args()
filename = args.filename
output = args.output
# table = args.table


# # create a dictionary to store Protein IDs and associated Gene IDs and gene names.

# protein_dict = {} # stores Protein ID as key and associated Gene ID and gene name as a list
# naming_list = [] # stores protein ID and gene name to append to dictionary 
# skipline = 1

# with open(table, "r") as hm_file: 
    
#     # parse through reference table with all gene ID, protein ID, and gene name

#     for line in hm_file: 
        
#         # skip header line
#         if (skipline == 1):
#             skipline =0
#             continue

#         newline = line.strip("\n")
#         newline =  newline.split("\t")
        
#         # print(newline)

#         proteinID = newline[1] # protein ID is in the second column of table
#         # print(proteinID)

#         # not all genes have a gene name
#         # not all genes have proteins 
#         # store gene ID, protein ID and gene name if there is a protein
#         if proteinID != "":
#             geneID = newline[0] # key in dictionary 

#             if proteinID not in protein_dict:
#                 geneName = newline[2] # gene name in 3rd column of table
                
#                 # don't add gene name if blank
#                 if geneName != "":
#                     protein_dict[proteinID] = [geneID, geneName]
#                 else:
#                     protein_dict[proteinID] = geneID
                


protein_dict = {} # stores protein ID and the longest protein length
protein_len = 0 # protein length
name_dict = {} # stores gene ID, it's longest protein ID, and gene name 
 

with open(filename, "r") as file:
   # name_list = [] # stores protein id and gene name to append to gene ID dictionary
    protein = ""
    genename = ""
    geneID = ""

    # parse through fasta file 
    for line in file: 
        newline = line.strip()

        # at header line
        if newline.startswith(">"): 
        
            # find gene ID in header line
            geneID =  re.findall(r'(?<=gene:)[A-Z,a-z,0-9]+', newline)
            geneID = geneID[0] # regex expression returns a list 
           
            # if gene doesn't have a name, set empty string
            try:
                genename = re.findall(r'(?<=gene_symbol:)[A-Z,a-z,0-9]+', newline)[0]
            except:
                genename = ""
            
            proteinID = re.findall(r'(?<=>)[A-Z,a-z,0-9]+', newline)
            proteinID = proteinID[0] # regex expression returns a list 
    
            protein = "" # reset protein length

        else: 
            protein += newline.strip("\n") # count protein sequences 
            
            # update dictionary to store each gene ID and its longest protein sequence 
            if geneID != "":
                if geneID in protein_dict:   
                    if len(protein) > len(protein_dict[geneID]):
                        protein_dict[geneID] = protein
                        name_dict[geneID] = [proteinID, genename]
                else: 
                    protein_dict[geneID] = protein
                    name_dict[geneID] = [proteinID, genename]

# write out fasta record for longest protein length for each gene
with open(output, "w") as file:
   
    # write header in format: Protein ID, Gene ID, Gene Name then fastsa record below
    for gene in protein_dict:
        proteinID = name_dict[gene][0]    
        genename = name_dict[gene][1]
        sequence = protein_dict[gene]
        file.write(">" + proteinID + " " + gene + " " + genename + "\n" + sequence + "\n")    

print(len(list(protein_dict.keys())))
print(len(list(name_dict.keys())))
