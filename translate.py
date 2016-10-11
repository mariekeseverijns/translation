#translate.py takes at least two arguments.
#The first is again a codon table filename.
#The second is either the input DNA/RNA sequence directly or a filename of an input sequence to read.
#You are free to implement whichever of these two options you find most convenient.
#translate.py is supposed (on standard output or to a file) to print the sequence of
#amino acids encoded by the input DNA/RNA (according to the codon table).
#If you are translating for multiple reading frames then it would be convenient if you
#print the specifics about the reading frame, for example like this:

#$ ./translate.py codon_table.txt input_sequence.txt
#....
#Reading frame, offset +2:
#MAAC*
#....
#Reading frame, offset +1, reverse complement
#MTRAI*
import sys
import transpose

def input_seq(input_form, input):
    seq = ""
    if input_form == "seq": 		#input string
        seq = input
    elif input_form == "file": 		#input file
        file = open(input, "r").read().splitlines()
        seq = "".join(file)
    else:
        raise ValueError
    return seq.upper()

def output_choice(choice):		# Choice of output in file or in terminal
    if choice == "file":
        file = True
    elif choice == "print":
        file = False
    else:
        raise ValueError
    return file

def first_check(first, amino_acid):	# Check if startcodon has been found
    if amino_acid == "M":
        first = False
    return first

def sequence_check(sequence):		# Check, if U char in sequence, change to A
    for char in sequence:
        for char2 in sequence:
            if char =="A" and char2 == "U" or char =="U" and char2 == "A":
                return sequence.replace("U", "A")
    return sequence

def reverse_trans(sequence):
    return sequence[::-1]

def translate(codon_file, sequence, start, step):
    first = True			# If first == true, ATG has not yet been found
    aminoseq = ""
    if step == 3:
        print "Reading frame, offset +" + str(start) + ":"
    elif step == -3:
        print "Reading frame, offset +" + str(start) + ", reverse complement:"
        sequence = reverse_trans(sequence)	
    frame = sequence[start:]
    for i in range(2, len(frame), abs(step)):
        amino = codon_file[str(frame[i-2]+frame[i-1]+frame[i])]
        first = first_check(first, amino)
        if not first:
            aminoseq += amino
        if amino == "*":
            break
    if not aminoseq:			# Check if amino sequence is empty
        print aminoseq + "No startcodon. \n"
    elif aminoseq[-1] == "*":
        print aminoseq + "\n"
    else:
        print aminoseq + ", no stopcodon.\n"

def read(codon_file, sequence):
    for i in range(0, 3):
        translate(codon_file, sequence, i, 3)
        translate(codon_file, sequence, i, -3)

def main():
    if len(sys.argv) < 4:
        print "Program usage: python translate.py [codon file] [input form: 'seq' or 'file'] [input] [output form: 'file' or 'print'] \n i.e. python translate.py codon_table.txt seq ctgctttgatatgct print"
        return
    codon_file = sys.argv[1]
    codon_file = transpose.build_codon_dic(codon_file)
    sequence = input_seq(sys.argv[2], sys.argv[3])
    sequence = sequence_check(sequence)
    output_form = output_choice(sys.argv[4])
    if output_form:
        sys.stdout = open("output_translate_script.txt", "a")
        read(codon_file, sequence)
        sys.stdout.close()
    else:
        read(codon_file, sequence)
    print "translation finished"

if __name__ == "__main__":
    main()
