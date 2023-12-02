import random

# Global
def get_tank():
	return ["D.Va","Orisa","Reinhardt","Roadhog","Sigma","Winston","Wrecking Ball","Zarya","Junker Queen","Ramattra","Mauga","Doomfist"]
def get_dps():
	return ["Ashe","Bastion","Cassidy","Echo","Genji","Hanzo","Junkrat","Mei","Pharah","Reaper","Soldier","Sombra","Symmetra","Torbjörn","Tracer","Widowmaker","Soujorn"]
def get_support():
	return ["Ana","Baptiste","Brigitte","Lúcio","Mercy","Moira","Zenyatta","Kiriko",'Illari','Lifeweaver']

def get_role():
	roles = ["Tank", "DPS", "Support", "Tank+DPS", "Tank+Support", "DPS+Support", "Flex"]
	return random.choice(roles)

def get_any_hero():
	heroes = get_tank()+get_dps()+get_support()
	return random.choice(heroes)

def get_any_support():
	heroes = get_support()
	return random.choice(heroes)

def get_any_dps():
	heroes = get_dps()
	return random.choice(heroes)

def get_any_tank():
	heroes = get_tank()
	return random.choice(heroes)