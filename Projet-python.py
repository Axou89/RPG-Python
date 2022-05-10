#region lecture
def Reading(lecture):
  test = "TXTS/" + lecture + ".txt"
  print(test)
  f = open(test,'r')
  message = f.read()
  print(message)
  f.close()
#end region

#region fight
class Attack:
  def __init__(self,name,dmg,crit_chance) -> None:
    self.name = name
    self.dmg = dmg
    self.crit_chance = crit_chance

  def calculate_damage(self, entity = None):
    from random import randint
    R = randint(0,100)
    if R < self.crit_chance:
      if type(entity) == Player and self.type_adventurer == "Assassin":
        return self.dmg *3
      return self.dmg *2
    return self.dmg

#endregion

#region entity

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

  def equip(self, id_weapon):   ## Pour les armes
    if self.equipped_weapon != None:
      self.desequip(self.equipped_weapon)
    self.equipped_weapon = self.inventory[id_weapon]
    self.strength += self.inventory[id_weapon].strength_bonus


  def EquipArmure(self,id_armure):   ## Pour les armures
    if self.equipped_armure != None:
      self.desequip(self.equipped_armure)
    self.equipped_armure = self.inventory[id_armure]
    self.defense += self.inventory[id_armure].defense_bonus
  

  def EquipRelique(self,weapon):  ## Pour les amulettes
    if self.equipped_relique != None:
      self.desequip(self.equipped_relique)
    self.equipped_relique = self.inventory[weapon]
    self.hp += self.inventory[weapon].hp_bonus


  def desequip(self, weapon):
    if type(weapon) == Weapon:
      self.strength -= weapon.strength_bonus
    elif type(weapon) == Armor:
      self.defense -= weapon.defense_bonus
    elif type(weapon) == Amulette:
      self.hp -= weapon.hp_bonus

class Merchant(Entity):
  def __init__(self,items,name,money):
    super().__init__(name,150,40,10)
    self.money = money
    self.inventory = items
    self.inventory.append(Item("Petite potion de soin","heal",10,2)) 
    self.inventory.append(Item("Moyenne potion de soin","heal",50,8))
    self.inventory.append(Weapon("dague de fer",10,50,10))
    self.inventory.append(Weapon("Arc en fer",30,20,10))
    self.inventory.append(Weapon("Epee en fer",20,5,10))
    self.inventory.append(Amulette("Amulette de fer",20))
    self.inventory.append(Armor("Plastron en fer",5,10))
    
  def buy_item(self,player):
    for i in range(len(self.inventory)):
      print(i,"-",self.inventory[i].name,":",self.inventory[i].price)
    print("pick an item")
    choice = int(input())
    Item = self.inventory[choice]
    if player.money >= Item.price:
      player.money -= Item.price
      self.money += Item.price
      player.inventory.append(Item)
      self.inventory.remove(Item)
    else:
      print("Vous n'avez pas assez d'argent")
    print("Voulez vous continuez d'acheter?")
    print("y or n ? ( yes or no )")
    choix = str(input())
    if choix == "y":
     self.buy_item(player)
    else:
      pass

class Monster(Entity):
  def __init__(self,monster_type):
    # Monstre basique
    self.count_boss = 0
    if monster_type == "Sbire IOT":
      super().__init__(monster_type,10,2,2)
      self.inventory.append(Item("Petite Potion Soin","heal",10,2))
      self.inventory.append(Weapon("Carte graphique",10,10,25))

    if monster_type == "Mec de Pepytes":
      super().__init__(monster_type,15,3,5)
      self.inventory.append(Item("Petite Potion Soin","heal",10,2))
      self.inventory.append(Weapon("Prospectus Ynov",10,10,10))

    if monster_type == "B1 informatique":
      super().__init__(monster_type,5,1,2)
      self.inventory.append(Item("Petite Potion Soin","heal",10,2))
      self.inventory.append(Weapon("Prospectus Ynov",10,10,10))

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
      #self.inventory.append(Item("Feuille d'emargement",""))


'''  def Loot(self):   # Permet de faire un loot aléatoire parmi l'inventaire du monstre
    from random import randint
    return self.inventory[randint(0,len(self.inventory))]
'''

class Player(Entity):  
  def __init__(self,name,type_adventurer):
    self.type_adenturer = type_adventurer
    if type_adventurer == "warrior":     ## bcp de vie , peu d'attack
      super().__init__(name,100,10,20)
      self.inventory.append(Weapon("Sword",10,5,1))
      self.inventory.append(Item("Potion de soin","heal",50,5))
    elif type_adventurer == "assassin":     # faire 3x les crits | moyen vie bcp d'attaque 
      super().__init__(name,50,20,15)
      self.inventory.append(Weapon("Dagger",5,30,1))    
      self.inventory.append(Item("Potion de soin","heal",50,5))
    elif type_adventurer == "archer":       #  son arme a bcp d'attaque
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

    elif type(item) == Armor:
      self.EquipArmure(choice)
    elif type(item) == Amulette:
      self.EquipRelique(choice)
    elif type(item) == Item:
      item.use(self)

#endregion

#region item

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

#endregion

#region map

