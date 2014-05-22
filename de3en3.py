todo = ["uno","dos","tes","cuatro","cinco","seis","siete","ocho"]

detresentres = [] # <-- el array contenedor tendra los grupos de 3 en 3 dentro
c = 0
print len(todo)

while c <= len(todo):
    grupo = [] # creando los subgrupos de 3 en 3
    try: # <-- puede dar error si no hay suficientes para completar otro grupo de tres
        for sg in range(3): # realizo 3 veces una accion
            grupo.append(todo[c]) # se va rellenando con el iterador externo de 3 en 3 tandas
            c = c +1 # al terminar las 3 tandas se sigue iterando otras 3 mas y asi
    except: # <-- si no hay suficientes no importa continuamos y salimos del while
        c = len(todo)+1
    detresentres.append(grupo) # agregando al grupo principal

print(detresentres)
