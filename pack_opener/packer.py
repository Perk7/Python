import random
import shelve
import sys
import os

# Defenitions of global variables

money = 0
collect_list = []

# Parent class for all cards

class Card:
	def __init__(self, name = 'Player', quickprice = 100, chance = [i for i in range(0,100)]):
		self.chance = chance
		self.name = name
		self.quickprice = quickprice

	def __str__(self):
		return f'''
		###################### 
		90 
		CF 
		ATM 
		RUS 
		        {self.name}      
		   92 PAC      94 DRI 
		   86 SHO      89 DEF 
		   89 PAS      87 PHY 
		###################### 
		'''

	def printForCollection(self):
		return f"{self.name} 90\n\t\t\t\t  "

# Defenitions of cards

Denis = Card('Denis', 320)
Artyom = Card('Artyom', 300)
Dasha = Card('Dasha', 280)

cards = [ Denis, Artyom, Dasha]

# Function of qiut form interface 
	
def wait_of_answer(answer_variant, answer): 
	try:
		os.system('cls')
		eval(answer_variant[answer])
	except KeyError as e:
		print(f'({e.args[0]}) - неверный вариант, введите правильную букву: ')
		answer = input()
		try:
			os.system('cls')
			eval(answer_variant[answer])
			
		except KeyError as e:
			os.system('cls')
			print(f"Нет варианта ответа '{e.args[0]}'")
			sys.exit()

# Collection 

class Collection:

	def __init__(self):
		
		output = ''

		for i in collect_list:
			output += i.printForCollection()

		while(True):
			print(f'''

				  ############################# 

			 	  	Ваша коллекция:
				
				  {output}

				  q - Выйти

				  ############################# 
				  		''')

			answer = input()
			if answer == 'q':
				os.system('cls')
				break
			else:
				wait_of_answer(answer_variant, answer)

	@classmethod
	def collect(cls, Card):
		collect_list.append(Card)

	@classmethod
	def in_list(cls, Card):
		for i in collect_list:
			if Card.name == i.name:
				return True
		return False

	@classmethod
	def return_collect_list(cls):
		return collect_list

	@classmethod
	def change_collect_list(cls, data):
		collect_list = data

# Interface of Packs menu

class Pack_menu:
	def __init__(self):

		answer_variant = {
							'd' : 'Pack_menu.defaultPack()',
							'p' : 'Pack_menu.primaryPack()',
						 }
		while(True):
			print(f'''
			 	  ############################# 

			 	  		Паки:
						      Деньги: {money}
			 	  d - Обычный
			 	  p - Премиум (600)
			 	  q - Выйти

			 	  #############################
				  ''')

			answer = input()
			if answer == 'q':
				os.system('cls')
				break
			else:
				wait_of_answer(answer_variant, answer)

	

	# Default pack
	@classmethod
	def defaultPack(cls):
		os.system('cls')
		print('\t\tОткрываю пак:')
		rand = random.randint(1,100)

		Denis.chance = [i for i in range(0,20)]
		Artyom.chance = [i for i in range(20,60)]
		Dasha.chance = [i for i in range(60,100)]

		global money

		for card in cards:
			if rand in card.chance:
				print(card)
				if Collection.in_list(card):
					money += card.quickprice
				else:
					Collection.collect(card)

	# Primary pack
	@classmethod
	def primaryPack(cls):
		os.system('cls')

		global money

		if money >= 600:
			money -= 600
			print('\t\tОткрываю пак:')
			rand = random.randint(1,100)

			Denis.chance = [i for i in range(0,40)]
			Artyom.chance = [i for i in range(40,70)]
			Dasha.chance = [i for i in range(70,100)]

			for card in cards:
				if rand in card.chance:
					print(card)
					if Collection.in_list(card):
						money += card.quickprice
					else:
						Collection.collect(card)
		else:
			print("\nНе хватает денег")

# Interface of main menu

class Main_menu:
	def __init__(self):

		global money

		data = shelve.open('cache/cache')
		money = data['money']
		Collection.change_collect_list(data['collect_list']) 
		data.close()

		answer_variant = {
							'p' : 'Pack_menu()',
							'c' : 'Collection()',
							'r' : 'Main_menu.clear_cache()',
						 }
		while(True):
			print(f'''
			 	  ############################# 

			 	  		Меню:
						      Деньги: {money}
			 	  p - Паки
			 	  c - Коллекция
			 	  r - Очистить сохранения
			 	  q - Выйти

			 	  #############################
				  ''')

			answer = input()
			if answer == 'q':
				data = shelve.open('cache/cache')
				data['money'] = money
				data['collect_list'] = Collection.return_collect_list()
				data.close()
				os.system('cls')
				break
			else:
				wait_of_answer(answer_variant, answer)

	@classmethod
	def clear_cache(cls):
		global money
		money = 0
		Collection.change_collect_list([])
		data = shelve.open('cache/cache')
		data['money'] = money
		data['collect_list'] = Collection.return_collect_list()
		data.close()

os.system('cls')
Main_menu()