import os
import subprocess

p=subprocess.Popen('ls mapping/mapp_SRR*/*.err > err_list.txt', shell=True)
p.wait()


d=dict()
file_err=open('err_list.txt')
for i in file_err:
	name_f=i.split('/')[2].split('.')[0]
	

	file=open(i.strip('\n'))
	for line in file:
			
		if 'overall alignment rate' in line:
			tmp=line.split()
				
			mapping_score=tmp[0]
		if 'Input Read Pairs:' in line:
			tmp=line.split()
			trimming_score=[str(tmp[7].strip('()'))+'/'+str(tmp[20].strip('()'))]
		
	d[name_f]=[mapping_score,trimming_score]
							
	file.close()
file_err.close()

#print(d)


file_done=open('done.txt')
outfile_done=open('done_v2.txt','w')
outfile_done.write('SRA \t file_size \t %mapping \t trimming:both surv/dropped \n')
for line in file_done:

        tmp=line.split()

        if tmp[0] in d.keys():
                percent_map=d[tmp[0]][0]
                percent_trim=d[tmp[0]][1]
                newline=tmp[0]+'\t'+tmp[1]+'\t'+str(percent_map)+'\t'+str(percent_trim)+'\n'
                #print(newline)
                outfile_done.write(newline)
outfile_done.close()
file_done.close()

