import string
import sys
import re
import math
import decimal

#-------- FUNCTIONS ------------------------------------------------------------#

def fixexp(num):
# FIX EXPONENT FORMATTING
		
	num = re.sub(r"(\d)\.", r".\1", num)
	exp = re.search(r"E([+-]\d+)", num)
	newexp = "E{:+03}".format(int(exp.group(1))+1)
	num = re.sub(r"E([+-]\d+)", newexp, num)

	
	if 'E+00' in num:
		num = num[:-4]
	
	return num	

def fixcol(num,col,prev):
# FIX COLUMN SPACING
		
	flag = False
	flagPrev = False
	
	if 'E' in num:
		flag = True
	if 'E' in prev:
		flagPrev = True
	
	if (col == 0 and flag):
		num = (num.rjust(15))
	elif (col == 0)	:
		num = (num.rjust(11))
	elif ((col == 1 or col == 2 or col == 3 or col == 4) and flagPrev and flag):
		num = (num.rjust(14))
	elif ((col == 1 or col == 2 or col == 3 or col == 4) and flagPrev):
		num = (num.rjust(10))
	elif ((col == 1 or col == 2 or col == 3 or col == 4) and flag):
		num = (num.rjust(18))
	elif (col == 1 or col == 2 or col == 3 or col == 4):
		num = (num.rjust(14))
	else:
		print ('ERROR IN FIXCOL FUNCTION')
		num = '0'
	
	return num	
	
#-------------------------------------------------------------------------------#

f = open('alfps.asc','r')
text_file = open('Output.txt', "w")

temp = []
InputSize, InputData1, InputData2, InputData3 = ([] for i in range(4))
InputData, TempInputData, NewInputData, In = ([] for i in range(4))
Data, NewData = ([] for i in range(2))

#-------- DATA EXTRACTION ------------------------------------------------------#

for line in f:
	line = line.strip()
	
	while any(s in line for s in '*'):
		text_file.write(line + '\n')
		line = next(f)
		line = line.strip()

	InputData, TempInputData, NewInputData, In = ([] for i in range(4))
	Title = line.split()
	NumInputs = (len(Title) - 1) / 2
	text_file.write(('/FUNC'+'\n'))
        text_file.write(Title[0] + ' ' + ' '.join(Title[-NumInputs:]) + '\n')
        text_file.write(' '.join(Title[0:NumInputs+1]) + '\n')
	startInData = NumInputs + 1
	InputSize = []
	InputData = []
	print(Title)
		
	#Match input name to number
	TotalData = 1
	for j in range(0,NumInputs):
		temp = int(Title[j+startInData])
		InputSize.append(temp)
		TotalData = TotalData * temp
		
	TotalInputData = sum(InputSize)
	
	if any(s in line for s in 'sin'):
		line = next(f)
		line = line.strip()	
		
#-------- INPUT DATA -----------------------------------------------------------#

	#--- Read Input Data ---#
	line = next(f)
	if any(s in line for s in 'sin'):
		line = next(f)
		line = line.strip()		
		
	DataRead = 0
	while (DataRead < TotalInputData):
		CurrentLine = line.split()
		InputData.extend(CurrentLine)
		DataRead = DataRead + float(len(CurrentLine))
		line = next(f)

	InputData = map(float,InputData)
	
	#--- Format Input Data ---#		
	i = 0	
	while (i < len(InputData)):
		dec = abs(decimal.Decimal(str(InputData[i])).as_tuple().exponent)
		if InputData[i] < 0:
			prec = (9 - (len(str(InputData[i])))) + dec
		else:
			prec = (8 - (len(str(InputData[i])))) + dec
		
		if(InputData[i] == 0):
                        InputData[i] = '0.0000000E+00'
	
		elif((abs(InputData[i])>0)):
		#InputData[i] = ('{:.6E}'.format(float(InputData[i])))
                        InputData[i] = ('{:.6E}'.format(InputData[i]))
			InputData[i] = InputData[i]
		else:	
			temp =  '%.f' % (prec, InputData[i])
			InputData[i] = temp
				
		TempInputData.append(InputData[i])
		i = i+1		

	#--- Order Input Data ---#
	if NumInputs == 3:
		InputData[0] = TempInputData[(len(TempInputData) - InputSize[0]):]
		InputData[2] = TempInputData[0:(InputSize[2])]
		InputData[1] = TempInputData[InputSize[2]:(InputSize[2]+InputSize[1])]	
	elif NumInputs == 2:
		InputData[0] = TempInputData[(len(TempInputData) - InputSize[0]):]
		InputData[1] = TempInputData[:InputSize[1]]		
	elif NumInputs == 1:
		InputData[0] = TempInputData
	
	#--- Pring Input Data by Column ---#
	for j in range(0,NumInputs):
	
		element = 0
		i = 0
		col = 0
		currInRow = 1
		dataBlockInRow = 1
		rowInSize = math.ceil(float(InputSize[j])/5.0)
		numInFinalRow = int(5 - ((5*rowInSize) - InputSize[j]))
	
		while (currInRow <= rowInSize):
			if(dataBlockInRow < rowInSize):
				prev = '0'
				for element in range(i,i+5):
					space = True
					temp = InputData[j][element]
					test2 = fixcol(temp,col,prev)
					NewInputData.append(test2)
					col = col + 1
					prev = temp
					if ('E' in temp): space = False
					if (col == 5 and space):
						NewInputData.append('   ')
					
				element = element + 1
				i = element
				col = 0
				dataBlockInRow = dataBlockInRow + 1
			
			elif(dataBlockInRow == rowInSize):
				prev = '0'
				for element in range(i,i+numInFinalRow):
					space = True
					temp = InputData[j][element]
					test2 = fixcol(temp,col,prev)
					NewInputData.append(test2)
					col = col +1
					prev = temp
					if ('E' in temp): space = False
					if (col == numInFinalRow and space):
						NewInputData.append('   ')
							
				element = element + 1
				i = element
				col = 0
				dataBlockInRow = 1
				
			else:
				print('ERROR IN FORMATTING LOOP')
				
			print(' '.join(NewInputData[0:]))	
			text_file.write( ' '.join(NewInputData[0:]) + '\n')
			NewInputData = []
			currInRow = currInRow + 1		
		
