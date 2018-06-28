fout = open('result.txt', 'w')

with open('pyFlexsea.py', 'r') as f:
	for line in f:
		l = line.strip()
		if(l != ''):
			if(l[0] == '#'):
				fout.write(line)
			elif(l[:3] == 'def'):
				fout.write(line + '\n')