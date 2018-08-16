import os
import subprocess

file=open('done.txt')
for line in file:
	tmp=line.split()
	if tmp[1]=='not_processed':
		srr=tmp[0] # get the SRR of non processed SRA
		
		bash_script_name='bash_'+srr+'.sh'
        	call_bash='bsub < '+bash_script_name
        	print(call_bash)
        	subprocess.call(call_bash, shell=True) # run the bash script of the non processed SRA
