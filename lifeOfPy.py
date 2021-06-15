'''
**************************************************************
***                     Life Of Py                         ***
**************************************************************


              A (For Learnig) Python's Version
                by: Guillermo Ibáñez Pupareli 



It is incomplete, it might never be completed
It is given as it is, no garanties given
100% Free to use/copy/distribute or change
Only attached to the restrictions of its libraries
'''
from tkinter import *
import numpy as np
'''
	Conway's Life Game for (learning) Python
	guilloip@guilloip.com
	
	Rules:
		-departs from infinit (periodic) matrix with cells 
		-cells have two states alive (1) or dead (0)
		-Each turn, for each cells, its alive neiborths are counted:
			-exactly 3 alives neigborths if dead turn to live
			-less than 2 or more than 3 : dies (or keep dead)
			-otherwise: remains in it state
			
	Structure:
		-class LifGame : responsable for playing the game itsalfe
		-class BtnFrame : GUI to show and change the matrix's cells
			-class BtnCell : A button to show and change an individual cell
		-class Window : Holds BtnFrame and control buttons, and so...
		-root is the main app window
'''


class LifeGame :
	'''
	Game of Life itself:
		Has two np.arrays: m and m0.
			m0 is original state
			calculates the new state and store it in m
			then m0=m
		Input:
			nx : width of matrix
			ny : height of matrix
			(remember is infinit, this dimensions are the periocidity)
		Functions Members:
			reset : set all to 0 and ticks counter too.
			set0(i,j,val): change m0[i,j] to val
			set(i,j,val): change m[i,j] to val
			get and get0 : oposite to set
			setm(m) and setm0(m) : sets the whole matrices at once
				m must be a np.array of dimensions nx,ny 
			getm and getm0 : returns m or m0
			getsum(i,j) : counts alive neightborts arround cell (i,j)
			newState(i,j) : sets m[i,j] evaluating m0 with getsum(i,j)
			step(i,j) : do a whole step as explained before
	'''
	def __init__(self, nx, ny) :
		self.nx = nx
		self.ny = ny
		self.reset()
		
	def reset(self):
		self.m = np.zeros((self.nx,self.ny))
		self.m0 = np.zeros((self.nx,self.ny))
		self.ticks = 0

	def set0(self,i,j,val) :
		self.m0[i % self.nx,j % self.ny]=val

	def set(self,i,j,val):
		self.m[i % self.nx,j % self.ny]=val

	def get0(self,i,j):
		return int(self.m0[i % self.nx,j % self.ny])
		
	def get(self,i,j):
		return int(self.m[i % self.nx,j % self.ny])

	def getm(self):
		return self.m

	def getm0(self):
		return self.m0
		
	def setm0(self,m):
		self.m0 = m

	def setm(self,m):
		self.m = m

	def getsum(self,i,j):
		s=0
		for k in range(i-1,i+1+1) :
			for q in range(j-1,j+1+1) :
				if k!=i or j!=q :
					s +=self.get0(k,q)
		if self.get0(i,j)>0 :
			print(f"({i},{j}) = {s}")
		return s

	def newState(self,i,j) :
		g = self.getsum(i,j)
		if g<2 :
			return 0
		if g==2 :
			return self.get0(i,j)
		if g==3 :
			return 1
		if g>3 :
			return 0

	def step(self):
		for i in range(self.nx) :
			for j in range(self.ny) :
				self.m[i,j]=self.newState(i,j)
		#self.m0 = self.m (it will be done in other place)
		self.ticks += 1

	def getTicks(self):
		return self.ticks
		
	def __str__(self):
		return self.m