class Map():
  def __init__(self) :
    # 0 = Wall, 1 = Random Fight, 2 = Danger Boss, 3 = Boss, 4 = Chest,
    # 5 = Start, 6 = Stairs, 7 = Merchant, 8 = Door, 9 = Goal
    #Map = 27 x 27
    self.map = [
      [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],#1
      [0,5,1,2,2,2,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],#2
      [0,0,0,2,2,2,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,4,1,1,1,0],#3
      [0,1,1,2,2,3,2,2,1,1,1,1,1,1,4,1,1,1,1,1,1,1,4,1,1,1,0],#4
      [0,1,1,2,2,2,2,2,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,1,1,0],#5
      [0,1,1,2,2,2,2,2,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,1,1,0],#6
      [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,3,2,2,1,1,0],#7
      [0,1,4,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,1,1,0],#8
      [0,1,1,1,2,2,2,2,2,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,1,1,0],#9
      [0,1,1,1,2,2,2,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],#10
      [0,1,1,1,2,2,3,2,2,1,1,4,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],#11
      [0,1,1,1,2,2,2,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,4,1,1,1,0],#12
      [0,1,1,1,2,2,2,2,2,1,1,1,1,7,1,1,1,1,1,1,2,2,2,2,2,1,0],#13
      [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,1,0],#14
      [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6,0,0,0,0],#15   Stair 1
      [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],#16
      [0,0,0,0,0,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],#17   Stair 2
      [0,1,1,1,1,7,1,1,1,1,1,1,8,8,1,1,1,1,0,1,1,1,1,1,1,1,0],#18
      [0,1,4,1,1,1,1,1,1,1,1,1,8,8,1,1,1,1,0,1,1,1,1,1,1,1,0],#19
      [0,1,1,1,1,1,1,1,1,1,1,1,8,8,1,1,2,2,0,1,1,1,1,1,1,1,0],#20
      [0,1,1,1,2,2,2,2,2,1,1,1,8,8,1,1,2,2,0,1,1,1,1,1,1,1,0],#21
      [0,1,1,1,2,2,2,2,2,1,1,1,8,8,1,4,2,2,3,1,1,1,9,1,1,1,0],#22
      [0,1,1,1,2,2,3,2,2,1,1,1,8,8,1,1,2,2,0,1,1,1,1,1,1,1,0],#23
      [0,1,1,1,2,2,2,2,2,1,4,1,8,8,1,1,2,2,0,1,1,1,1,1,1,1,0],#24
      [0,1,1,1,2,2,2,2,2,1,1,1,8,8,1,1,1,1,0,1,1,1,1,1,1,1,0],#25
      [0,1,1,1,1,1,1,1,1,1,1,1,8,8,1,1,1,1,1,1,1,1,1,1,1,1,0],#26
      [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]#27
    ]
    self.PosX = 1
    self.PosY = 1
    print("You are at the position :",self.PosX,";",self.PosY)

  def move_map(self):
    import msvcrt
    self.action_map(self.PosX,self.PosY)
    choice_direction = msvcrt.getch()
    if choice_direction == b"d": #Right
      if self.wall_map(self.PosX,self.PosY) == False:
        self.PosX+=1
    elif choice_direction == b"q": #Left
      if self.wall_map(self.PosX,self.PosY) == False:
        self.PosX-=1
    elif choice_direction == b"z": #Up
      if self.wall_map(self.PosX,self.PosY) == False:
        self.PosY+=1
    elif choice_direction == b"s": #Down
      if self.wall_map(self.PosX,self.PosY) == False:
        self.PosY-=1

  def action_map(self,X,Y):
    from random import randint
    if self.map[X][Y] == 1:
      random_number = randint(1,20)
      if random_number == 1:
        print("You encounter a monster")
        #Commencer combat
      else:
        print("You walk peacefully")
    if self.map[X][Y] == 2:
      print("You feel something near you")
    if self.map[X][Y] == 3:
      print("You meet a boss")
      #Commencer le combat
    if self.map[X][Y] == 4:
      print("You find a chest")
      #Donne un item
    if self.map[X][Y] == 5:
      print("Here is the start of your story")
    if self.map[X][Y] == 6:
      print("You find stairs")
      print("Do you want to take them ?")
      print("yes ? no ?")
      Answer = str(input())
      if Answer == "yes":
        if self.PosX == 6:
          self.PosX = 23
          self.PosY = 15
        else:
          self.PosX = 6
          self.PosY = 17
    if self.map[X][Y] == 7:
      print("You encounter a merchant")
      Merchant.buy_item()
    if self.map[X][Y] == 8:
      self.door_map()
    if self.map[X][Y] == 9:
      print("You finally locate Janin")
      #Start combat

  def wall_map(self,X,Y):
    if self.map[X][Y] == 0:
      print("A wall is blocking the road")
      return True
    else:
      return False

  def door_map(self):
    if Monster.count_boss == 4:
        print("You killed the 4 bosses, now you can open the door")
        return False
    else:
      print("The door seems locked")
      self.PosX-=1
      return True

#endregion


#region Gameplay
def ennemy_attack():
  pass
def main():
  Win = 0
  map = Map()

  print("What is your name ? ")
  Nom = str(input())
  print("Choose a class between :'Assassin','Archer' and 'Warrior' ")
  type_adventurer = str(input()).lower()
  if type_adventurer != "assassin" and type_adventurer != "archer" and type_adventurer != "warrior":
    print("Error, no such class")
    exit()
  P = Player(Nom,type_adventurer)
  print("Your name is ",Nom, "and you choose the class ", type_adventurer)
  print("")
  print("")
  print("you got :" ,P.hp, "hp, a strength of " ,P.strength , " and", P.defense, "point in defense.")
  print("you have :")
  for item in P.inventory:
    print(item.name)
  while P.hp >= 0 or Win != 1:
    map.move_map()
    

  print("End of the game")
  
#endregion

main()
