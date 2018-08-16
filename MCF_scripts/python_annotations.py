import os
import subprocess



# Index for Hisat2:
p4=subprocess.Popen('wget ftp://ftp.ccb.jhu.edu/pub/infphilo/hisat2/data/grch38_tran.tar.gz', shell= True)
p4.wait()
p5=subprocess.Popen('tar xvzf grch38_tran.tar.gz', shell= True)
p5.wait()
p6=subprocess.Popen('mv grch38_tran Annotations/', shell= True)
p6.wait()



# gencode annotations for stringtie:
p9=subprocess.Popen('wget ftp://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_28/gencode.v28.chr_patch_hapl_scaff.annotation.gtf.gz', shell= True)
p9.wait()
p10=subprocess.Popen('gunzip gencode.v28.chr_patch_hapl_scaff.annotation.gtf.gz', shell= True)
p10.wait()
subprocess.Popen('mv gencode.v28.chr_patch_hapl_scaff.annotation.gtf Annotations/', shell= True)


