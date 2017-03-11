# Librairies
import os
import subprocess
import sys
import re

# Config here
COMPRESS_FOLDER_NAME = "out"
EXCLUDE_EXT = ['.txt', '.lua', '.bz2', '.zip', '.MD', '.md']

CWD = os.getcwd()
COMPRESS_FOLDER_PATH = CWD + "\\" + COMPRESS_FOLDER_NAME + "\\"
BASE_FOLDER = ""

def can_be_compressed(filepath):
    """ Retourne True si le fichier peut être compressé. """
    ext = os.path.splitext(filepath)[1]
    return not ext in EXCLUDE_EXT

def compress_bz2(filepath):
    """ Compresse le fichier passé en paramètre en archive bz2. """
    print(filepath + ".bz2")
    subprocess.run([r"C:\Program Files\7-Zip\7z.exe", "u", "-tbzip2", "-mx9",
                   filepath + ".bz2", filepath], stdout=subprocess.DEVNULL)

def compress_bz2_to(filepath, dest):
    """ Compresse le fichier passé en paramètre en archive bz2 dans le dossier spécifié. """
    subprocess.run([r"C:\Program Files\7-Zip\7z.exe", "u", "-tbzip2", "-mx9",
                   dest + os.path.basename(filepath) + ".bz2",
                   filepath])

def compress_folder(folderpath):
    """ Compresse l'ensemble des fichiers présents dans le
    dossier passé en paramètre. """

    if os.path.basename(folderpath) == "lua":
        return

    relpath = os.path.relpath(folderpath)
    outfolder =  re.sub(BASE_FOLDER, COMPRESS_FOLDER_NAME, relpath, 1)

    if not os.path.exists(outfolder):
        os.mkdir(CWD + "\\" + outfolder)
    
    # Parcours des fichiers dans le répertoire de base
    with os.scandir(folderpath) as it:
        for entry in it:
            if entry.is_file():
                if can_be_compressed(entry.path):
                    compress_bz2_to(entry.path, outfolder + "\\")
            else:              
                compress_folder(entry.path)

def main():
    global BASE_FOLDER
    # 2 arguments obligatoires
    if len(sys.argv) != 2:
        print("Usage:\n")
        print("\tpython bzip.py <file>\n")
        sys.exit("Invalid arguments")

    # On récupère le fichier drag & drop
    arg_folder = sys.argv[1]
    BASE_FOLDER = os.path.relpath(arg_folder)

    # Un seul fichier, on le compresse directement.
    if os.path.isfile(arg_folder):
        compress_bz2(arg_folder)
    elif os.path.isdir(arg_folder):
        # Il faut parcourir récursivement le dossier, tout en
        # reconstruisant la hiérarchie des dossiers dans le dossier final.        
        compress_folder(arg_folder)
    else:
        print("Invalid argument !")

    os.system("pause")

if __name__ == "__main__":
    main()
