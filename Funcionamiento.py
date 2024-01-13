import cv2 #Recordar orden de Peticiones->Entrenamiento->Funcionamiento
import os
import imutils
from tqdm import tqdm
import shutil
def captura(direc, cant, plus): #donde cant es la cantidad de fotos y plus seran las añadidas
    if (plus!= 0):
        count = len([f for f in os.listdir(direc) if f.endswith(tuple('.jpg'))])
        canttotal = count + plus
        images = plus
    else:
        count = 0
        canttotal = cant
        images = cant
    if not os.path.exists(direc):
        os.makedirs(direc)
    cam = cv2.VideoCapture(0)
    faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
    if (cam.isOpened() == False):
        print('La camara no se pudo usar')
        if(count == 0):
            shutil.rmtree(direc)
        return (False)
    else:
        print('Camara iniciada')
        print('iniciando captura de rostro: ')
        barra = tqdm(total=images)
    while count<canttotal:
        ret, frame = cam.read()
        if ret == False: break
        frame =  imutils.resize(frame, width=640)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        auxFrame = frame.copy()

        faces = faceClassif.detectMultiScale(gray,1.3,5)

        for (x,y,w,h) in faces:
            cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)
            rostro = auxFrame[y:y+h,x:x+w]
            rostro = cv2.resize(rostro,(150,150),interpolation=cv2.INTER_CUBIC)
            cv2.imwrite(direc + '/rostro_{}.jpg'.format(count),rostro)
            count = count+1
            barra.update(1)
    tqdm(total=cant).close()
    return (True)



        
