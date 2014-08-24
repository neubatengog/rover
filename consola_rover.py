import serial
import glob

from Tkinter import *
import tkMessageBox

from PIL import Image, ImageTk

import Queue
import threading

import videocapture #clase para manejo de video




class App:
	def __init__(self, master):

		
		self.ser = None

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

		self.w2 = Scale(frame,
				from_=0, 
				to=180, 
				length=400, 
				tickinterval=20, 
				orient=HORIZONTAL)
		self.w2.set(90)
		self.w2.bind("<ButtonRelease-1>", self.valorSlider)

		self.w2.grid(row=3, column=0, columnspan=4)
		"""_______________ fin movimiento__________________ """

		"""_______________ movimiento rover___________a, s,d, w, e____"""
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
		butStop = Button(frame, text='STOP',width=4, height=3, command=self.moveStop)
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

		
		butVideo = Button(frame, text='Video',width=3, height=3, command=self.ventana)
		butVideo.grid(row=18, column=1)

	
	def ventana(self):
		#q = Queue.Queue()
		t = threading.Thread(target=videocapture.Player().main, name='captura')
		t.daemon = True #si se cierra el hilo principal, se cierra el video 
		t.start()


	#valores de barra slice de 0 a 180
	def valorSlider(self, event):
		try:
			self.ser.write(string(self.w2.get())+"\n")	
		except Exception, e:
			tkMessageBox.showinfo("Error", "No se ha podido enviar la orden \n verifique el puerto serial")
			

	"""evento al seleccionar un puerto del listado para conectar
	 con el puerto serial seleccionado de la lista"""
	def Conectar(self, event):
		w = event.widget
		index = int (w.curselection()[0])
		value = w.get(index)
		try:
			if self.ser == None:
				self.ser = serial.Serial(value, 57600)
				self.ser.timeout = 1;
				self.accion.set("CONECTADO")
			else:
				if self.ser.isOpen():
					self.ser.close()
					self.ser=None
					tkMessageBox.showinfo("Error", "El puerto ya se encuentra abierto")
				else:
					self.ser.open()
		except serial.SerialException, e:
			tkMessageBox.showinfo("Error", "problema al conectar el puerto serial seleccionado")

	#paneo de camara
	def pan(self):
		try:
			self.accion.set("PANEO")
			self.ser.write('p\n')
		except Exception, e:
			tkMessageBox.showinfo("Error", "No se ha podido enviar la orden \n verifique el puerto serial")
			
	#centrar el servo de la camara
	def arriba(self):
		self.accion.set("CAMARA CENT")
		try:
			self.ser.write('k\n')
		except Exception, e:
			tkMessageBox.showinfo("Error", "No se ha podido enviar la orden \n verifique el puerto serial")

		
	#movimiento izquierda camara	
	def izq(self):
		try:
			self.accion.set("<<<IZQ")
			self.ser.write('j\n')	
		except Exception, e:
			tkMessageBox.showinfo("Error", "No se ha podido enviar la orden \n verifique el puerto serial")
	
	#movimiento derecha camara
	def der(self):
		try:
			self.accion.set("DER>>>")
			self.ser.write('l\n')
		except Exception, e:
			tkMessageBox.showinfo("Error", "No se ha podido enviar la orden \n verifique el puerto serial")

	#movimiento avanzar rover
	def avanzar(self):
		try:
			self.accion.set("AVANZAR")
			self.ser.write('w\n')
		except Exception, e:
			tkMessageBox.showinfo("Error", "No se ha podido enviar la orden \n verifique el puerto serial")

	#movimiento retroceder rover
	def retro(self):
		try:
			self.accion.set("RETROCE")
			self.ser.write('s\n')
		except Exception, e:
			tkMessageBox.showinfo("Error", "No se ha podido enviar la orden \n verifique el puerto serial")

	#movimiento izquierda rover
	def moveiz(self):
		try:
			self.accion.set("<<< MOVER ")
			self.ser.write('a\n')
		except Exception, e:
			tkMessageBox.showinfo("Error", "No se ha podido enviar la orden \n verifique el puerto serial")

	#movimiento derecha rover
	def movede(self):
		try:
			self.accion.set("MOVER >>>")
			self.ser.write('d\n')
		except Exception, e:
			tkMessageBox.showinfo("Error", "No se ha podido enviar la orden \n verifique el puerto serial")

	#movimiento detener rover
	def moveStop(self):
		try:
			self.accion.set("DETENER")
			self.ser.write('e\n')
		except Exception, e:
			tkMessageBox.showinfo("Error", "No se ha podido enviar la orden \n verifique el puerto serial")

	#movimiento aumentar velocidad rover
	def Aumentar(self):
		try:
			self.accion.set("VEL++")
			self.ser.write('+\n')
		except Exception, e:
			tkMessageBox.showinfo("Error", "No se ha podido enviar la orden \n verifique el puerto serial")


	#movimiento disminuir velocidad rover
	def Disminuir(self):
		try:
			self.accion.set("VEL--")
			self.ser.write('-\n')
		except Exception, e:
			tkMessageBox.showinfo("Error", "No se ha podido enviar la orden \n verifique el puerto serial")

	""" Funcion que scanea las rutas fisicas de los puertos seriales """
	def scan(self):
		return glob.glob('/dev/tty.*') + glob.glob('/dev/ttyUSB*') + glob.glob('/dev/ttyACM*')





if __name__=='__main__':	
	principal = Tk()
	#titulo de la ventana
	principal.wm_title('ROVER')
	#tamano de la ventana principal
	principal.geometry("450x550")
	principal.bind(('<Escape>') , lambda e : principal.quit())

	app = App(principal)

	principal.mainloop()
	
	
	
