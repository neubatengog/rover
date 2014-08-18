import serial
import glob
from Tkinter import *


""" Funcion que scanea las rutas de los puertos seriales """
def scan():
    """Scan de puertos habilitados serial (linux, OSX) """
    return glob.glob('/dev/tty.*') + glob.glob('/dev/ttyUSB*') + glob.glob('/dev/ttyACM*')

class App:


	
	def __init__(self, master):
		frame = Frame (master)
		frame.pack()
		"""____________movimiento de camara, j, k , l , p____ """
		Label(frame, text = 'CAMARA'). grid(row=0, column=1)
		
		#boton de centrado de camara
		btnArriba = Button(frame, text='^', command=self.arriba)
		btnArriba.grid(row=1, column=1)
		
		#boton de movimiento izq de camara
		btnIzq = Button(frame, text='<<', command=self.izq)
		btnIzq.grid(row=2, column=0)

		#boton de movimiento de paneo 180 y centrado de camara
		btnPan = Button(frame, text='PANEO', command=self.pan)
		btnPan.grid(row=2, column=1)
		
		#boton de movimiento derecha de camara
		butDer = Button(frame, text='>>', command=self.der)
		butDer.grid(row=2, column=2)		
		"""_______________ fin movimiento__________________ """

		"""_______________ movimiento rover__________________"""
		Label(frame, text = 'ROVER'). grid(row=6, column=1)
		
		#boton de movimiento avanzar
		btnAvan = Button(frame, text='^', command=self.avanzar)
		btnAvan.grid(row=7, column=1)
		#boton de movimiento izquierda
		btnIz = Button(frame, text='<<', command=self.moveiz)
		btnIz.grid(row=8, column=0)
		#boton de movimiento derecha
		butDe = Button(frame, text='>>', command=self.movede)
		butDe.grid(row=8, column=2)
		#boton de movimiento detener
		butStop = Button(frame, text='S', command=self.moveStop)
		butStop.grid(row=8, column=1)
		#boton de movimiento retroceder
		butRetro = Button(frame, text='V', command=self.retro)
		butRetro.grid(row=9, column=1)
		#boton de aumentar velocidad
		butAumentar = Button(frame, text='+', command=self.Aumentar)
		butAumentar.grid(row=7, column=3)
		#boton de disminuir velocidad
		butDisminuir = Button(frame, text='-', command=self.Disminuir)
		butDisminuir.grid(row=9, column=3)
		"""_______________ fin movimiento rover__________________"""
		
		#Puertos seriales detectados para seleccionar
		Label(frame, text = 'PUERTO SERIAL'). grid(row=13, column=0)
		listbox = Listbox(frame, height = 2, selectmode=SINGLE)
		listbox.bind("<<ListboxSelect>>",self.Conectar)
		for puerto in scan():
			listbox.insert(END, puerto)
		listbox.grid(row=13, column=1)

		

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
		print ('PANEO')
		ser.write('p\n')
	#centrar el servo de la camara
	def arriba(self):
		print ('<<<--CENT--->>>')
		ser.write('k\n')
	#movimiento izquierda camara	
	def izq(self):
		print ('<<<--IZQ')
		ser.write('j\n')		
	#movimiento derecha camara
	def der(self):
		print ('DER-->>>')
		ser.write('l\n')
	#movimiento avanzar rover
	def avanzar(self):
		print('AVANZA')
		ser.write('w\n')
	#movimiento retroceder rover
	def retro(self):
		print('RETRO')
		ser.write('s\n')
	#movimiento izquierda rover
	def moveiz(self):
		print('<<< MOVER ')
		ser.write('w\n')
	#movimiento derecha rover
	def movede(self):
		print('MOVER >>>')
		ser.write('d\n')
	#movimiento detener rover
	def moveStop(self):
		print('STOP!!!')
		ser.write('s\n s\n')
	#movimiento aumentar velocidad rover
	def Aumentar(self):
		print('+++')
		ser.write('+\n')
	#movimiento disminuir velocidad rover
	def Disminuir(self):
		print('---')
		ser.write('-\n')

if __name__=='__main__':	
	principal = Tk()
	#titulo de la ventana
	principal.wm_title('ROVER')
	#tamaño de la venta principal
	principal.geometry("400x400")
	app = App(principal)
	principal.mainloop()
	
