Bonjour ! Voici une brève description de notre projet bioinformatique de l'UE Système HAI724I

__authors__ = ("Rayane AOMAR", "Elyes BRAHAM")
__contact__ = ("rayane.aomar@etu.umontpellier.fr","elyes.braham@etu.umontpellier.fr")
__version__ = "0.0.1"
__date__ = "12/14/2021"
__licence__ ="This program is free software: you can redistribute it and/or modify"
        under the terms of the GNU General Public License as published by
        the Free Software Foundation, either version 3 of the License, or
        (at your option) any later version.
        This program is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
        GNU General Public License for more details.
        You should have received a copy of the GNU General Public License
        along with this program. If not, see <https://www.gnu.org/licenses/>.

__description__ = 
"Ce projet en langage python a pour but d'analyser un fichier SAM,
en commencant par un check de la validité du fichier, 
puis une étape de parsing (lecture, stockage et parcours des données)
et affiche ensuite un résumé des informations  d'alignements des reads 
en fonction du FLAG et du CIGAR. 
Dans ce projet ont été extraits : les reads non_mappés, partiellement mappés, 
les  paires de reads où un seul read de la paire est entièrement mappé et l’autre non mappé, 
et les paires de reads où un seul read de la paire est entièrement mappé et
l’autre partiellement mappé.
La dernière étape est d'afficher le résumé des résultats obtenus, comme le nombre de reads et
paires de chaque catégorie."

__scriptDescription__ = 
"Le premier script SamReader.py permet de répondre aux attentes du projet avec inclus
du code qui nous a été donné. Ce script a un temps d'execution en moyenne de 10 min.
Le deuxième script SamToolsProject.py ne contient pas de fonction de parse, et avec un
temps d'execution de 5 secondes car utilise un programme externe, Samtools. Ce script a été
utilisé pour vérifier les résultats obtenus lors de l'exécution du 1er script.

__requirements__ = 
"Projet executé sur WSL (Windows Subsysteme for Linux) 
	on PowerShell sur Windows  : wsl --install -d <Distribution Name> 
Une distribution Linux est donc nécessaire pour executer ces 2 scripts
Lancer le terminal Ubuntu (version utilisée est 20.04) 

Version python : python3 
$ sudo apt update && upgrade
$ sudo apt install python3 python3-pip ipython3

Installation de Samtools :
$ sudo apt-get update -y
$ sudo apt-get install -y libncurses-dev libbz2-dev liblzma-dev   (ou -y samtools pour la dernière version)
$ cd XXX/       XXX= répertoire dans lequel on veut installer samtools 
$ wget https://github.com/samtools/samtools/releases/XXX/1.12/samtools-1.12.tar.bz2
$ tar xvjf samtools-1.12.tar.bz2
$ cd samtools-1.12/     (nouveau répertoire créer : samtools-1.12)
$ ./configure
$ make
$ sudo make install
$ export PATH="$PATH:/home/user/Downloads/samtools-1.12"
$ sudo gedit ~/.bashrc
$ export PATH="$PATH:/home/user/Downloads/samtools-1.12"    (ajouter cette ligne à la fin du fichier bashrc)
$ source ~/.bashrc

Find more here : http://samtools.sourceforge.net/
git clone git://github.com/samtools/samtools.git 

Pour lancer samtools, faire $ samtools sur le terminal ubuntu."

Installer subprocess
$ pip install subprocess.run



__download__ = "Les 2 scripts sont  à télécharger sur ce lien:"
https://github.com/ElyesBraham/ProjectSystemeSAM 


__instructions__ = 
$ python3 SamReader.py XXX.sam (fichier SAM à utiliser, ici XXX= mapping) ______ 1er script pour parser
$ python3 SamtoolsProject.py XXX.sam       _______ 2ème script utilisant Samtools 
!! Faites en sorte d'avoir toujours le fichier SAM à analyser dans le même répertoire que les 2 script !!

__output__ = 
"-Script SamReader.py : 4 fichiers 
only_unmapped.fasta 
only_partially_mapped.fasta
summary_partially_mapped.txt
summary_unmapped.txt"

"-Script SamtoolsProject.py : 7 fichiers 
only_unmapped.fasta
only_partially_mapped.fasta
read_mapped__mate_unmapped.fasta
read_unmapped_mate_mapped.fasta
read_mapped__mate_partially_mapped.fasta
read_partially_mapped__mate_mapped.fasta
summary_file.txt


