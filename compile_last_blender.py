#!/usr/bin/env python
import os.path
import subprocess
import platform
import apt

# instrucciones obtenidas de: https://wiki.blender.org/index.php/Dev:Doc/Building_Blender/Linux/Ubuntu/CMake
# probado en Ubuntu 16.04 xenial
version = "02"

blenderDir="blender"
#blenderDir = "BlenderMantaflow"
# entrando al home del usuario actual:
homeuser = os.environ['HOME']
os.chdir(homeuser)
# el directorio donde me gusta guardar los blenders:
lastBlendDir = ".lastblender"
#print os.getcwd()


if ( os.path.isdir(lastBlendDir) ):
    print("########## Entr in " + lastBlendDir + " ##########")
    os.chdir(lastBlendDir)
    #print os.getcwd()
    if ( os.path.isdir(blenderDir) != False ):
        print("########## Git clone... ##########")
        # si no existe el directorio blender es que nunca se compilo aqui
        if (lastBlendDir == "blender"):
            # blender:
            subprocess.call(["git", "clone", "https://git.blender.org/blender.git"], shell=False)
            # To clone the Blender sources with addons and translations included:
            #subprocess.call(["git", "clone", "git://git.blender.org/blender.git"], shell=False)
        elif (lastBlendDir == "BlenderMantaflow"):
            # mantaflow:
            #subprocess.call(["git", "clone", "https://github.com/sebbas/BlenderMantaflow.git"], shell=False)
            pass

        print("########## Entr in " + blenderDir + " ##########")
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

        if (lastBlendDir == "blender"):
            subprocess.call(["git", "submodule", "update", "--init", "--recursive"], shell=False)
            subprocess.call(["git", "submodule", "foreach", "git", "checkout", "master"], shell=False)
            subprocess.call(["git", "submodule", "foreach", "git", "pull", "--rebase", "origin", "master"], shell=False)
        elif (lastBlendDir == "BlenderMantaflow"):
            subprocess.call(["git", "submodule", "foreach", "git", "checkout", "master"], shell=False)
            subprocess.call(["git", "submodule", "foreach", "git", "pull", "--rebase", "origin", "master"], shell=False)

        print("########## Install dependencies with script install_deps.sh: ##########")
        print("########## This script works for Debian/Redhat/SuSE/Arch based distributions, both 32 and 64 bits. ##########")
        subprocess.call(["./build_files/build_environment/install_deps.sh"], shell=False)

        print("########## Compiling... ##########")
        subprocess.call("make", shell=False)

        exitMenu = False
        pwd = os.getcwd()
        while (exitMenu == False):
            existe = os.path.islink("/usr/local/bin/blender")  # si no hay link lo hacemos
            if existe:
                print "Symbolic link /usr/local/bin/blender exist -> " + os.readlink('/usr/local/bin/blender')
                entrada = raw_input("Upgrade this? (y/n): ")
                if entrada == "y" or entrada == "Y":
                    print "########## updating link... ########## "
                    print "########## for this action need root password: "
                    subprocess.call(["sudo", "ln", "-sf" , homeuser+"/"+lastBlendDir+"/"+"build_linux/bin/blender", "/usr/local/bin/blender"], shell=False)
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
                subprocess.call(["sudo", "ln", "-sf" , homeuser+"/"+lastBlendDir+"/"+"build_linux/bin/blender", "/usr/local/bin/blender"], shell=False)
                exitMenu = True
    else:
        print("########## Already compiled, now upgrade... ##########")
        os.chdir(blenderDir)
        subprocess.call(["git", "pull", "--rebase"], shell=False)
        subprocess.call(["git", "submodule", "foreach", "git", "pull", "--rebase", "origin", "master"], shell=False)
        subprocess.call(["make", "update"], shell=False)
        subprocess.call("make", shell=False)

print("Gracias por usar mi script version: "+version+", de auto-compilacion de blender!")
