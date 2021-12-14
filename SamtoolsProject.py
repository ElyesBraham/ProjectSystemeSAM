#!/usr/bin/python3
#-*- coding : utf-8 -*-

import os
import sys
import re
import subprocess


#Analyse des reads : Utilisation de samtools

from subprocess import call 
# appel qui va exécuter un programme externe, ici samtools
              

def analyse() :
    for cmd in ("samtools view -S -b mapping.sam > mapping.bam", #SAM --> BAM (= + d'espace de stockage et + processing plus rapide)
                "samtools sort mapping.bam -o mapping.sorted.bam", #Trier et stocker BAM dans un autre fichier (tri par coordonnées d'alignement sur la ref)
                "samtools index mapping.sorted.bam", # indexage du fichier BAM "sorted"

                ################################ Total reads in SAM file 
                            
                #read mapped in proper pair : 0x2
                #read unmapped : 0x4
                #mate unmapped : 0x8
                #100M = Match pour 100 positions d'alignement (ceux qu'on va exclure)
                
                ################################ read non mappés extraits 

                "samtools view -f 0x4 mapping.sorted.bam > only_unmapped.fasta", 
                "samtools view -f 0x4 mapping.sorted.bam | echo 'Nombre de read non mappés:' $(wc -l) >> summary_file.txt ", # nombre de read non mappés mit dans un fichier txt

                ################################ read partiellement mappés extraits
                
                "samtools view -f 0x2  mapping.sorted.bam | grep -v '100M' > only_partially_mapped.fasta",
                "samtools view -f 0x2  mapping.sorted.bam | grep -v '100M' | echo 'Nombre de read partiellement mappés:' $(wc -l) >> summary_file.txt",

                ################################ paires de reads où un seul read de la paire est entièrement mappé et l'autre non mappé
                

                "samtools view  -f 0x4 -F 0x8 mapping.sorted.bam > read_unmapped_mate_mapped.fasta",
                "samtools view  -f 0x8 -F 0x4 mapping.sorted.bam > read_mapped__mate_unmapped.fasta",
        
                "samtools view  -f 0x4 -F 0x8 mapping.sorted.bam | echo 'Nombre de paires de read avec le read unmapped et le mate mapped:' $(wc -l) >> summary_file.txt",
                "samtools view  -f 0x8 -F 0x4 mapping.sorted.bam | echo 'Nombre de paires de read avec le read mapped et le mate unmapped:' $(wc -l) >> summary_file.txt",
                
                ################################ paires de reads où un seul read de la paire est entièrement mappé et l'autre partiellement mappé
                
                "samtools view -f 0x4 -F 0x8 mapping.sorted.bam | grep -v '100M' > read_mapped__mate_partially_mapped.fasta",
                "samtools view -F 0x4 -F 0x8 mapping.sorted.bam | grep -v '100M' > read_partially_mapped__mate_mapped.fasta",

                "samtools view -f 0x4 -F 0x8 mapping.sorted.bam | grep -v '100M' | echo 'Nombre de paires de read avec le read mapped et le mate partially mapped:' $(wc -l) >> summary_file.txt",
                "samtools view -F 0x4 -F 0x8 mapping.sorted.bam | grep -v '100M' | echo 'Nombre de paires de read avec le read partially mapped et le mate mapped:' $(wc -l) >> summary_file.txt",
                "samtools idxstats mapping.sorted.bam >> summary_file.txt", #résumé statistique des alignements (mappés et non mappés)
                "rm mapping.sorted.bam mapping.sorted.bam.bai mapping.bam"): #enlever les fichiers inutiles
                call(cmd, shell=True) 




def main() : 
    analyse()



main()

    
    


