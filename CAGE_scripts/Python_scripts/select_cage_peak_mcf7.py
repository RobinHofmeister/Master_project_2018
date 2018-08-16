file=open('hg19.cage_peak_phase1and2combined_tpm_ann.osc.txt')
outfile=open('Mcf7_cage_peak_tpm_ann.osc.txt','w')
for line in file:
    if line.find('chr')==0:
        tmp=line.split()
        tmp2=tmp[0].split(':')
        tmp3=tmp2[1].split('..')
        start=tmp3[0]
        tmp4=tmp3[1].split(',')
        end=tmp4[0]
        strand=tmp4[1]
        mcf7_chr=tmp2[0]
        mcf7_value=float(tmp[1299])
        name='*'
        if mcf7_value>0:
            newline=mcf7_chr+'\t'+start+'\t'+end+'\t'+name+'\t'+str(mcf7_value)+'\t'+strand+'\n'
            outfile.write(newline)
            
file.close()
outfile.close()

