import Entrenamiento as Ent
import conexion as db


peti = False
entre = False
Probar = ''
#informacion para la insercion

mycursor = db.mydb.cursor()


id_nombre =""



Nombre = input('Nombre de usuario: ')


while (True):
    annadir = input('Desea añadir usuario? ')
    if(annadir == 'Y' or annadir == 'y'):
        sql = "INSERT INTO usuario  (nombre) VALUES (%s)"
        val = (str(Nombre),) 
        mycursor.execute(sql, val)
        db.mydb.commit()
        print(mycursor.rowcount, "record inserted null")

        mycursor.execute("SELECT MAX(id) FROM usuario")

        myresult = mycursor.fetchall()

        print(str(myresult[0]))
        id_nombre =str(myresult[0][0])


        peti = Ent.pet(id_nombre)
        if (peti == True):
            print("Se guardaron las imagenes")
        else:
            print('Ha ocurrido un error. Programa finalizado')
            break
    else:
        break
if(peti == True):
    print('Dando comienzo a entenamiento...')
    entre = Ent.entrenamiento()



if (entre == True):
    Probar = input('Desea probar modelo? ')
if(Probar == 'Y' or Probar == 'y' and entre==True):
    Ent.Modelo()