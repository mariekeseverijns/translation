#transpose.py takes one argument, the filename/path to a codon table text file. 
#It then prints each of of single-letter amino acid codes,
#together with the codons that encode for this amino acid. For example (codons are not correct):
#$ ./transpose.py codon_table.txt
#M ["ATG", "GGA", "CGA"]
#\A ["CCG", "TTT", "AAA"]

import sys

def build_codon_dic(codon_file):
    codon_amino_dic = {}
    with open(codon_file) as f:
        for line in f:
            split = line.split('\t')
            codon = split[0]
            amino = split[1]
            codon_amino_dic[codon] = amino
    return codon_amino_dic
if __name__ == "__main__":
    codon_file = sys.argv[1]
    codon_amino_dic = build_codon_dic(codon_file)
    print codon_amino_dic
