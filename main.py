from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
import train

class MyGui():
	HEIGHT = 500
	WIDTH = 1000
	def __init__(self, root,img):
		self.root = root
		self.C = Canvas(root, height=self.HEIGHT, width=self.WIDTH)
		self.background_image= PhotoImage(file=img)
		self.background_label = Label(app, image=self.background_image)
		self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
		self.C.pack()
		self.frame = Frame(root,  bg='#42c2f4', bd=5)
		self.frame.place(relx=0.5, rely=0.3, relwidth=0.8, relheight=0.15, anchor='n')
		self.menu = self.Menubutton()
		self.about_our()

	def OpenImg(self,image,width,height):
	    self.img = Image.open(image)
	    self.img = self.img.resize((width,height), Image.ANTIALIAS)
	    self.img = ImageTk.PhotoImage(self.img)
	    return self.img
	

	def Menubutton(self):
		#set icon
		self.iconHome = self.OpenImg('icon/icons8-home-page-40.png',25,25)
		self.iconAbsen = self.OpenImg('icon/icons8-clock-40.png',25,25)
		self.iconTrain = self.OpenImg('icon/icons8-services-40.png',25,25)
		self.iconAdd = self.OpenImg('icon/icons8-plus-40.png',25,25)
		self.iconAbout = self.OpenImg('icon/icons8-about-40.png',25,25)
		self.iconExit = self.OpenImg('icon/icons8-cancel-40.png',25,25)

		self.Home = self.create_button("Home",self.iconHome,0,0.15,1,self.home)
		self.absen = self.create_button("Absen",self.iconAbsen,0.16,0.15,1,self.face_recognation)
		self.train= self.create_button('Train',self.iconTrain,0.32,0.15,1,self.train)
		self.About = self.create_button("About",self.iconAbout,0.48,0.15,1,self.about_our)
		self.addData= self.create_button("Tambah Data",self.iconAdd,0.64,0.2,1,self.addData)
		self.exit= self.create_button("Keluar",self.iconExit,0.85,0.15,1,self.quit)


	def create_button(self,text,icon,x,w,y,command):
		self.button = Button(self.frame,text=text,font = 40 ,bg='black',fg = 'white', image = icon, compound = LEFT, command= command)
		self.button.place(relx= x, relwidth = w , relheight = y)
	
	def face_recognation(self):
		import recognation
		self.detect = recognation.Detector()
		print("Exiting Program")
	def train(self):
		self.hide_pane()		
		self.train = train.Train()
		self.lower_frame = Frame(self.root, bg='#42c2f4', bd=10)
		self.lower_frame.place(relx=0.5, rely=0.4625, relwidth=0.8, relheight=0.1, anchor='n')
		self.label1 = Label(self.lower_frame,font=60, bg='#42c2f4',fg = 'black',text="Train Selesai !!")
		self.label1.pack()
		
	def addData(self):
		#to delete frame and text on pane
		self.hide_pane()

		self.lower_frame = Frame(self.root, bg='#42c2f4', bd=10)
		self.lower_frame.place(relx=0.5, rely=0.4625, relwidth=0.8, relheight=0.1, anchor='n')
		self.label = Label(self.lower_frame, font=60,fg = 'black', text="Nama :",  bg='#42c2f4')
		self.label.place(relx=0, relwidth=0.1,relheight=1)
		self.textbox = Entry(self.lower_frame, font=40)
		self.textbox.place(relx=0.11, relwidth=0.35,relheight=1)

		self.label2 = Label(self.lower_frame, font=60,fg = 'black', text="Jumlah Foto :",  bg='#42c2f4')
		self.label2.place(relx=0.48, relwidth=0.15,relheight=1)
		self.textbox2 = Entry(self.lower_frame, font=40)
		self.textbox2.place(relx=0.64, relwidth=0.2,relheight=1)

		self.submit = Button(self.lower_frame, text='Ambil Data',bg='black',fg = 'white', font=40,width= 10 ,command=self.getData)
		self.submit.place(relx=0.85, relwidth=0.15,relheight=1)
	
	def getData(self):

		self.nama = self.textbox.get()
		self.count = self.textbox2.get()
		import generat_dataset
		self.generat = generat_dataset.Generat(self.nama,self.count)

	def about_our(self):
		self.lower_frame = Frame(self.root, bg='#42c2f4', bd=10)
		self.lower_frame.place(relx=0.5, rely=0.4625, relwidth=0.8, relheight=0.4, anchor='n')
		self.about = Text(app, bg='#42c2f4', bd=10,fg='black')
		self.about.place(relx=0.5, rely=0.4625, relwidth=0.8, relheight=0.4, anchor='n')
		self.quote = """
		Our Team :
		1. Hilmi Adzin Pratama (18040210)
		2. Niza Fadila (18040030)
		3. Zahrul Azhari (18040218)

		Revisi dan Tambahan :
		- Menjadikan kode menjadi oop(object oriented programing)
		- fix bug
		- Menambahkan field tanggal pada tabel di database
		- Input Tambah data langsung dari GUI
		- Merapikan Susunan Direktori
		"""
		self.about.insert(END, self.quote)
	def home(self):
		self.hide_pane()
		self.lower_frame = Frame(self.root, bg='#42c2f4', bd=10)
		self.lower_frame.place(relx=0.5, rely=0.4625, relwidth=0.8, relheight=0.4, anchor='n')
		self.label = Label(self.lower_frame,font=120, text="SELAMAT DATANG DI APLIKASI ABSEN KELAS 4B", bg = 'black',fg ='white',height = 60 , width = 150, justify = CENTER)
		self.label.pack(padx = 20, pady = 20)
	
	def hide_pane(self):
		self.lower_frame.place_forget()
		self.about.place_forget()
	
	def quit(self):
		self.response = messagebox.askquestion("Aplikasi Absen" ,"Yakin Ingin Keluar ?")
		if(self.response == "yes"):
			print("Exiting Program")
			quit()

if __name__ == "__main__":
	app = Tk()
	app.title('Aplikasi Absen')
	app.iconbitmap('icon/sun_icon.ico')
	e = MyGui(app,"img/landscape.png")
	app.mainloop()