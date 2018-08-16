import os
import subprocess


mapping_directory='mapp_SRRxxx'
map_dir_path='/scratch/local/weekly/rhofmeis_sra/mapp_SRRxxx'


if os.path.exists('scratch/local/weekly/rhofmeis_sra/mapp_SRRxxx') :
	subprocess.Popen('rm -r scratch/local/weekly/rhofmeis_sra/mapp_SRRxxx', shell=True) # supress if already created, can include a bugg..

subprocess.Popen('mkdir -p /scratch/local/weekly/rhofmeis_sra/mapp_SRRxxx', shell=True)



###-- Download SRA file:
p0=subprocess.Popen('nohup prefetch SRRxxx', shell=True)
p0.wait()

p00=subprocess.Popen('mv /scratch/beegfs/monthly/rhofmeis_sra/dbGaP-8031/sra/SRRxxx.sra /scratch/local/weekly/rhofmeis_sra/mapp_SRRxxx/', shell= True)
p00.wait()
p000=subprocess.Popen('mv /scratch/beegfs/monthly/rhofmeis_sra/dbGaP-8031/sra/SRRxxx.sra.vdbcache /scratch/local/weekly/rhofmeis_sra/mapp_SRRxxx/', shell= True)
p000.wait()

## Copy annotations files in the mapping directory:
p01=subprocess.Popen('cp -r /scratch/beegfs/monthly/rhofmeis_sra/dbGaP-8031/annotations '+map_dir_path, shell= True)
p01.wait()
p02=subprocess.Popen('tar xvzf '+map_dir_path+'/annotations/grch38_tran.tar.gz -C '+map_dir_path+'/annotations', shell= True)
p02.wait()
####-- conversion file.sra into file.fastq
fastq_dump='nohup fastq-dump --split-3 /scratch/local/weekly/rhofmeis_sra/mapp_SRRxxx/SRRxxx.sra -O '+map_dir_path

p1=subprocess.Popen(fastq_dump, shell=True)
p1.wait()      
sra_path='/scratch/local/weekly/rhofmeis_sra/mapp_SRRxxx/SRRxxx.sra'
os.remove(sra_path)
os.remove(sra_path+'.vdbcache')
    
#####----  trimming:
trimming='nohup trimmomatic PE -phred33 -threads 4 '+map_dir_path+'/SRRxxx_1.fastq '+map_dir_path+'/SRRxxx_2.fastq '+map_dir_path+'/sample_1.fastq '+map_dir_path+'/unpaired_sample_1.fastq '+map_dir_path+'/sample_2.fastq '+map_dir_path+'/unpaired_sample_2.fastq ILLUMINACLIP:/data/ul/dp/marques/jtan/TruSeq3-PE.fa:2:30:10 LEADING:15 TRAILING:15 SLIDINGWINDOW:4:15 MINLEN:36'

p2=subprocess.Popen(trimming, shell=True)
p2.wait()
os.remove(map_dir_path+'/SRRxxx_1.fastq')
os.remove(map_dir_path+'/SRRxxx_2.fastq')

####----- mapping:
mapping='nohup hisat2 -p 8 --dta --rg-id=SRRxxx --rg SM:SRRxxx --rg PL:ILLUMINA -x '+map_dir_path+'/annotations/grch38_tran/genome_tran -1 '+map_dir_path+'/sample_1.fastq -2 '+map_dir_path+'/sample_2.fastq -S '+map_dir_path+'/mapped_SRRxxx.output.sam > '+map_dir_path+'/sample.hisat.log'

p3=subprocess.Popen(mapping, shell=True)
p3.wait()
os.remove(map_dir_path+'/sample_1.fastq')
os.remove(map_dir_path+'/sample_2.fastq')
os.remove(map_dir_path+'/unpaired_sample_1.fastq')
os.remove(map_dir_path+'/unpaired_sample_2.fastq')


## Pipeline 1: Stringtie
#####---- conversion sam bam:
convert='nohup samtools sort -@ 8 -o '+map_dir_path+'/mapped_SRRxxx.output.bam '+map_dir_path+'/mapped_SRRxxx.output.sam'

p4=subprocess.Popen(convert, shell=True)
p4.wait()
os.remove(map_dir_path+'/mapped_SRRxxx.output.sam')

####--- add chr tag to bam file:
add_tag="nohup samtools view -H "+map_dir_path+"/mapped_SRRxxx.output.bam | sed -e 's/SN:1/SN:chr1/' | sed -e 's/SN:2/SN:chr2/' | sed -e 's/SN:3/SN:chr3/' | sed -e 's/SN:4/SN:chr4/' | sed -e 's/SN:5/SN:chr5/' | sed -e 's/SN:6/SN:chr6/' | sed -e 's/SN:7/SN:chr7/' | sed -e 's/SN:8/SN:chr8/' | sed -e 's/SN:9/SN:chr9/' | sed -e 's/SN:10/SN:chr10/' | sed -e 's/SN:11/SN:chr11/' | sed -e 's/SN:12/SN:chr12/' | sed -e 's/SN:13/SN:chr13/' | sed -e 's/SN:14/SN:chr14/' | sed -e 's/SN:15/SN:chr15/' | sed -e 's/SN:16/SN:chr16/' | sed -e 's/SN:17/SN:chr17/' | sed -e 's/SN:18/SN:chr18/' | sed -e 's/SN:19/SN:chr19/' | sed -e 's/SN:20/SN:chr20/' | sed -e 's/SN:21/SN:chr21/' | sed -e 's/SN:22/SN:chr22/' | sed -e 's/SN:X/SN:chrX/' | sed -e 's/SN:Y/SN:chrY/' | sed -e 's/SN:MT/SN:chrM/' | samtools reheader - "+map_dir_path+"/mapped_SRRxxx.output.bam > "+map_dir_path+"/mapped_SRRxxx_modified_CHR.output.bam"
p5=subprocess.Popen(add_tag, shell=True)
p5.wait()
os.remove(map_dir_path+'/mapped_SRRxxx.output.bam')


