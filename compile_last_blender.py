#!/usr/bin/env python
import os.path
import subprocess
import platform
import apt
import sys

# Based in: https://wiki.blender.org/index.php/Dev:Doc/Building_Blender/Linux/Ubuntu/CMake
# Tested in Ubuntu 16.04 xenial

# Usage:
# for compile blender:
# chmod +x myscript.py
# ./myscript.py
# And for compile Mantaflow build;
# chmod +x myscript.py
# ./myscript.py --mantaflow

version = "03"

#print(sys.argv[1])
arguments = sys.argv
#print(arguments)
if (len(arguments) > 1):
    if (arguments[1] == "--mantaflow"):
        print("\n\n########## Target to compile: Blender + Mantaflow ##########")
        blenderDir = "BlenderMantaflow"
    else:
        print("\n\n########## Target to compile: Blender ##########")
        blenderDir="blender"
else:
    print("\n\n########## Target to compile: Blender ##########")
    blenderDir="blender"

homeUser = os.environ['HOME']
os.chdir(homeUser)
lastBlendDir = ".lastblender"
#print os.getcwd()


def checkSymLink():
    exitMenu = False
    pwd = os.getcwd()
    while (exitMenu == False):
        if (blenderDir == "blender"):
            existe = os.path.islink("/usr/local/bin/blender")  # si no hay link lo hacemos
        if (blenderDir == "BlenderMantaflow"):
            existe = os.path.islink("/usr/local/bin/blenderMantaflow")  # si no hay link lo hacemos

        if existe:
            print("Previous Symbolic link exist!" )
            entrada = raw_input("Upgrade link (y/n): ")
            if entrada == "y" or entrada == "Y":
                print "########## updating link... ########## "
                print "########## for this action need root password: "

                if (blenderDir == "blender"):
                    subprocess.call(["sudo", "ln", "-sf" , homeUser+"/"+lastBlendDir+"/"+"build_linux/bin/blender", "/usr/local/bin/blender"], shell=False)
                    exitMenu = True

                if (blenderDir == "BlenderMantaflow"):
                    subprocess.call(["sudo", "ln", "-sf" , homeUser+"/"+lastBlendDir+"/"+mantaDir+"/"+"build_linux/bin/blender", "/usr/local/bin/blenderMantaflow"], shell=False)
                    exitMenu = True

            elif entrada == "n" or entrada == "N":
                print "########## keep link. ##########"
                exitMenu = True
            else:
                print "Only are avalidable this options:  y Y n N"
                exitMenu = False
        else:
            print "########## Making Symbolic link -> in to path ##########"
            print "########## for this action need root password: "

            if (blenderDir == "blender"):
                subprocess.call(["sudo", "ln", "-sf" , homeUser+"/"+lastBlendDir+"/"+"build_linux/bin/blender", "/usr/local/bin/blender"], shell=False)
                exitMenu = True

            if (blenderDir == "BlenderMantaflow"):
                subprocess.call(["sudo", "ln", "-sf" , homeUser+"/"+lastBlendDir+"/"+mantaDir+"/"+"build_linux/bin/blender", "/usr/local/bin/blenderMantaflow"], shell=False)
                exitMenu = True

if ( os.path.isdir(lastBlendDir) ):
    print("########## Enter in " + lastBlendDir + " ##########")
    os.chdir(lastBlendDir)

    if (blenderDir == "BlenderMantaflow"):
        mantaDir = 'MantaflowBuild'
        if not os.path.exists(mantaDir):
            os.makedirs(mantaDir)
            print("########## Enter in " + mantaDir + " ##########")
            os.chdir(mantaDir)
        else:
            os.chdir(mantaDir)

    #print os.getcwd()
    if ( os.path.isdir(blenderDir) == False ):
        print("########## Git clone... ##########")
        # si no existe el directorio blender es que nunca se compilo aqui
        if (blenderDir == "blender"):
            subprocess.call(["git", "clone", "https://git.blender.org/blender.git"], shell=False)
            # To clone the Blender sources with addons and translations included:
            #subprocess.call(["git", "clone", "git://git.blender.org/blender.git"], shell=False)
        elif (blenderDir == "BlenderMantaflow"): # mantaflow:
            subprocess.call(["git", "clone", "https://github.com/sebbas/BlenderMantaflow.git"], shell=False)

        print("########## Enter in " + blenderDir + " ##########")
        os.chdir(blenderDir)
        #print os.getcwd()

        print("########## Get all... ##########")
        # detectando la distro:
        if ( platform.linux_distribution()[0] == "Ubuntu" or  platform.linux_distribution()[0] == "Debian"):
            print("########## your distro is Debian based. ##########")
            print("########## Now installing some dependencies ##########")
            cache = apt.Cache()
            if (cache['git'].is_installed == False) or (cache['build-essential'].is_installed == False) or (cache['cmake'].is_installed == False) or (cache['cmake-curses-gui'].is_installed == False):
                print("########## You need any dependence ##########")
                print("########## installing:")
                subprocess.call(["sudo", "apt-get", "update"], shell=False)
                subprocess.call(["sudo", "apt-get", "install", "git", "build-essential", "cmake", "cmake-curses-gui"], shell=False)
            else:
                print("########## All dependeces are ok ##########")

        if (blenderDir == "blender"):
            subprocess.call(["git", "submodule", "update", "--init", "--recursive"], shell=False)
            subprocess.call(["git", "submodule", "foreach", "git", "checkout", "master"], shell=False)
            subprocess.call(["git", "submodule", "foreach", "git", "pull", "--rebase", "origin", "master"], shell=False)
        elif (blenderDir == "BlenderMantaflow"): # mantaflow:
            subprocess.call(["git", "submodule", "foreach", "git", "checkout", "master"], shell=False)
            subprocess.call(["git", "submodule", "foreach", "git", "pull", "--rebase", "origin", "master"], shell=False)

        print("########## Install dependencies with script install_deps.sh: ##########")
        print("########## This script works for Debian/Redhat/SuSE/Arch based distributions, both 32 and 64 bits. ##########")
        subprocess.call(["./build_files/build_environment/install_deps.sh"], shell=False)

        print("########## Compiling... ##########")
        subprocess.call("make", shell=False)

        checkSymLink()

    else:
        print("########## Previously compiled here, now upgrade... ##########")
        os.chdir(blenderDir)
        subprocess.call(["git", "pull", "--rebase"], shell=False)
        subprocess.call(["git", "submodule", "foreach", "git", "pull", "--rebase", "origin", "master"], shell=False)
        subprocess.call(["make", "update"], shell=False)
        subprocess.call("make", shell=False)
        checkSymLink()

print("Thanks for use my script version: "+version)
