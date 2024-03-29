# SKELETON ASSEMBLER WRITTEN BY JOHN RIEFFEL
# MODIFIED BY BOBBY HEADRICK, MARCH 2019

import sys

from helperfunctions import *

opcodeDict = {
        'add':'0000000',
        'and':'0000100',
        'or':'0001000',
        'sub':'0001100',
        'addi':'1000000',
        'andi':'1000100',
        'ori':'1001100',
        'lw':'1010000',
        'sw':'1100000',
        'j':'0000010',
        'beq':'0001101'}

def ConvertAssemblyToMachineCode(inline):
	'''given a string corresponding to a line of assembly,
	strip out all the comments, parse it, and convert it into
	a string of binary values'''

	outstring = ''

	if inline.find('#') != -1:
		inline = inline[0:inline.find('#')] #get rid of anything after a comment
	if inline != '':
		if inline.find(')') != -1:
			LorS = 1
		else:
			LorS = 0
		inline = inline.replace("("," ") #replaces all parenthesis with whitespace
		inline = inline.replace(")"," ")
		words = inline.split() #assuming syntax words are separated by space, not comma
		operation = words[0]
		operands = words[1:]
		outstring += opcodeDict[operation]
		if operation == 'j':
			outstring += int2bs(operands[0], 9)
			return outstring
		if operation == 'beq':
			temp = operands[0]
			operands[0] = operands[2]
			operands[2] = temp
		if LorS == 1:
			temp = operands[1]
			operands[1] = operands[2]
			operands[2] = temp
		for oprand in operands:
			#currently only handles R-type instructions
			if oprand[0] == '$':
				outstring += int2bs(oprand[1:],3)
			else:
				outstring += int2bs(oprand,3)
	return outstring


def AssemblyToHex(infilename,outfilename):
	'''given an ascii assembly file , read it in line by line and convert each line of assembly to machine code
	then save that machinecode to an outputfile'''
	outlines = []
	with open(infilename) as f:

		lines = [line.rstrip() for line in f.readlines()]  #get rid of \n whitespace at end of line
		#if you are a python ninja, use list comprehension. and replace the for loop below
		# with this expression
		#outlines = [ConvertAssemblyToMachineCode(curline) for curline in lines]
		# but, no judgement if you prefer explicit for loops
		for curline in lines:
			outstring = ConvertAssemblyToMachineCode(curline)
			if outstring != '':
				outlines.append(bs2hex(outstring))

	f.close()

	with open(outfilename,'w') as of:
		of.write("v2.0 raw\n")
		for outline in outlines:
			of.write(outline)
			of.write("\n")
	of.close()


if __name__ == "__main__":
	#in order to run this with command-line arguments
	# we need this if __name__ clause
	# and then we need to read in the subsequent arguments in a list.

	#### These two lines show you how to iterate through arguments ###
	#### You can remove them when writing your own assembler
	print 'Number of arguments:', len(sys.argv), 'arguments.'
	print 'Argument List:', str(sys.argv)

	## This is error checking to make sure the correct number of arguments were used
	## you'll have to change this if your assembler takes more or fewer args
	if (len(sys.argv) != 3):
		print('usage: python skeleton-assembler.py inputfile.asm outputfile.hex')
		exit(0)
	inputfile = sys.argv[1]
	outputfile = sys.argv[2]
	AssemblyToHex(inputfile,outputfile)
