class Entity:
  def __init__(self,name,hp,strength,defense):
    self.name = name
    self.hp = hp
    self.strength = strength
    self.defense = defense
    self.inventory = []
    self.equipped_weapon = None
    self.equipped_armure = None
    self.equipped_relique = None
    self.critical_chance = 1
    self.money = 0

  def take_damage(self,amount):   # Calcul des dégat, l'attaque doit être supérieur à la défense
    if amount > self.defense:
      amount -= self.defense
      self.hp -= amount 

  def equip(self, id_weapon):
    if self.equipped_weapon != None:
      self.desequip(self.equipped_weapon)

    self.equipped_weapon = self.inventory[id_weapon]
    self.strength += self.inventory[id_weapon].strength_bonus

  def desequip(self, weapon):
    if type(weapon) == Weapon:
      self.strength -= weapon.strength_bonus
    elif type(weapon) == Armor:
      self.defense -= weapon.defense_bonus
    elif type(weapon) == Amulette:
      self.hp -= weapon.hp_bonus

  def EquipArmure(self,id_armure):
    if self.equipped_armure != None:
      self.desequip(self.equipped_armure)
    pass
  
  def EquipRelique(self,weapon):
    pass 
class Monster(Entity):
  def __init__(self,monster_type):
    # Monstre basique 
    if monster_type == "Sbire IOT":
      super().__init__(monster_type,10,2,2)
      self.inventory.append(Item("Petite Potion Soin","heal",10,2))
      self.inventory.append(Weapon("Carte graphique",10,10))

    if monster_type == "Mec de Pepytes":
      super().__init__(monster_type,15,3,5)
      self.inventory.append(Item("Petite Potion Soin","heal",10,2))
      self.inventory.append(Weapon("Prospectus Ynov",10,10,10))

    if monster_type == "Ouin-Ouin B1":
      super().__init__(monster_type,5,1,2)
      self.inventory.append(Item("Petite Potion Soin","heal",10,2))
      self.inventory.append(Weapon("Prospectus Ynov",10,10,10))

    elif monster_type == "":
      pass

    # Boss
    elif monster_type == "Sofiane":
      super().__init__(monster_type,100,20,30)
      self.inventory.append(Item("Potion de soin","heal",50,5))


    elif monster_type == "Guillaume":
      super().__init__(monster_type,40,10,20)
      self.inventory.append(Weapon("Machoire",15,20,20))
      self.inventory.append(Item("Potion de soin","heal",50,5))

    elif monster_type == "Antoine":
      super().__init__(monster_type,50,20,15)
       # item ?
      self.inventory.append(Item("Potion de soin","heal",50,5))


    elif monster_type == "Paul":
      super().__init__(monster_type,60,25,20)
      self.inventory.append((""))
      self.inventory.append(Item("Potion de soin","heal",50,5))
      
    elif monster_type == "Zouina":
      super().__init__(monster_type,140,20,20)
      self.inventory.append(Item("Potion de soin","heal",50,5))

    elif monster_type == "Janin":
      super().__init__(monster_type,170,25,30)
      self.inventory.append(Item("Feuille d'emargement",""))


'''  def Loot(self):   # Permet de faire un loot aléatoire parmi l'inventaire du monstre
    from random import randint
    return self.inventory[randint(0,len(self.inventory))]
'''

class Player(Entity):
  def __init__(self,name,type_adventurer):
    self.type_adenturer = type_adventurer
    if type_adventurer == "Guerrier":
      super().__init__(name,100,10,20)
      self.inventory.append(Weapon("Sword",10,5,1))
      self.inventory.append(Item("Potion de soin","heal",50,5))
    elif type_adventurer == "Assassin":     # faire 2,5x les crits 
      super().__init__(name,50,20,15)
      self.inventory.append(Weapon("Dagger",5,40,1))    
      self.inventory.append(Item("Potion de soin","heal",50,5))
    elif type_adventurer == "Archer":
      super().__init__(name,40,20,15)
      self.inventory.append(Weapon("Arc",20,20,1))
      self.inventory.append(Item("Potion de soin","heal",50,5))

  def open_inventory(self):
    for i in range(len(self.inventory)):
      print(i,":",self.inventory[i].name)
    print("Quel objet voulez vous utiliser ?")
    choice = int(input())
    item = self.inventory[choice]
    if type(item) == Weapon:
      self.equip(choice)
    elif type(item) == Item:
      item.use(self)



class Item:
  def __init__(self,name,effect,power,price):
    self.name = name
    self.effect = effect
    self.power = power
    self.price = price

  def use(self,target):
    if self.effect == "heal":
      target.hp += self.power
    elif self.effect == "Str":
      target.strength += self.power

    elif self.effect == "Equipement":
      pass

class Weapon(Item):
  def __init__(self, name, strength_bonus, critical_chance, price):
    super().__init__(name,"Str",strength_bonus, price)
    self.critical_chance = critical_chance
  
  def use(self,target):
    super().use(target)
    target.critical_chance += self.critical_chance

class Armor(Item):
  def __init__(self, name, defense_bonus, price):
    super().__init__(name,"Def",defense_bonus, price)
    self.defense += defense_bonus
    
  def use(self,target):
    super().use(target)
    target.defense += self.defense
  
class Amulette(Item):
  def __init__(self, name, hp_bonus):
    super().__init__(name,"hp",hp_bonus)
    self.hp += hp_bonus
  
  def use(self,target):
    super().use(target)
    target.defense += self.defense

def Map() :
    import msvcrt
    Map = [
       [0,1,2,1,0,3],
       [0,6,2,1,0,3],
       [0,1,2,1,4,3],
       [0,0,2,1,0,3],
       [2,1,2,1,5,3],
       [0,1,2,1,0,3]
    ] 
    PosX = 1
    PosY = 1
    print(Map[PosX][PosY])
    choice_direction = msvcrt.getch()
    if choice_direction == b"d": #Right
        PosY+=1
    if choice_direction == b"q": #Left
        PosY-=1
    if choice_direction == b"z": #Up
        PosX+=1
    if choice_direction == b"s": #Down
        PosX-=1
    print(Map[PosX][PosY])

Map()