#!/usr/bin/python3
#-*- coding : utf-8 -*-


import os
import sys
import re


def parse() :  
    if len(sys.argv) == 2 :    #Tester le bon nombre de paramètre (processing d'un fichier à la fois)
        print("Bonjour, \n Début du check du fichier " + sys.argv[1])
        print("Nom du script: \t"  + sys.argv[0])
        print("Nom du fichier à analyser: \t"+ sys.argv[1])

    ####################################################### Check
  
    #L'argument 1 doit être un fichier existant

    extension = os.path.splitext(sys.argv[1])
    
    if os.path.exists(sys.argv[1]):
        print ("Le fichier existe.")
    else : 
        print("Erreur : Le fichier n'existe pas .")
        exit()
            
    if os.path.isfile(sys.argv[1]):
        print ("Il s'agit bien d'un fichier.")
    else:
        print ("Erreur : Il ne s'agit pas d'un fichier.")
        exit()

    # Vérifier que le fichier n'est pas vide

    if os.stat(sys.argv[1]).st_size!=0: 
        print(extension) 
    else:
        print("Erreur : le fichier est vide")
        exit()  
    
    # Vérifier qu'il s'agisse d'un fichier avec la bonne extension

    if (extension[1] == ".sam"):
        print("C'est un fichier SAM")
    else:
        if (extension[1] == "") :
            print("Erreur : Pas d'extension")
        else:
            print("Erreur : Mauvaise extension")
        exit()


 ####################################################### 
 # Lecture du fichier et stockage des sections dans des listes
    
    header =[]
    flag = []
    cigar = []
    splitLines = []
    file = open(sys.argv[1],"r")
    contenu = file.readline()
    readline = 0 
    while line in contenu:
                if line.startswith("@"):
                    header.append(line)
                    print("Header : ", header)
                else:                                                       
                    if len(header) == 0: # verifier que la section header existe
                        print("Erreur : pas de header présent")
                        exit()
                    else :
                        unmapped(line)
                        partiallyMapped(line)
                        splitLines = line.split("\t")
                        flag.append(splitLines[1]) 
                        cigar.append(splitLines[5]) 
    print("FLAG : ")
    if len(flag)==0 : #vérifier que la liste FLAG existe 
            print("Erreur: pas de FLAG")
    else :
            print(flag)  

    for file in flag:
            print("BAM FLAG : ", flagBinary(flag))

    print("CIGAR:")
    if len(cigar)==0 : #vérifier que la liste CIGAR existe 
            print ("Erreur : pas de CIGAR")
    else :      
            print(cigar)
    for file in cigar :
            print("Cigar :", readCigar(cigar))

 ####################################################### Analyze 

#### Convert the flag into binary ####
def flagBinary(flag) : 

    flagB = bin(int(flag)) # Transform the integer into a binary.
    flagB = flagB[2:] # Remove '0b' Example: '0b1001101' > '1001101'
    flagB = list(flagB) 
    if len(flagB) < 12: # Size adjustement to 12 (maximal flag size)
        add = 12 - len(flagB) # We compute the difference between the maximal flag size (12) and the length of the binary flag.
        for t in range(add): 
            flagB.insert(0,'0') # We insert 0 to complete until the maximal flag size.
    return flagB



#### Analyze the unmapped reads (not paired) ####
                
def unmapped(line): 
    
    unmapped_count = 0
    with open ("only_unmapped.fasta", "a+") as unmapped_fasta, open("summary_unmapped.txt", "w") as summary_file:
        col_line = line.split("\t")
        print(col_line)
        flag = flagBinary(col_line[1])

        if int(flag[-3]) == 1:
            unmapped_count += 1
            unmapped_fasta.write(line)

        summary_file.write("Total unmapped reads: " + str(unmapped_count) + "\n") 
    return unmapped_count

#### Analyze the partially mapped reads ####

