file=open('Bed_intersect/intergenic_transcripts.gtf')

size_transcripts=dict()
count_transcripts=0

for line in file:
    if line.find('chr')==0:
        tmp=line.split()
        if tmp[2]=='transcript':
            count_transcripts+=1
            transcript_id=tmp[11].strip(';').strip('"')
            size_transcript=0
        elif tmp[2]=='exon':
            exon_transcript_id=tmp[11].strip(';').strip('"')
            size_exon=int(tmp[4])-int(tmp[3])
            if exon_transcript_id==transcript_id:
                size_transcript+=size_exon
                size_transcripts[transcript_id]=size_transcript
file.close()

transcripts_longer_200=[]
transcripts_smaller=[]
for k,v in size_transcripts.items():
    if v>200:
        transcripts_longer_200.append(k)
    else:
        transcripts_smaller.append(k)
        
file2=open('Bed_intersect/intergenic_transcripts.gtf')
outfile=open('transcripts_intergenic_longer200.gtf','w')
for line in file2:
    if line.find('chr')==0:
        tmp=line.split()
        if tmp[2]=='transcript':
            count_transcripts+=1
            transcript_id=tmp[11].strip(';').strip('"')
            if transcript_id in transcripts_longer_200:
                outfile.write(line)
        elif tmp[2]=='exon':
            exon_transcript_id=tmp[11].strip(';').strip('"')
            if exon_transcript_id in transcripts_longer_200:
                outfile.write(line)
outfile.close()
file2.close()
