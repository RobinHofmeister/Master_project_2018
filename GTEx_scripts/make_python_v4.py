
import os
import subprocess

## List all SRA
p=subprocess.Popen('prefetch -l cart_224_sra.krt > srr_liste.txt', shell=True)
p.wait()


## create file to store all the processed SRA:
file=open('srr_liste.txt')
outfile=open('done.txt','w')
for line in file:
    if line.find('8031')==0:
        tmp=line.split('|')
        newline=tmp[2]+'\t'+'not_processed'+'\n'
        outfile.write(newline)
file.close()
outfile.close()




##### directory local

### directory beegfs, where will be copied the final files:
os.makedirs('/scratch/beegfs/monthly/rhofmeis_sra/dbGaP-8031/mapping')

####

liste=open('srr_liste.txt')
for i in liste:
	if i.find('8031')==0:
		tmp=i.split('|')
		srr=tmp[2]

       
        	mapping_directory='mapp_'+str(srr)
		
		if os.path.exists('/scratch/beegfs/monthly/rhofmeis_sra/dbGaP-8031/mapping/'+str(mapping_directory)) :
			subprocess.call('rm -r /scratch/beegfs/monthly/rhofmeis_sra/dbGaP-8031/mapping/'+str(mapping_directory))

		os.makedirs('/scratch/beegfs/monthly/rhofmeis_sra/dbGaP-8031/mapping/'+str(mapping_directory)) # where to copy final files with fpkm values
				

        	script_name='python_'+srr+'.py'
        	outfile=open(script_name,'w')
        	script=open('python_script_empty_v4.py')
        	for line in script:
                	if 'SRRxxx' in line:
                        	outfile.write(line.replace('SRRxxx',srr))

                	else:
                        	outfile.write(line)

        	outfile.close()
        	bash_script_name='bash_'+srr+'.sh'
        	outfile2=open(bash_script_name,'w')
        	bash_script=open('bash_script_empty_v4.sh')
        	for line in bash_script:
                	if 'SRRxxx' in line:
                        	outfile2.write(line.replace('SRRxxx',srr))
                	else:
                        	outfile2.write(line)
        	outfile2.close()

        	call_bash='bsub < '+bash_script_name
        	print(call_bash)
        	subprocess.call(call_bash, shell=True)


