# LifeOfPy
A Python (learning) version of Conway's Game of Life

**************************************************************
**                CONWAY'S  GAME OF LIFE                   **
**************************************************************
              A (For Learnig) Python's Version
                by: Guillermo Ibáñez Pupareli  @guilloip 

**Rules:**

 		-departs from infinit (periodic) matrix with cells 
 		-cells have two states alive (1) or dead (0)
 		-Each turn, for each cells, its alive neiborths are counted:
 			-exactly 3 alives neigborths if dead turn to live
 			-less than 2 or more than 3 : dies (or keep dead)
 			-otherwise: remains in it state


			
**Structure:**

		-class LifGame : responsable for playing the game itsalfe
		-class BtnFrame : GUI to show and change the matrix's cells
			-class BtnCell : A button to show and change an individual cell
		-class Window : Holds BtnFrame and control buttons, and so...
		-root is the main app window

***
Classes' desctiption
***

**class LifeGame :**

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
			setm(m) and setm0(m) : sets the whole matrices at once m must be a np.array of dimensions nx,ny 
			getm and getm0 : returns m or m0
			getsum(i,j) : counts alive neightborts arround cell (i,j)
			newState(i,j) : sets m[i,j] evaluating m0 with getsum(i,j)
			step(i,j) : do a whole step as explained before

***********************
GUI starts here
***********************

**class CellBtn(Button) :**

	Creates a button for showing and changing 1 cell
		input:
			i,j place of the cell in the represented matrix
			holder = LifeGame object attached to
			cols = tuplet with dead an alive colors
			val = 0 if dead else 1
			other buttons parameters
			
		text: it will be automatically set with number of alive neighbords
		
		funtions:
			set(val): turns button to its val and modified m0 in associated LifeGame Object also sets button's text value
			flip: changes it state (used for button pressing)

**class BtnFrame(Frame) :**

	Frame to hold the cells buttons (matrix holder)
		input:
			rows and columns
			other frame params
		funtions:
			set(m): set all the buttons from an np.array m
			clear() : set all to 0 

**class Window(Frame) :**

	Main window: holds BtnFram other control buttons
		Its function is to control everything (start, stop, clear,...)
		In the future migt save, go backward and so.
