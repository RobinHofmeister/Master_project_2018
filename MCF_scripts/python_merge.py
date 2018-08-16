import os
import subprocess



# create merged_liste
p1=subprocess.Popen('ls Mapping1/mapping_library*/output.gtf > mergelist.txt', shell= True)
p1.wait()
p2=subprocess.Popen('mv mergelist.txt Merged_assembly/', shell= True)
p2.wait()

# merged assembly:

assembly='nohup stringtie --merge -p 8 -G Annotations/gencode.v28.chr_patch_hapl_scaff.annotation.gtf -o Merged_assembly/stringtie_merged.gtf Merged_assembly/mergelist.txt'
p3=subprocess.Popen(assembly, shell= True)
p3.wait()

# library1_merged:

os.makedirs('Merged_assembly/merged_library1')
merged_library1='nohup stringtie -e --fr Mapping1/mapping_library1/mapped_library1_modified_CHR.output.bam -l merge_library1 -p 8 -G Merged_assembly/stringtie_merged.gtf -o Merged_assembly/merged_library1/output.gtf -A Merged_assembly/merged_library1/output.gene_abundance.tsv -B -C Merged_assembly/merged_library1/output.cov_ref.gtf > Merged_assembly/merged_library1/stringtie.log'
p4=subprocess.Popen(merged_library1, shell= True)
# library2_merged:

os.makedirs('Merged_assembly/merged_library2')
merged_library2='nohup stringtie -e --fr Mapping1/mapping_library2/mapped_library2_modified_CHR.output.bam -l merge_library2 -p 8 -G Merged_assembly/stringtie_merged.gtf -o Merged_assembly/merged_library2/output.gtf -A Merged_assembly/merged_library2/output.gene_abundance.tsv -B -C Merged_assembly/merged_library2/output.cov_ref.gtf > Merged_assembly/merged_library2/stringtie.log'
p5=subprocess.Popen(merged_library2, shell= True)



# Find lincRNAs:
os.makedirs('Bed_intersect')
## a) Select transcripts that do not intercept with extended coordinates:
## a1) download genome file
p6=subprocess.Popen('wget http://hgdownload.cse.ucsc.edu/goldenPath/hg38/bigZips/hg38.chrom.sizes', shell= True)
p6.wait()
subprocess.Popen('mv hg38.chrom.sizes Annotations/', shell = True )
##a2) select gencode PCGs
p7=subprocess.Popen('python Python_scripts_final/select_gencode_proteincoding.py', shell= True) #outputs: gencode_proteincoding_genes_only.gtf
p7.wait()
p8=subprocess.Popen('nohup bedtools slop -i gencode_proteincoding_genes_only.gtf -g Annotations/hg38.chrom.sizes -b 1000 > Annotations/gencode_proteincoding_genes_only_ext1000.gtf' , shell= True)
p8.wait()
## a3) select intergenic transcripts:
p9= subprocess.Popen('nohup bedtools intersect -a Merged_assembly/stringtie_merged.gtf -b Annotations/gencode_proteincoding_genes_only_ext1000.gtf -v > Bed_intersect/intergenic_transcripts.gtf', shell= True)
p9.wait()
## a4) select those longer than 200bp:
p10=subprocess.Popen('python Python_scripts_final/filter_200bp.py', shell= True)
p10.wait() #outputs: transcripts_intergenic_longer200.gtf

## a5) select those without proteincoding potential:
os.makedirs('CPC2')
p11=subprocess.Popen('split -l 40000 transcripts_intergenic_longer200.gtf', shell= True)
p11.wait()
p12=subprocess.Popen('mv xa* CPC2/', shell= True)
p12.wait()
# 		run CPC3 on xaa, xab, xac files.
# 		outputs 3 results files, stored in directory CPC2/

