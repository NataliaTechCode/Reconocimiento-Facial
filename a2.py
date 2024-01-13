import cv2
import os
import pandas as pd
import conexion as db
import metodo as jesus

mycursor = db.mydb.cursor()
cont = 0
resultado = 0
Direccion = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
Usua = pd.read_csv(Direccion+'/Nombres.csv').columns
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
        
        if result[1] < 3000:
            cv2.putText(frame,'{}'.format(Usua[result[0]]),(x,y-25),2,1.1,(0,255,0),1,cv2.LINE_AA)
            cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)
            cont+=0
            resultado = result[0]
            jesus.dios(True)
            
        else:
            cv2.putText(frame,'Desconocido',(x,y-20),2,0.8,(0,0,255),1,cv2.LINE_AA)
            cv2.rectangle(frame, (x,y),(x+w,y+h),(0,0,255),2)
            
    cv2.imshow('frame',frame)
    k = cv2.waitKey(1)
    #if k == 27:
    if cont>0 or k == 27:
        break
print('label', Usua[resultado])

id=Usua[resultado]
sql = "INSERT INTO asistencia  (salon, usuario_id, fechahora) VALUES (%s,%s, NOW())"
val = ("C34",str(id)) # agregamos una coma después del valor para convertirlo en una tupla

mycursor.execute(sql, val)

db.mydb.commit()

print(mycursor.rowcount, "record inserted.")

cap.release()   
cv2.destroyAllWindows()