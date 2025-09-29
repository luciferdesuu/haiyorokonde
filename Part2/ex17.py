import random

animals = ['Rat', 'Eel', 'Bear', 'Goat']
adjective = ['Black', 'Red', 'Bastardized', 'Blue']

print("What is your name?")
name = input()

print(f"{name}, your codename is: ", (random.choice(adjective)), (random.choice(animals)))

print(f"Your lucky number is", (random.randint(1, 99)))