'''
***********************
GUI starts here
***********************
'''
class CellBtn(Button) :
	'''
	Creates a button for showing and changing 1 cell
		input:
			i,j place of the cell in the represented matrix
			holder = LifeGame object attached to
			cols = tuplet with dead an alive colors
			val = 0 if dead else 1
			other buttons parameters
			
		text: it will be automatically set with number of alive neighbords
		
		funtions:
			set(val): turns button to its val and modified m0 in associated LifeGame Object
					also sets button's text value
			flip: changes it state (used for button pressing)
	'''
	def __init__ (self, master=None,i=0,j=0,val=0,holder=None,cols=("#FFFFFF","#000000"), **kw) :
		Button.__init__(self, master,kw,command=self.flip)
		self.cols = cols
		self.master = master
		self.val = val
		self.holder = holder
		self.i=i
		self.j=j
		self.set(0)

	def set(self,val):
		self.val=val
		self.config(bg=self.cols[self.val],activebackground=self.cols[self.val])
		self.config(fg=self.cols[not self.val],activeforeground=self.cols[not self.val])
		self.holder.set0(self.i,self.j,self.val)
		s=self.holder.getsum(self.i,self.j)
		self.config(text=str(s))

	def flip(self) :
		self.set(val = not self.val)


#buttom matrix class
class BtnFrame(Frame) :
	'''
	Frame to hold the cells buttons (matrix holder)
		input:
			rows and columns
			other frame params
		funtions:
			set(m): set all the buttons from an np.array m
			clear() : set all to 0 
	'''
	def __init__ (self,rows,columns,master=None,holder=None):
		Frame.__init__(self,master)
		self.master=master
		self.rows=rows
		self.columns=columns
		self.buttons=[]
		for i in range(rows) :
			buttonsrow = []
			for j in range(columns) :
				btn = CellBtn(self,text=" ",i=i,j=j,val=0,holder=holder)
				btn.grid(column=j, row=i)
				buttonsrow.append(btn)
			self.buttons.append(buttonsrow)

	def set(self,m):
		for i in range(len(self.buttons)):
			for j in range(len(self.buttons[i])):
				self.buttons[i][j].set(int(m[i,j]))
				
	def clear(self):
		m = np.zeros((self.rows,self.columns))
		self.set(m)


class Window(Frame) :
	'''
	Main window: holds BtnFram other control buttons
		Its function is to control everything (start, stop, clear,...)
		In the future migt save, go backward and so.
	'''
	def __init__(self, master=None) :
		Frame.__init__(self,master)
		self.master = master
		self.init_window()
		self.stopped=True


	def init_window(self) :
		#seting window
		self.master.title("Life Of Py")
		self.pack(fill=BOTH,expand=1)
		self.lg = LifeGame(20,20)
		self.world = BtnFrame(master=self,rows=20,columns=20,holder=self.lg)
		self.world.pack(side=TOP)
		self.world.set(self.lg.getm())
		#self.m = np.zeros((10,10))
		#for i in range(10) :
		#	self.m[i,i] = 1
		#self.world.set(self.m)
		cFrame = Frame(self)
		cFrame.pack(side=TOP)
		btn = Button(cFrame,text="CLEAR",command=self.clear)
		btn.pack(side=LEFT)
		btn = Button(cFrame,text="STEP",command=self.step)
		btn.pack(side=LEFT)
		btn = Button(cFrame,text="EVAL",command=self.eval)
		btn.pack(side=LEFT)
		self.playbtn = Button(cFrame,text="PLAY",command=self.playpause)
		self.playbtn.pack(side=LEFT)

	def clear(self):
		self.lg.reset()
		self.world.clear()

	def step(self) :
		self.lg.step()
		self.world.set(self.lg.getm())
		self.eval()
		#self.lg.setm0(self.lg.getm())

	def eval(self) :
		self.world.set(self.lg.getm0())
		
	def playpause(self) :
		if self.stopped :
			self.stopped=False
			self.playbtn.config(bg="black",fg="white",text="PAUSE")
			self.timer = self.after(200,self.play)
		else:
			self.stopped=True
			self.playbtn.config(fg="black",bg="white",text="PLAY")
			self.after_cancel(self.timer)
			
	def play(self) :
		self.step()
		self.timer = self.after(200,self.play)


root = Tk()
app = Window(root)
root.mainloop()
