#!/usr/bin/env python
import os.path
import subprocess
import platform
import apt

# instrucciones obtenidas de: https://wiki.blender.org/index.php/Dev:Doc/Building_Blender/Linux/Ubuntu/CMake
# probado en Ubuntu 16.04 xenial
version = "01"

blenderDir="blender"
# entrando al home del usuario actual:
homeuser = os.environ['HOME']
os.chdir(homeuser)
# el directorio donde me gusta guardar los blenders:
lastBlendDir = ".lastblender"
#print os.getcwd()


if ( os.path.isdir(lastBlendDir) ):
    print("Entrando en " + lastBlendDir)
    os.chdir(lastBlendDir)
    #print os.getcwd()
    if ( os.path.isdir(blenderDir) == False ):
        print("haciendo git clone...")
        # si no existe el directorio blender es que nunca se compilo aqui
        # blender:
        subprocess.call(["git", "clone", "https://git.blender.org/blender.git"], shell=False)
        # To clone the Blender sources with addons and translations included:
        #subprocess.call(["git", "clone", "git://git.blender.org/blender.git"], shell=False)
        # mantaflow:
        #subprocess.call(["git", "clone", "https://github.com/sebbas/BlenderMantaflow.git"], shell=False)
        #blenderDir = "BlenderMantaflow"
        print("Entrando en " + blenderDir)
        os.chdir(blenderDir)
        #print os.getcwd()

        print("Obteniendo todo...")
        # detectando la distro:
        if ( platform.linux_distribution()[0] == "Ubuntu" or  platform.linux_distribution()[0] == "Debian"):
            print("Tu distro esta basada en Debian.")
            print("Procedere a instalar algunas dependencias en caso de no tenerlas instaladas")
            cache = apt.Cache()
            if (cache['git'].is_installed == False) or (cache['build-essential'].is_installed == False) or (cache['cmake'].is_installed == False) or (cache['cmake-curses-gui'].is_installed == False):
                print("Parece que te falta alguna dependencia.")
                print("Pocedemos a instalarla:")
                subprocess.call(["sudo", "apt-get", "update"], shell=False)
                subprocess.call(["sudo", "apt-get", "install", "git", "build-essential", "cmake", "cmake-curses-gui"], shell=False)
            else:
                print("Parece que ya las tienes instaladas...")

        subprocess.call(["git", "submodule", "update", "--init", "--recursive"], shell=False)
        subprocess.call(["git", "submodule", "foreach", "git", "checkout", "master"], shell=False)
        subprocess.call(["git", "submodule", "foreach", "git", "pull", "--rebase", "origin", "master"], shell=False)

        print("Instalando las dependencias con el script de la BF install_deps.sh:")
        print("This script works for Debian/Redhat/SuSE/Arch based distributions, both 32 and 64 bits.")
        subprocess.call(["./build_files/build_environment/install_deps.sh"], shell=False)

        print("Compilando...")
        subprocess.call("make", shell=False)

        exitMenu = False
        pwd = os.getcwd()
        while (exitMenu == False):
            existe = os.path.islink("/usr/local/bin/blender")  # si no hay link lo hacemos
            if existe:
                print "Actualmente ya existe el enlace simbolico /usr/local/bin/blender y esta apuntado a: " + os.readlink('/usr/local/bin/blender')
                entrada = raw_input("Desea mantenerlo o renovarlo? (r/m): ")
                if entrada == "r" or entrada == "R":
                    print "creando enlace al path..."
                    print "Para agregar blender al path es necesario el password de root: "
                    subprocess.call(["sudo", "ln", "-sf" , homeuser+"/"+lastBlendDir+"/"+"build_linux/bin/blender", "/usr/local/bin/blender"], shell=False)
                    exitMenu = True
                elif entrada == "m" or entrada == "M":
                    print "mantenido."
                    exitMenu = True
                else:
                    print "Solo son validas las siguientes opciones:  R r M m"
                    exitMenu = False
            else:
                print "creando enlace al path..."
                print "Para agregar blender al path es necesario el password de root: "
                subprocess.call(["sudo", "ln", "-sf" , homeuser+"/"+lastBlendDir+"/"+"build_linux/bin/blender", "/usr/local/bin/blender"], shell=False)
                exitMenu = True
    else:
        print("Posiblemente ya este compilado. Ahora lo actualizaremos...")
        os.chdir(blenderDir)
        subprocess.call(["git", "pull", "--rebase"], shell=False)
        subprocess.call(["git", "submodule", "foreach", "git", "pull", "--rebase", "origin", "master"], shell=False)
        subprocess.call(["make", "update"], shell=False)
        subprocess.call("make", shell=False)

print("Gracias por usar mi script version: "+version+", de auto-compilacion de blender!")
