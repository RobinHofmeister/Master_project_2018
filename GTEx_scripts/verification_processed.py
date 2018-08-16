import subprocess

p=subprocess.Popen('ls mapping/mapp_SRR*/transcripts_fpkm.txt > map_list_transc_fpkm.txt', shell=True)
p.wait()

file=open('map_list_transc_fpkm.txt')
map_srr=[]
for i in file:
	#print(i.split('/')[1].split('_')[1])
	map_srr.append(i.split('/')[1].split('_')[1])
file.close()
file2=open('srr_liste.txt')
all_srr=[]
for line in file2:
	if '8031' in line:
		tmp=line.split('|')
		#print(tmp)
		all_srr.append(tmp[2])

file2.close()

outfile=open('not_mapped.txt','w')
for i in all_srr:
	#print(i)
	if i in map_srr:
		pass
	else:
		outfile.write(i+'\n+')

print('Done. If all SRA have been processed, file "not_mapped.txt" should be empty.')
