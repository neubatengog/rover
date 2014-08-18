import serial
import glob

from Tkinter import *



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


		Label(frame, text = 'ROVER'). grid(row=6, column=1)
		
		btnAvan = Button(frame, text='^', command=self.avanzar)
		btnAvan.grid(row=7, column=1)

		btnIz = Button(frame, text='<<', command=self.moveiz)
		btnIz.grid(row=8, column=0)

		butDe = Button(frame, text='>>', command=self.movede)
		butDe.grid(row=8, column=2)
		
		butStop = Button(frame, text='S', command=self.moveStop)
		butStop.grid(row=8, column=1)
		
		butRetro = Button(frame, text='V', command=self.retro)
		butRetro.grid(row=9, column=1)
		
		butAumentar = Button(frame, text='+', command=self.Aumentar)
		butAumentar.grid(row=7, column=3)
		
		butDisminuir = Button(frame, text='-', command=self.Disminuir)
		butDisminuir.grid(row=9, column=3)

		
		#Puertos seriales detectados para seleccionar
		Label(frame, text = 'PUERTO SERIAL'). grid(row=13, column=0)
		listbox = Listbox(frame, height = 2, selectmode=SINGLE)
		listbox.bind("<<ListboxSelect>>",self.Conectar)
		for puerto in scan():
			listbox.insert(END, puerto)
		listbox.grid(row=13, column=1)

		


	def Conectar(self, event):
		w = event.widget
		index = int (w.curselection()[0])
		value = w.get(index)
		global ser
		ser = serial.Serial(value, 57600)
		ser.timeout = 1;
		

	def pan(self):
		print ('PANEO')
		ser.write('p\n')

	def arriba(self):
		print ('<<<--CENT--->>>')
		ser.write('k\n')
		
	def izq(self):
		print ('<<<--IZQ')
		ser.write('j\n')		
		
	def der(self):
		print ('DER-->>>')
		ser.write('l\n')
	
	def avanzar(self):
		print('AVANZA')
		ser.write('w\n')
	
	def retro(self):
		print('RETRO')
		ser.write('s\n')
	
	def moveiz(self):
		print('<<< MOVER ')
		ser.write('w\n')
	
	def movede(self):
		print('MOVER >>>')
		ser.write('d\n')

	def moveStop(self):
		print('STOP!!!')
		ser.write('s\n s\n')
	
	def Aumentar(self):
		print('+++')
		ser.write('+\n')
	
	def Disminuir(self):
		print('---')
		ser.write('-\n')

if __name__=='__main__':	
	
		
	principal = Tk()
	principal.wm_title('ROVER')


	principal.geometry("400x400")
	app = App(principal)
	principal.mainloop()
	
