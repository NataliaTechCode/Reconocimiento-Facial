import tkinter as tk
def dios(es_verde):
    def ocultar_todo():
        if es_verde:
            label_defecto.destroy()
            #btn_inicio.pack_forget()
            label_verificado.pack()
            root.configure(background='green')
            root.after(5000, cerrar_ventana)
        else:
            label_defecto.destroy()
            #btn_inicio.pack_forget()
            label_error.pack()
            root.configure(background='red')


    def cerrar_ventana():
        root.destroy()
    # Crear la ventana principal
    root = tk.Tk()
    root.geometry("600x600")

    # Marco por defecto
    marco_defecto = tk.Frame(root)

    # Etiqueta para el estado verificado
    label_verificado = tk.Label(marco_defecto, background='green',text='¡Verificado!', font=('Arial', 24), pady=200, fg='white')

    # Etiqueta para el estado de error
    label_error = tk.Label(marco_defecto, background='red',text='¡Error!', font=('Arial', 24), pady=200, fg='white')

    # Etiqueta por defecto
    label_defecto = tk.Label(marco_defecto, text='Esperando', font=('Arial', 24), pady=200)

    # Botón para comenzar la verificación
    #btn_inicio = tk.Button(marco_defecto, text='Comenzar', command=ocultar_todo)

    # Empaquetar los elementos en el marco
    label_defecto.pack()
    #btn_inicio.pack()

    # Empaquetar el marco en la ventana principal
    marco_defecto.pack()

    # Variable para indicar si está verificado o no

    ocultar_todo()


    # Ejecutar el bucle principal de la aplicación
    root.mainloop()