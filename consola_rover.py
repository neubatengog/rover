import serial
import glob
from Tkinter import *



class App:
	def __init__(self, master):
		frame = Frame (master)
		frame.pack()
		"""____________movimiento de camara, j, k , l , p____ """
		Label(frame, text = 'CAMARA',font = "Helvetica 12 bold",fg = "blue",
		 bg = "yellow"). grid(row=0, column=1)
		
		#boton de centrado de camara
		btnArriba = Button(frame, text='^', width=6, height=2, command=self.arriba)
		btnArriba.grid(row=1, column=1)
		
		#boton de movimiento izq de camara
		btnIzq = Button(frame, text='<<', width=6, height=2,command=self.izq)
		btnIzq.grid(row=2, column=0)

		#boton de movimiento de paneo 180 y centrado de camara
		btnPan = Button(frame, text='PANEO', width=6, height=2,command=self.pan)
		btnPan.grid(row=2, column=1)
		
		#boton de movimiento derecha de camara
		butDer = Button(frame, text='>>',width=6, height=2, command=self.der)
		butDer.grid(row=2, column=2)		
		"""_______________ fin movimiento__________________ """

		"""_______________ movimiento rover__________________"""
		Label(frame, text = 'ROVER', font = "Helvetica 12 bold",fg = "blue",
		 bg = "yellow"). grid(row=6, column=1)
		
		#boton de movimiento avanzar
		btnAvan = Button(frame, text='^',width=7, height=3, command=self.avanzar)
		btnAvan.grid(row=7, column=1)
		#boton de movimiento izquierda
		btnIz = Button(frame, text='<<',width=7, height=3, command=self.moveiz)
		btnIz.grid(row=8, column=0)
		#boton de movimiento derecha
		butDe = Button(frame, text='>>',  width=7, height=3, command=self.movede)
		butDe.grid(row=8, column=2)
		#boton de movimiento detener
		butStop = Button(frame, text='S',width=4, height=3, command=self.moveStop)
		butStop.grid(row=8, column=1)
		#boton de movimiento retroceder
		butRetro = Button(frame, text='V',width=7, height=3, command=self.retro)
		butRetro.grid(row=9, column=1)
		#boton de aumentar velocidad
		butAumentar = Button(frame, text='+',width=3, height=3, command=self.Aumentar)
		butAumentar.grid(row=7, column=3)
		#boton de disminuir velocidad
		butDisminuir = Button(frame, text='-',width=3, height=3, command=self.Disminuir)
		butDisminuir.grid(row=9, column=3)
		"""_______________ fin movimiento rover__________________"""
		
		#Puertos seriales detectados para seleccionar
		Label(frame, text = 'Puertos detectados:'). grid(row=13, column=0)
		listbox = Listbox(frame, height = 2, selectmode=SINGLE)
		listbox.bind("<<ListboxSelect>>",self.Conectar)
		for puerto in self.scan():
			listbox.insert(END, puerto)
		listbox.grid(row=13, column=1)

		self.accion = StringVar()
		Label(frame, 
					textvariable= self.accion,
					bg = "light green",
					font = "Helvetica 16 bold"
			).grid(row=17, column=1)


		

	#evento al seleccionar un puerto del listado
	def Conectar(self, event):
		w = event.widget
		index = int (w.curselection()[0])
		value = w.get(index)
		global ser
		ser = serial.Serial(value, 57600)
		ser.timeout = 1;
		
	#paneo de camara
	def pan(self):
		self.accion.set("PANEO")
		ser.write('p\n')

	#centrar el servo de la camara
	def arriba(self):
		self.accion.set("CAMARA CENT")
		ser.write('k\n')
	#movimiento izquierda camara	
	def izq(self):
		self.accion.set("<<<IZQ")
		ser.write('j\n')		
	#movimiento derecha camara
	def der(self):
		self.accion.set("DER>>>")
		ser.write('l\n')
	#movimiento avanzar rover
	def avanzar(self):
		self.accion.set("AVANZAR")
		ser.write('w\n')
	#movimiento retroceder rover
	def retro(self):
		self.accion.set("RETROCE")
		ser.write('s\n')
	#movimiento izquierda rover
	def moveiz(self):
		self.accion.set("<<< MOVER ")
		ser.write('w\n')
	#movimiento derecha rover
	def movede(self):
		self.accion.set("MOVER >>>")
		ser.write('d\n')
	#movimiento detener rover
	def moveStop(self):
		self.accion.set("DETENER")
		ser.write('s\n s\n')
	#movimiento aumentar velocidad rover
	def Aumentar(self):
		self.accion.set("VEL++")
		ser.write('+\n')
	#movimiento disminuir velocidad rover
	def Disminuir(self):
		self.accion.set("VEL--")
		ser.write('-\n')

	""" Funcion que scanea las rutas fisicas de los puertos seriales """
	def scan(self):
		return glob.glob('/dev/tty.*') + glob.glob('/dev/ttyUSB*') + glob.glob('/dev/ttyACM*')


if __name__=='__main__':	
	principal = Tk()
	#titulo de la ventana
	principal.wm_title('ROVER')
	#tamano de la ventana principal
	principal.geometry("450x350")
	app = App(principal)
	principal.mainloop()
	
