#Connect4

from random import randint

class Pieces:
	def __init__(self, pieces):
		self.pieces = pieces

	def getPieces(self):
		return self.pieces


def findPossibleMoves(board):
	possiblemoves = []
	for i in range(0,7):
		nextmoveindex = i
		while nextmoveindex < 42 and board[nextmoveindex] != 0:
			nextmoveindex += 7 # finds first available slot in column
		possiblemoves.append(nextmoveindex)
	possiblemoves = sorted(possiblemoves)
	return possiblemoves



def findPieces(board, user):
	pieces = []	# this represents the pieces of one player to see if they connect
	for i in range(0, len(board)):
		if board[i] == user:
			pieces.append(i)
	return pieces

def runEval(board, user, recursion):
	possiblemoves = findPossibleMoves(board)
	pieces = findPieces(board, user)
	opening = 0
	if not pieces:
		opening = 1
	if opening == 0 and len(pieces) < 2:
		opening = 1
	if opening == 1:
		open = []
		for i in range(1, 6):
			if board[i] == 0:
				open.append(i)
		int = randint(0, (len(open) - 1))
		MOVE = open[int]
		return MOVE
	evaluations = {} # eval : moveIndex
	for moveindex in possiblemoves:
		newPieces = pieces[:]
		newPieces.append(moveindex)
		newPieces = sorted(newPieces) # remove new moveindex after done
		index = eval(newPieces)
		evaluations[moveindex] = index
		x = 0
	largest = 0
	largestIndex = 0
	for i in evaluations:
		if evaluations[i] > largest:
			largest = evaluations[i]
			largestIndex = i
	if largest < 900:
		if recursion == 0:
			defense = runEval(board, 2, 1)
			if defense[0] >= largest:
				largestIndex = defense[1]
	if recursion == 1:
		return [largest, largestIndex]
	return largestIndex



def horizontal(pieces):
	starters = {} # store the starting index for each connection here, length of this dictionary is number of horizontal connections
	startVal = 0
	if len(pieces) > 1:
		for index in range(0, len(pieces)):
			if index == 0:
				startVal = pieces[index]
			if len(pieces) > 0:
				if pieces[0] == startVal:

					length = 0
					trap = 0 # check to terminate search
					while trap == 0:
						upper = index + length + 1
						lower = index + length
						if upper >= len(pieces): # check to see if upper is larger than the array
							trap = 1
							break
						if pieces[upper] - pieces[lower] == 1:
							while pieces[index + length + 1] - pieces[index + length] == 1:
								length += 1
								if len(pieces) <= index + length + 1:
									trap = 1
									break
								if length == 3:
									trap = 1
						else:
							trap = 1
					if length == 0:
						pieces.pop(index)
					if length > 0:
						starters[pieces[index]] = length
						for l in range(length, -1, -1):
							pieces.remove(pieces[index] + (l))
					trap = 0
					length = 0
				else:
					if len(pieces) > 1:
						reset = horizontal(pieces)
						if reset != {}:
							for piece in reset:
								starters[piece] = reset[piece]
	return starters


def inArray(needle, haystack):
	for i in haystack:
		if needle == i:
			return 1
	return 0





def positive(pieces, x):
# this makes sure that the function does not change pieces, which will be used further in the eval function
	starters = {}  # starting index: length                          [2, 10, 18, 19, 32] --> [19, 32]
	startVal = 0
	for index in range(0, (len(pieces) - 1)):

		if index == 0:
			startVal = pieces[index]
		if len(pieces) > 0:
			if pieces[0] == startVal:

				length = 0
				trap = 0  # check to terminate search
				if len(pieces) <= 1:
					trap = 1
				while trap == 0:
					needle = pieces[index] + (x * (length + 1))
					if inArray(needle, pieces) == 1:
						length += 1
						if index >= (len(pieces) - 1) or length == 3:
							trap = 1
					else:
						if length == 0:
							pieces.pop(index)
						trap = 1
				if length > 0:
					starters[pieces[index]] = length
					for l in range(length, -1, -1):
						pieces.remove(pieces[index] + (l * x))   #[19, 32]


				trap = 0
				length = 0
			else:
				if len(pieces) > 1:
					reset = positive(pieces, x)
					if reset != {}:
						for piece in reset:
							starters[piece] = reset[piece]
	return starters



def manyInArray(needle, haystack):
	count = 0
	for i in haystack:
		if i == needle:
			count += 1
	return count

def eval(newPieces):
	# winning move = 900
		# vertical, difference of 7
		# horizontal, difference of 1
		# positive slope, difference of 8
		# negative slope, difference of 6
	# connect3 = 100
	# connect2 = 50
	# connect1 = 10
	# user = 2, cpu = 1

