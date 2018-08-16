file_intergenic=open('intergenic_chromHMM_sorted.bed')
outfile_promoters=open('intergenic_promoters.bed','w')
outfile_enhancer=open('intergenic_enhancers.bed','w')
for line in file_intergenic:
    tmp=line.split()
    if 'Enhancer' in tmp[3]:
        outfile_enhancer.write(line)
    elif 'Promoter' in tmp[3]:
        outfile_promoters.write(line)
outfile_promoters.close()
outfile_enhancer.close()
file_intergenic.close()