def partiallyMapped(line): 
    
    partially_mapped_count = 0

    with open ("only_partially_mapped.fasta", "a+") as partillay_mapped_fasta, open("summary_partially_mapped.txt", "w") as summary_file:
        col_line = line.split("\t")
        flag = flagBinary(col_line[1]) # We compute the same 

        if int(flag[-2]) == 1: 
            if col_line[5] != "100M":
                partially_mapped_count += 1
                partillay_mapped_fasta.write(line)

        summary_file.write("Total partially mapped reads: " + str(partially_mapped_count) + "\n") 
    return partially_mapped_count



### Analyse the CIGAR = regular expression that summarise each read alignment ###
def readCigar(cigar): 
   
    ext = re.findall('\w',cigar) # split cigar 
    key=[] 
    value=[]    
    val=""

    for i in range(0,len(ext)): # For each numeric values or alpha numeric
        if (ext[i] == 'M' or ext[i] == 'I' or ext[i] == 'D' or ext[i] == 'S' or ext[i] == 'H' or ext[i] == "N" or ext[i] == 'P'or ext[i] == 'X'or ext[i] == '=') :
            key.append(ext[i])
            value.append(val)
            val = ""
        else :
            val = "" + val + ext[i]  # Else concatenate in order of arrival
    
    dico = {}
    n = 0
    for k in key:   # Dictionnary contruction in range size lists              
        if k not in dico.keys():    # for each key, insert int value
            dico[k] = int(value[n])   # if key not exist, create and add value
            n += 1
        else:
            dico[k] += int(value[n])  # inf key exist add value
            n += 1
    return dico

### Analyse the CIGAR = regular expression that summarise each read alignment ###
def percentMutation(dico):
        
    totalValue = 0 # Total number of mutations
    for v in dico :
        totalValue += dico[v]

    mutList = ['M','I','D','S','H','N','P','X','=']
    res = ""
    for mut in mutList : # Calculated percent of mutation if mut present in the dictionnary, else, percent of mut = 0
        if mut in dico.keys() :
            res += (str(round((dico[mut] * 100) / totalValue, 2)) + ";")
        else :
            res += ("0.00" + ";")
    return res

def globalPercentCigar():
    """
      Global representation of cigar distribution.
    """
    
    with open ("outpuTable_cigar.txt","r") as outpuTable, open("Final_Cigar_table.txt", "w") as FinalCigar:
        nbReads, M, I, D, S, H, N, P, X, Egal = [0 for n in range(10)]

        for line in outpuTable :
            mutValues = line.split(";")
            nbReads += 2
            M += float(mutValues[2])+float(mutValues[12])
            I += float(mutValues[3])+float(mutValues[13])
            D += float(mutValues[4])+float(mutValues[14])
            S += float(mutValues[5])+float(mutValues[15])
            H += float(mutValues[6])+float(mutValues[16])
            N += float(mutValues[7])+float(mutValues[17])
            P += float(mutValues[8])+float(mutValues[18])
            X += float(mutValues[9])+float(mutValues[19])
            Egal += float(mutValues[10])+float(mutValues[20])

        FinalCigar.write("Global cigar mutation observed :"+"\n"
                        +"Alignlent Match : "+str(round(M/nbReads,2))+"\n"
                        +"Insertion : "+str(round(I/nbReads,2))+"\n"
                        +"Deletion : "+str(round(D/nbReads,2))+"\n"
                        +"Skipped region : "+str(round(S/nbReads,2))+"\n"
                        +"Soft Clipping : "+str(round(H/nbReads,2))+"\n"
                        +"Hard Clipping : "+str(round(N/nbReads,2))+"\n"
                        +"Padding : "+str(round(P/nbReads,2))+"\n"
                        +"Sequence Match : "+str(round(Egal/nbReads,2))+"\n"
                        +"Sequence Mismatch : "+str(round(X/nbReads,2))+"\n")


#####################################################################################################


                    
    
    
def main() :  
    parse()

main()