# make class that has one property (pieces), and one method(getPieces). This makes the property unchangeable
	vpieces = newPieces
	negPieces = vpieces[:]
	posPieces = vpieces[:]
	vertPieces = vpieces[:]
	horPieces = vpieces[:]

	vert = positive(vertPieces, 7)

	hor = horizontal(horPieces)

	pos = positive(posPieces, 8)

	neg = positive(negPieces, 6)

	coll = [vert, hor, pos, neg]
	connects = []
	for i in range(0, len(coll)):
		for key in coll[i]:
			connects.append(coll[i][key])
	eval = 0
	if len(connects) == 0:
		eval = 0
		return eval
	connect4 = manyInArray(3, connects)
	if connect4 >= 1: # return 900 * count
		eval += 900 * connect4
	connect3 = manyInArray(2, connects)
	if connect3 >= 1:
		eval += 100 * connect3
	connect2 = manyInArray(1, connects)
	if connect2 >= 1:
		eval += 50 * connect2
	return eval





	

	





# ------GAMEPLAY-----------------------------------------------------------------------------------------------------------
def removeCommas(sub):
	sub = str(sub)
	newSub = sub.replace(",", " ")
	return newSub





def showBoard(board):
	dimensional = []
	count = 0
	for i in range(5, -1, -1):
		beg = i * 7
		end = (i+1)*7
		sub = board[beg:end]
		newSub = removeCommas(sub)
		dimensional.append(newSub)
	for row in dimensional:
		print row



def letsPlay():
	print "I am player 1 and you are player 2."
	print "Columns are numbered 0 to 6 from left to right."
	# lines of 10, 6 rows x7 columns = 42
	board = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
				0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
				0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
				0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
				0, 0]
	

	#start repetetive process here
	end = 0
	opening = 0
	while end == 0:
		board = userTurn(board)
		board = cpuTurn(board)
		if board == 0:
			end = 1
			break
		else:
			showBoard(board)
			if opening == 1:
				end = win(board, 2)
			elif opening == 0:
				totalPieces = len(findPieces(board, 1)) + len(findPieces(board, 2))
				if totalPieces > 3:
					opening = 1



def win(board, user):
	end = 0
	userPieces = findPieces(board, user)
	if eval(userPieces) >= 900:
		end = 1
	return end


def userTurn(board):
	trap = 0
	print "Your move. Which avaliable column would you like to move in?"
	opponentmove = raw_input()
	#if opponentmove == "checkCPU":
	#	cpuPieces = findPieces(board, 1)
	#	index = runEval(board, 1, 0)
	#	checkCPUBoard = board[:]
	#	checkCPUBoard[index] = 1
	#	print "CPU next move is " + str(index) + " with an eval of " + str(eval(findPieces(checkCPUBoard, 1)))
	#	board = userTurn(board)
	#	trap = 1
	if trap == 0:
		exactoppmove = int(opponentmove)
		check = 0
		while board[exactoppmove] != 0 and check == 0: #check to see if user has exceeded their chosen column
			if exactoppmove < 35:
				exactoppmove += 7
			else:
				check = 1
		if check == 1:
			print "That column is already full."
			return userTurn(board)
		board[exactoppmove] = 2
	return board


def cpuTurn(board):
	if eval(findPieces(board, 1)) >= 900:
		print "That's connect four! I won!"
		return 0
	index = runEval(board, 1, 0)
	board[index] = 1
	while index >= 7:
		index -= 7
	print "I'll play column " + str(index) + "."
	return board
	


def newTurn(board, user):
	if board == 0:
		return 0	
	index = runEval(board, user, 0)
	if win(board, user) == 1:
		print "newTurn! That's connect four! User " + str(user) + " won!"
		return 0
	newIndex = index
	while newIndex >= 7:
		newIndex -= 7
	print "I'll play column " + str(newIndex) + "."
	board[index] = user
	return board



def cpuPlay():
	board = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
				0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
				0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
				0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
				0, 0]
	end = 0
	opening = 0
	while end == 0:
		board = newTurn(board, 1)
		board = newTurn(board, 2)
		if board == 0:
			end = 1
			break
		else:
			showBoard(board)
			if opening == 1:
				end = win(board, 2)
				end = win(board, 1)
			elif opening == 0:
				totalPieces = len(findPieces(board, 1)) + len(findPieces(board, 2))
				if totalPieces > 3:
					opening = 1



letsPlay()

#cpuPlay()




























