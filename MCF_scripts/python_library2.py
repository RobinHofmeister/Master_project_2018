import os
import subprocess

os.makedirs('Mapping1/mapping_library2')


#Download RNAseq:
download_read1='wget https://www.encodeproject.org/files/ENCFF000HQQ/@@download/ENCFF000HQQ.fastq.gz'
download_read2='wget https://www.encodeproject.org/files/ENCFF000HRH/@@download/ENCFF000HRH.fastq.gz'
p1=subprocess.Popen(download_read1, shell =True)
p1.wait()
p2=subprocess.Popen(download_read2, shell= True)
p2.wait()

subprocess.call('mv ENCFF000HQQ.fastq.gz Mapping1/mapping_library2/library2_1.fastq.gz', shell= True)
subprocess.call('mv ENCFF000HRH.fastq.gz Mapping1/mapping_library2/library2_2.fastq.gz', shell= True)

#quality control:
os.makedirs('Mapping1/mapping_library2/quality_control')
subprocess.call('nohup fastqc Mapping1/mapping_library2/library2_1.fastq.gz Mapping1/mapping_library2/library2_2.fastq.gz -o Mapping1/mapping_library2/quality_control', shell= True)

#trimming:
trimming='nohup trimmomatic PE -phred64 -threads 4 Mapping1/mapping_library2/library2_1.fastq.gz Mapping1/mapping_library2/library2_2.fastq.gz Mapping1/mapping_library2/trimmed_library2_1.fastq.gz Mapping1/mapping_library2/unpaired_trimmed_library2_1.fastq.gz Mapping1/mapping_library2/trimmed_library2_2.fastq.gz Mapping1/mapping_library2/unpaired_trimmed_library2_2.fastq.gz ILLUMINACLIP:/data/ul/dp/marques/jtan/TruSeq3-PE.fa:2:30:10 LEADING:15 TRAILING:15 SLIDINGWINDOW:4:15 MINLEN:36'
p3=subprocess.Popen(trimming, shell= True)
p3.wait()

os.makedirs('Mapping1/mapping_library2/quality_control_trimmed')
subprocess.call('nohup fastqc Mapping1/mapping_library2/trimmed_library2_1.fastq.gz Mapping1/mapping_library2/trimmed_library2_2.fastq.gz -o Mapping1/mapping_library2/quality_control_trimmed', shell= True)

#mapping:
#os.makedirs('Annotations')
#p4=subprocess.Popen('wget ftp://ftp.ccb.jhu.edu/pub/infphilo/hisat2/data/grch38_tran.tar.gz', shell= True)
#p4.wait()
#p5=subprocess.Popen('nohup tar xvzf grch38_tran.tar.gz', shell= True)
#p5.wait()
#subprocess.call('mv grch38_tran Annotations/', shell= True)

mapping='nohup hisat2 -p 8 --dta --rg-id=library2 --rg SM:library2 --rg PL:ILLUMINA -x Annotations/grch38_tran/genome_tran -1 Mapping1/mapping_library2/trimmed_library2_1.fastq.gz -2 Mapping1/mapping_library2/trimmed_library2_2.fastq.gz -S Mapping1/mapping_library2/mapped_library2.output.sam > Mapping1/mapping_library2/library2.hisat.log'
p6=subprocess.Popen(mapping, shell= True)
p6.wait()

sorting='nohup samtools sort -@ 8 -o Mapping1/mapping_library2/mapped_library2.output.bam Mapping1/mapping_library2/mapped_library2.output.sam'
p7=subprocess.Popen(sorting, shell= True)
p7.wait()

add_tag="nohup samtools view -H Mapping1/mapping_library2/mapped_library2.output.bam | sed -e 's/SN:1/SN:chr1/' | sed -e 's/SN:2/SN:chr2/' | sed -e 's/SN:3/SN:chr3/' | sed -e 's/SN:4/SN:chr4/' | sed -e 's/SN:5/SN:chr5/' | sed -e 's/SN:6/SN:chr6/' | sed -e 's/SN:7/SN:chr7/' | sed -e 's/SN:8/SN:chr8/' | sed -e 's/SN:9/SN:chr9/' | sed -e 's/SN:10/SN:chr10/' | sed -e 's/SN:11/SN:chr11/' | sed -e 's/SN:12/SN:chr12/' | sed -e 's/SN:13/SN:chr13/' | sed -e 's/SN:14/SN:chr14/' | sed -e 's/SN:15/SN:chr15/' | sed -e 's/SN:16/SN:chr16/' | sed -e 's/SN:17/SN:chr17/' | sed -e 's/SN:18/SN:chr18/' | sed -e 's/SN:19/SN:chr19/' | sed -e 's/SN:20/SN:chr20/' | sed -e 's/SN:21/SN:chr21/' | sed -e 's/SN:22/SN:chr22/' | sed -e 's/SN:X/SN:chrX/' | sed -e 's/SN:Y/SN:chrY/' | sed -e 's/SN:MT/SN:chrM/' | samtools reheader - Mapping1/mapping_library2/mapped_library2.output.bam > Mapping1/mapping_library2/mapped_library2_modified_CHR.output.bam"
p8=subprocess.Popen(add_tag, shell= True)
p8.wait()

#assembly

#p9=subprocess.Popen('wget ftp://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_28/gencode.v28.chr_patch_hapl_scaff.annotation.gtf.gz', shell= True)
#p9.wait()
#p10=subprocess.popen('gunzip gencode.v28.chr_patch_hapl_scaff.annotation.gtf.gz', shell= True)
#p10.wait()
#subprocess.call('mv gencode.v28.chr_patch_hapl_scaff.annotation.gtf Annotations/', shell= True)

assembly='nohup stringtie --fr Mapping1/mapping_library2/mapped_library2_modified_CHR.output.bam -l Assembly_library2 -p 8 -G Annotations/gencode.v28.chr_patch_hapl_scaff.annotation.gtf -o Mapping1/mapping_library2/output.gtf -A Mapping1/mapping_library2/output.gene_abundance.tsv -B -C Mapping1/mapping_library2/output.cov_ref.gtf > Mapping1/mapping_library2/stringtie.log'
p11=subprocess.Popen(assembly, shell= True)
p11.wait()

