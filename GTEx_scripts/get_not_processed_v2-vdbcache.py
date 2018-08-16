import os
import subprocess

file=open('done.txt')
for line in file:
	tmp=line.split()
	if tmp[1]=='not_processed':
		srr=tmp[0] # get the SRR of non processed SRA
		

		script_name='python_'+srr+'.py'
		python_file=open(script_name)
		new_script_name='python_'+srr+'_v2.py'
		new_python_file=open(new_script_name,'w')
		for line in python_file:
			if 'vdbcache' in line:
				pass
			elif 'p000' in line:
				pass
			else:
				new_python_file.write(line)
		new_python_file.close()
		python_file.close()


		bash_script_name='bash_'+srr+'.sh'
        	
		bash_file=open(bash_script_name)
		new_bash_script_name='bash_'+srr+'_v2.sh'
		new_bash_file=open(new_bash_script_name,'w')
		
		for line in bash_file:
			if 'python' in line:
				new_bash_file.write(line.replace(srr,srr+'_v2'))
			else:
				new_bash_file.write(line)
		bash_file.close()
		new_bash_file.close()

			
		call_bash='bsub < '+new_bash_script_name
        	print(call_bash)
        	subprocess.call(call_bash, shell=True) # run the bash script of the non processed SRA
