import os
import subprocess



## download CAGE reads replicates
p1=subprocess.Popen('wget http://fantom.gsc.riken.jp/5/datafiles/latest/basic/human.timecourse.hCAGE/MCF7%2520breast%2520cancer%2520cell%2520line%2520response%2520to%2520EGF1%252c%252000hr00min%252c%2520biol_rep2.CNhs12475.13097-140D1.hg19.nobarcode.bam', shell=True)
p1.wait()

p2=subprocess.Popen('wget http://fantom.gsc.riken.jp/5/datafiles/latest/basic/human.timecourse.hCAGE/MCF7%2520breast%2520cancer%2520cell%2520line%2520response%2520to%2520EGF1%252c%252000hr00min%252c%2520biol_rep3.CNhs12703.13163-141B4.hg19.nobarcode.bam', shell=True)
p2.wait()


p3=subprocess.Popen('bedtools bamtobed -i MCF7%20breast%20cancer%20cell%20line%20response%20to%20EGF1%2c%2000hr00min%2c%20biol_rep2.CNhs12475.13097-140D1.hg19.nobarcode.bam > cage_reads_hg19_rep1.bed',shell=True)
p3.wait()

p4=subprocess.Popen('bedtools bamtobed -i MCF7%20breast%20cancer%20cell%20line%20response%20to%20EGF1%2c%2000hr00min%2c%20biol_rep3.CNhs12703.13163-141B4.hg19.nobarcode.bam > cage_reads_hg19_rep2.bed',shell=True)
p4.wait()


p44=subprocess.Popen('wget http://fantom.gsc.riken.jp/5/datafiles/latest/basic/human.cell_line.hCAGE/breast%2520carcinoma%2520cell%2520line%253aMCF7.CNhs11943.10482-107A5.hg19.nobarcode.bam', shell=True)
p44.wait()
p444=subprocess.Popen('bedtools bamtobed -i breast%20carcinoma%20cell%20line%3aMCF7.CNhs11943.10482-107A5.hg19.nobarcode.bam > cage_reads_hg19_norep.bed',shell=True)
p444.wait()


## merge, convert and sort CAGE reads replicates
p5=subprocess.Popen('cat cage_reads_hg19_rep1.bed > cage_reads_hg19_rep1_rep2_rep3.bed', shell=True)
p5.wait()
p6=subprocess.Popen('cat cage_reads_hg19_rep2.bed >> cage_reads_hg19_rep1_rep2_rep3.bed', shell=True)
p6.wait()

p66=subprocess.Popen('cat cage_reads_hg19_norep.bed >> cage_reads_hg19_rep1_rep2_rep3.bed', shell=True)
p66.wait()

subprocess.check_call('bedtools sort -i cage_reads_hg19_rep1_rep2_rep3.bed > cage_reads_hg19_rep1_rep2_rep3_sorted.bed', shell=True)

p8=subprocess.Popen('liftOver -minMatch=0.2 -minBlocks=0.01 cage_reads_hg19_rep1_rep2_rep3_sorted.bed hg19ToHg38.over.chain cage_reads_hg38_rep1_rep2_rep3.bed cage_reads_hg38_rep1_rep2_rep3_unlifted.bed', shell=True)
p8.wait()
p9=subprocess.Popen('bedtools sort -i cage_reads_hg38_rep1_rep2_rep3.bed > cage_reads_hg38_rep1_rep2_rep3_sorted.bed', shell=True)
p9.wait()





# Get TSS

### Get 5' of each reads (TSS)
file=open('cage_reads_hg38_rep1_rep2_rep3_sorted.bed')
outfile=open('cage_reads_hg38_start_start.bed','w')
for line in file:
	tmp=line.split()
	
	strand=tmp[5]
	if strand=='-':	
		start=int(tmp[2])-1
		end=tmp[2]
		newline=tmp[0]+'\t'+str(start)+'\t'+str(end)+'\t'+tmp[3]+'\t'+tmp[4]+'\t'+tmp[5]+'\n'
		outfile.write(newline)
	else:
		start=int(tmp[1])
		end=start+1
	
		newline=tmp[0]+'\t'+str(start)+'\t'+str(end)+'\t'+tmp[3]+'\t'+tmp[4]+'\t'+tmp[5]+'\n'
		outfile.write(newline)
file.close()
outfile.close()




p10=subprocess.Popen('bedtools sort -i cage_reads_hg38_start_start.bed > cage_reads_hg38_start_start_sorted.bed', shell=True)
p10.wait()


### cluster reads with TSS away from 20bp
#	options -c, -o allow to select cluster with more than 2 reads
p11=subprocess.Popen('bedtools merge -i cage_reads_hg38_start_start_sorted.bed -s -d 20 -c 1,6 -o count,distinct > cage_clusters_20bp.bed', shell=True)
p11.wait()


## select cluster with 2 reads or more and modify output to reproduce a bed format
file2=open('cage_clusters_20bp.bed')
outfile2=open('cage_cluster_20bp_pairs.bed','w')
for line in file2:
	tmp=line.split()
	if int(tmp[4]) > 1 :
		
		outfile2.write(line)
file2.close()
outfile2.close()


p12=subprocess.Popen('bedtools sort -i cage_cluster_20bp_pairs.bed > cage_cluster_20bp_pairs_sorted.bed', shell=True)
p12.wait()

### cluster previous output (cluster_20bp) away from 400bp


p13=subprocess.Popen('bedtools merge -i cage_cluster_20bp_pairs_sorted.bed -s -d 400 -c 1,5,6 -o count,sum,distinct > cage_clusters_400bp.bed', shell=True)
p13.wait()

## select clusters with 5 reads or more 
file3=open('cage_clusters_400bp.bed')
outfile3=open('TSS_cage_cluster.bed','w')

for line in file3:
	tmp=line.split()
	nbr_reads=tmp[5]
	if int(nbr_reads)>4:
		newline=tmp[0]+'\t'+tmp[1]+'\t'+tmp[2]+'\t'+'*'+'\t'+tmp[5]+'\t'+tmp[6]+'\n'
		outfile3.write(newline)
file3.close()
outfile3.close()


