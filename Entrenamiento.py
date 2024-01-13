import cv2 #Recordar orden de Peticiones->Entrenamiento->Funcionamiento
import os
import Funcionamiento
import numpy as np
from tqdm import tqdm
import csv
a =[]
Direccion = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
def pet (Nombre):
    #Nombre = input('Nombre de usuario: ')

    DirecUsuario = Direccion + '/Usuarios/' + Nombre
    #print('la direccion es:' + DirecUsuario)
    if not os.path.exists(DirecUsuario):
        print('Carpeta Creada: ', DirecUsuario)
        os.makedirs(DirecUsuario)
        Peticion = Funcionamiento.captura(DirecUsuario, 450, 0)
    else:
        print('Usuario existente')
        YN = input('¿Añadir Imagenes? (Y/N): ')
        if(YN == 'Y' or YN == 'y'):
            Peticion = Funcionamiento.captura(DirecUsuario, 450, int(input('indique la cantidad de imagenes a añadir: ')))
        else:
            print('Saliendo...')
            Peticion=False
            #Añadir opciones de salida...
    return Peticion
def entrenamiento():
    DirecModelo = Direccion+'/'+'Modelo'
    if not os.path.exists(DirecModelo):
        os.makedirs(DirecModelo)
    DireccionUs = Direccion+'/Usuarios'
    ListaUs = os.listdir(DireccionUs)
    print('Lista de usuarios: ', ListaUs)
    a =ListaUs
    facesData = []
    labels = []
    label = 0
    print('Iniciando lectura de imagenes...')
    for  nameDir in ListaUs:
        DirecUsuario = DireccionUs+'/'+nameDir
        print(nameDir)
        barra = tqdm(total=len([f for f in os.listdir(DirecUsuario) if f.endswith(tuple('.jpg'))]))
        for filename in os.listdir(DirecUsuario):
            barra.update(1)
            labels.append(label)
            facesData.append(cv2.imread(DirecUsuario+'/'+filename,0))
        label = label + 1
        barra.close()
    face_recognizer = cv2.face.EigenFaceRecognizer_create()

    print("Entrenando...")
    face_recognizer.train(facesData, np.array(labels))

    face_recognizer.write(DirecModelo+'/modelo.xml')
    with open(Direccion+'/Nombres.csv', 'w') as N:
        Escritor = csv.writer(N)
        Escritor.writerow(ListaUs)
    print("Modelo almacenado...")
    return True
def Modelo():
    DirecUsuarios = Direccion+'/Usuarios'
    Usua = os.listdir(DirecUsuarios)
    print('Nombres: ', Usua)
    face_recognizer = cv2.face.EigenFaceRecognizer_create()
    face_recognizer.read(Direccion+'/Modelo/modelo.xml')
    faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)
    while True:
        ret,frame = cap.read()
        if ret == False: break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        auxFrame = gray.copy()

        faces = faceClassif.detectMultiScale(gray,1.3,5)

        for (x,y,w,h) in faces:
            rostro = auxFrame[y:y+h,x:x+w]
            rostro = cv2.resize(rostro,(150,150),interpolation= cv2.INTER_CUBIC)
            result = face_recognizer.predict(rostro)

            cv2.putText(frame,'{}'.format(result),(x,y-5),1,1.3,(255,255,0),1,cv2.LINE_AA)
            
            if result[1] < 3200:
                cv2.putText(frame,'{}'.format(Usua[result[0]]),(x,y-25),2,1.1,(0,255,0),1,cv2.LINE_AA)
                cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)
            else:
                cv2.putText(frame,'Desconocido',(x,y-20),2,0.8,(0,0,255),1,cv2.LINE_AA)
                cv2.rectangle(frame, (x,y),(x+w,y+h),(0,0,255),2)
        cv2.imshow('frame',frame)
        k = cv2.waitKey(1)
        if k == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