#-------- TABLE DATA -----------------------------------------------------------#

	#--- Read Table Data ---#
	DataRead = 0
	CurrentLine = line.split()
	Data = CurrentLine
	DataRead = float(len(CurrentLine))
	
	while (DataRead < TotalData):
		line = next(f)
		CurrentLine = line.split()
		Data.extend(CurrentLine)
		DataRead = DataRead + float(len(CurrentLine))
	
	Data = map(float,Data)

	#--- Format and Print Table Data ---#
	if (sum(InputSize) > 0):	
		element = 0
		i = 0
		col = 0
		currRow = 1
		dataBlockRow = 1
		rowSize = math.ceil(InputSize[0]/5.0)
		numInFinalRow = int(5 - ((5*rowSize) - InputSize[0]))
		totalRows = rowSize
	
		for j in range(1,NumInputs):
			totalRows = totalRows * InputSize[j]
		
		while (currRow <= totalRows):

			if(dataBlockRow < rowSize):
			
				prev = '0'
				for element in range(i,i+5):
					space = True
					dec = abs(decimal.Decimal(str(Data[element])).as_tuple().exponent)
					if Data[element] < 0:
						prec = (9 - (len(str(Data[element])))) + dec
					else:
						prec = (8 - (len(str(Data[element])))) + dec
				
					if Data[element] == 0:
						Data[element] = '0.0000000E+00'
						temp = Data[element]
					else:
							Data[element] = ('{:.6E}'.format(Data[element]))
							temp = Data[element]
						
					test2 = fixcol(temp,col,prev)
					NewData.append(test2)
					col = col + 1
					prev = temp
					if ('E' in temp): space = False
					if (col == 5 and space):
						NewData.append('   ')
					
				element = element + 1
				i = element
				col = 0
				dataBlockRow = dataBlockRow + 1
			
			elif(dataBlockRow == rowSize):
			
				prev = '0'
				for element in range(i,i+numInFinalRow):
					space = True
					dec = abs(decimal.Decimal(str(Data[element])).as_tuple().exponent)
					if Data[element] < 0:
						prec = (9 - (len(str(Data[element])))) + dec
					else:
						prec = (8 - (len(str(Data[element])))) + dec
						
					if Data[element] == 0:
						Data[element] = '0.0000000E+00'
						temp = Data[element]
					else:
							Data[element] = ('{:.6E}'.format(Data[element]))
							temp = Data[element]
					
					test2 = fixcol(temp,col,prev)
					NewData.append(test2)
					col = col +1
					prev = temp
					if ('E' in temp): space = False
					if (col == numInFinalRow and space):
						NewData.append('   ')
							
				element = element + 1
				i = element
				col = 0
				dataBlockRow = 1
				
			else:
				print('ERROR IN FORMATTING LOOP')
	
			
			print(' '.join(NewData[0:]))
			if (currRow == totalRows):
				text_file.write( ' '.join(NewData[0:]))
			else:
				text_file.write( ' '.join(NewData[0:]) + '\n')
				
			NewData = []
			currRow = currRow + 1
			
		text_file.write('\n')	
		line = next(f)
	else:
		text_file.write('.0000000E+00')
		NewData = []
		currRow = currRow + 1
		text_file.write('\n')	
		line = next(f)
				
#	text_file.close()
#	break





