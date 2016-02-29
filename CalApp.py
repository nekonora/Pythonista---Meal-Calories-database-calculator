#------------------------------------------------------------
# coding: utf-8
#
#					Script: Meal Calories calculator - 1.0
#			    Author: Filippo Zaffoni
#			Written in: Pythonista 2.0
#
#	 Food Database: http://www.usda.gov/wps/portal/usda/usdahome
#
#------------------------------------------------------------

import ui

# --- Variables

foodNames = list()
foodCodes = list()
foodCals = list()
customGrams = 0
customCal = 0
currentCal = 0.0
currentCustomCal = 0.0
total = 0.0

# --- Dictionary |TO-DO: improve dictionary to translate terms from database|

dictionary = {
"FRSH": "fresh", "JUC": "juice",
"W/": "with", "PREP": "prepared",
"WO/": "without", "FRZ": "froze",
"UNSWTND": "unsweetened", "SKN": "skin",
"SWTND": "sweetened", "FRZ": "frozen",
"CKD": "cooked", "": "",
"": "", "": "",
}

# --- UI Elements

_NameLabel = ui.Label()
_NameLabel.text = "Food: "
_NameLabel.x = 10
_NameLabel.y = 400
_NameLabel.width = 480
_NameLabel.height = 40

_100CalLabel = ui.Label()
_100CalLabel.text = "Calories in 100g: "
_100CalLabel.x = 10
_100CalLabel.y = 430
_100CalLabel.width = 360
_100CalLabel.height = 40

_customCalLabel = ui.Label()
_customCalLabel.text = "Calories in "
_customCalLabel.x = 10
_customCalLabel.y = 460
_customCalLabel.width = 90
_customCalLabel.height = 40

_customGramsTextField = ui.TextField()
_customGramsTextField.placeholder = "100g"
_customGramsTextField.keyboard_type = ui.KEYBOARD_NUMBER_PAD
_customGramsTextField.x = 100
_customGramsTextField.y = 465
_customGramsTextField.width = 90
_customGramsTextField.height = 30
_customGramsTextField.text = ""

_customCalResLabel = ui.Label()
_customCalResLabel.text = ": "
_customCalResLabel.x = 200
_customCalResLabel.y = 460
_customCalResLabel.width = 90
_customCalResLabel.height = 40

_totalLabel = ui.Label()
_totalLabel.text = "Total calories:"
_totalLabel.x = 520
_totalLabel.y = 40
_totalLabel.width = 110
_totalLabel.height = 40

_totalLabelNumber = ui.Label()
_totalLabelNumber.text = "0"
_totalLabelNumber.x = 630
_totalLabelNumber.y = 40
_totalLabelNumber.width = 100
_totalLabelNumber.height = 40


# -------- Search Function

def search_tapped(sender) :
	input = sender.superview["_searchField"].text
	searchTerm = input.upper()
	table = sender.superview["_foodListView"].data_source.items
	tableView = sender.superview["_foodListView"]
	del table[:]
	del foodCodes[:]
	del foodNames[:]
	del foodCals[:]
	database = open("food_database.txt", "r")
	for line in database :
		foodItem = line.split("^")
		if searchTerm in foodItem[1]  :			
			
			# --- Correct abbrevations in database names
			for word, correction in dictionary.items() :
				foodItem[1] = foodItem[1].replace(word, correction)
			
			foodName = foodItem[1].strip("~").capitalize().replace(",", ", ")
			foodCode = foodItem[0].strip("~")
			foodCal = foodItem[2]
			foodCodes.append(foodCode)
			foodNames.append(foodName)
			foodCals.append(foodCal)
			table.append(foodName)
	database.close()		

# --- Udate info |TO-DO: implement autoupdate on textfield edited feature|
	
def cell_pressed(sender) :
	selected = sender.selected_row
	_NameLabel.text = ("Food: %s" % foodNames[selected])
	_100CalLabel.text = ("Calories in 100g: %s cal" % foodCals[selected])
	global currentCal 
	currentCal = float(foodCals[selected])

# --- Calculate custom cal

def calculate_cal(sender) :
	grams = float(_customGramsTextField.text)
	result = int((currentCal / 100) * grams)
	_customCalResLabel.text = (": %d cal" % result)
	global currentCustomCal
	currentCustomCal = result
	
# --- Add buttons |TO-DO: Rewrite total meal calories UI in order to edit added foods|
	
def add_100cal(sender) :
	global total
	total += currentCal
	_totalLabelNumber.text = str(total)
	
	
def add_customCal(sender) :
	global total
	total += currentCustomCal
	_totalLabelNumber.text = str(total)


# --- Reset Button

def reset_button(sender) :
	global total
	total = 0.0
	_totalLabelNumber.text = str(total)

# --- View Loading
v = ui.load_view()
v.name = "Calories Counter"
v.add_subview(_NameLabel)
v.add_subview(_100CalLabel)
v.add_subview(_customCalLabel)
v.add_subview(_customGramsTextField)
v.add_subview(_customCalResLabel)
v.add_subview(_totalLabel)
v.add_subview(_totalLabelNumber)

v.present("sheet")





	