####--- bam file stats:
#bam_stats='nohup samtools flagstat '+map_dir_path+'/mapped_SRRxxx_modified_CHR.output.bam > '+map_dir_path+'/file.stats'

#p6=subprocess.Popen(bam_stats, shell=True)
#p6.wait()

####---- Stringtie:
stringtie='nohup stringtie --fr -e '+map_dir_path+'/mapped_SRRxxx_modified_CHR.output.bam -l Assembly_SRRxxx -p 8 -G '+map_dir_path+'/annotations/Final_gtf.gtf -o '+map_dir_path+'/output.gtf -A '+map_dir_path+'/output.gene_abundance.tsv -B -C '+map_dir_path+'/output.cov_ref.gtf > '+map_dir_path+'/stringtie.log'

p7=subprocess.Popen(stringtie, shell=True)
p7.wait()

os.remove(map_dir_path+'/e2t.ctab')
os.remove(map_dir_path+'/e_data.ctab')
os.remove(map_dir_path+'/i2t.ctab')
os.remove(map_dir_path+'/i_data.ctab')
os.remove(map_dir_path+'/t_data.ctab')
os.remove(map_dir_path+'/output.cov_ref.gtf')
os.remove(map_dir_path+'/mapped_SRRxxx_modified_CHR.output.bam')

## Built a file with transcripts fpkm values, that is the only file needed for the next:
file1=open(map_dir_path+'/output.gtf')
outfile_fpkm=open(map_dir_path+'/transcripts_fpkm.txt','w')
outfile_fpkm.write('transcript_id'+'\t'+'Fpkm'+'\t'+'Tpm'+'\n')
for line in file1:
    if line.find('#')==0:
        pass
    else:
        tmp=line.split()
        if tmp[2]=='transcript':
            t_id=tmp[11].strip(';').strip('"')
            if tmp[12]=='ref_gene_name':
                fpkm=tmp[17].strip(';').strip('"')
                tpm=tmp[19].strip(';').strip('"') 
            else:
                fpkm=tmp[15].strip(';').strip('"')
                tpm=tmp[17].strip(';').strip('"')
            newline=str(t_id)+'\t'+str(fpkm)+'\t'+str(tpm)+'\n'
            outfile_fpkm.write(newline)
outfile_fpkm.close()
file1.close()
os.remove(map_dir_path+'/output.gtf')
os.remove(map_dir_path+'/output.gene_abundance.tsv')



## copy files into scratch directory:
p8=subprocess.Popen('cp '+map_dir_path+'/transcripts_fpkm.txt /scratch/beegfs/monthly/rhofmeis_sra/dbGaP-8031/mapping/mapp_SRRxxx', shell= True)
p8.wait()



### Modify the file done.txt with the size of the output file.

subprocess.call('ls -l mapping/mapp_SRRxxx/* > liste_SRRxxx.txt', shell= True)
liste_file=open('liste_SRRxxx.txt')
size_SRRxxx=0
for line in liste_file:
	size_SRRxxx=line.split()[4]
liste_file.close()

file_done=open('done.txt')
outfile_done=open('done1.txt','w')
for line in file_done:
	if line.find('SRRxxx')==0:
		newline=line.replace('not_processed', str(size_SRRxxx))
		outfile_done.write(newline)
	else:
		outfile_done.write(line)
file_done.close()
outfile_done.close()

subprocess.call('rm liste_SRRxxx.txt', shell= True)
subprocess.call('rm done.txt', shell= True)
subprocess.call('mv done1.txt done.txt', shell= True)


### Pipeline 2: HTseq
#sam_sorted='nohup samtools sort -@ 8 -O sam -o '+map_dir_path+'/mapped_SRRxxx_sorted.sam '+map_dir_path+'/mapped_SRRxxx.output.sam'
#pp=sub.....
#os.remove(map_dir_path+'/mapped_SRRxxx.output.sam')

#htseq='nohup htseq-count --mode=intersection-strict --order=pos '+map_dir_path+'/mapped_SRRxxx_sorted.sam /scratch/beegfs/monthly/rhofmeis_ncbi/annotations/mcf7_expressed_transcripts.gtf > '+map_dir_path+'/gene_count_SRRxxx.txt'
#p8=subprocess.Popen(htseq, shell=True)
#p8.wait()    dont need to wait..
#print('-----')
#print(htseq)
