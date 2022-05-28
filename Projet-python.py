#region lecture

import sys

def Reading(lecture):
  test = "TXTS/" + lecture + ".txt"
  f = open(test,'r')
  message = f.read()
  print(message)
  f.close()

#end region

Inventaire = []

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

  def equip(self, id_weapon):   ## Pour les armes
    if self.equipped_weapon != None:
      print("You unnequip",self.equipped_weapon.name)
      self.desequip(self.equipped_weapon,self.inventory[id_weapon].power)
      self.equipped_weapon = None
    else:
      print("you equip yourself with :", self.inventory[id_weapon].name)
      self.strength += self.inventory[id_weapon].power
      self.equipped_weapon = self.inventory[id_weapon]
    

  def EquipArmure(self,id_armure):   ## Pour les armures
    if self.equipped_armure != None:
      print("You unnequip",self.equipped_armure.name)
      self.desequip(self.equipped_armure,self.inventory[id_armure].defense_bonus)
      self.equipped_armure = None
    else:
      print("You equip yourself with :",self.inventory[id_armure].name)
      self.equipped_armure = self.inventory[id_armure]
      self.defense += self.inventory[id_armure].defense_bonus
  

  def EquipRelique(self,weapon):  ## Pour les amulettes
    if self.equipped_relique != None:
      print("You desequip",self.equipped_relique.name)
      self.desequip(self.equipped_relique)
      self.equipped_relique = None
    self.equipped_relique = self.inventory[weapon]
    self.hp += self.inventory[weapon].hp_bonus


  def desequip(self, weapon,bonus):
    if type(weapon) == Weapon:
      self.strength = self.strength-bonus
    elif type(weapon) == Armor:
      self.defense = self.defense-bonus
    elif type(weapon) == Amulette:  
      self.hp = self.strength-self.inventory[weapon].hp_bonus

class Merchant(Entity):
  def __init__(self,name,money):
    super().__init__(name,150,40,10)
    self.money = money
    self.inventory = []
    self.inventory.append(Item("small healing potion","heal",10,2)) 
    self.inventory.append(Item("healing potion","heal",50,8))
    self.inventory.append(Weapon("iron dagger",10,50,10))
    self.inventory.append(Weapon("iron bow",30,20,10))
    self.inventory.append(Weapon("iron sword",20,5,10))
    self.inventory.append(Amulette("iron amulet",20,10))
    self.inventory.append(Armor("iron chestplate",5,10))
  def buy_item(self,player):
    for i in range(len(self.inventory)):
      print(i,"-",self.inventory[i].name,", cost :",self.inventory[i].price , "$")
    print("choose an item to buy")
    choice = int(input())
    Item = self.inventory[choice]
    if player.money >= Item.price:
      player.money = player.money-Item.price
      self.money = self.money = Item.price
      print("You buy 1", Item.name)
      player.inventory.append(Item)
      self.inventory.remove(Item)
    else:
      print("you don't have enough money")
    print("do you want to keep buying?")
    print("y or n ? ( yes or no )")
    choix = str(input())
    if choix == "y":
     self.buy_item(player)
    else:
      print("You leave the market and walk peacefully")
      pass

class Monster(Entity):
  def __init__(self,monster_type):
    # Monstre basique
    if monster_type == "Sbire IOT":
      super().__init__(monster_type,20,12,10)
      self.inventory.append(Item("small healing potion","heal",10,2))
      self.inventory.append(Weapon("graphic card",10,10,25))

    if monster_type == "Mec de Pepytes":
      super().__init__(monster_type,25,13,15)
      self.inventory.append(Item("small healing potion","heal",10,2))
      self.inventory.append(Weapon("Ynov flyer",10,10,10))

    if monster_type == "B1 informatique":
      super().__init__(monster_type,15,11,12)
      self.inventory.append(Item("small healing potion","heal",10,2))
      self.inventory.append(Weapon("Ynov flye",10,10,10))

    # Boss
    elif monster_type == "Sofiane":
      super().__init__(monster_type,100,15,10)
      self.inventory.append(Item("healing potion","heal",50,5))


    elif monster_type == "Guillaume":
      super().__init__(monster_type,50,15,20)
      self.inventory.append(Weapon("jaw",15,20,20))
      self.inventory.append(Item("healing potion","heal",50,5))

    elif monster_type == "Antoine":
      super().__init__(monster_type,60,20,15)
       # item ?
      self.inventory.append(Item("healing potion","heal",50,5))


    elif monster_type == "Paul":
      super().__init__(monster_type,65,30,20)
      self.inventory.append((""))
      self.inventory.append(Item("healing potion","heal",50,5))
      
    elif monster_type == "Zouina":
      super().__init__(monster_type,140,20,20)
      self.inventory.append(Item("healing potion","heal",50,5))

    elif monster_type == "Janin":
      super().__init__(monster_type,170,25,30)
      #self.inventory.append(Item("sign-off sheet",""))


'''  def Loot(self):   # Permet de faire un loot aléatoire parmi l'inventaire du monstre
    from random import randint
    return self.inventory[randint(0,len(self.inventory))]
'''
class Player(Entity):  
  def __init__(self,name,type_adventurer):
    self.type_adenturer = type_adventurer
    self.inventory = []
    self.level = 1
    self.xp = 0
    if type_adventurer == "warrior":     ## bcp de vie , peu d'attack
      super().__init__(name,80,15,10)
      self.inventory.append(Weapon("Sword",15,5,1))
      self.inventory.append(Item("healing potion","heal",50,5))
    elif type_adventurer == "assassin":     # faire 3x les crits | moyen vie bcp d'attaque 
      super().__init__(name,60,35,5)
      self.inventory.append(Weapon("Dagger",5,40,1))    
      self.inventory.append(Item("healing potion","heal",50,5))
    elif type_adventurer == "archer":       #  son arme a bcp d'attaque
      super().__init__(name,65,20,7)
      self.inventory.append(Weapon("Arc",20,20,1))
      self.inventory.append(Item("healing potion","heal",50,5))

  def open_inventory(self):
    for i in range(len(self.inventory)):
      print(i,":",self.inventory[i].name)
    print("Which object do you want to use ?")
    print("Press 99 to exit")
    choice = int(input())
    if choice == 99:
      print("Leaving inventory")
      return
    while len(self.inventory)-1 < choice:
      print("You have entered an invalid value, try again")
      self.open_inventory()
    item = self.inventory[choice]
    if type(item) == Weapon:
      self.equip(choice)
    elif type(item) == Armor:
      print("you equip yourself with :", self.inventory[choice].name)
      self.EquipArmure(choice)
    elif type(item) == Amulette:
      print("you equip yourself with :", self.inventory[choice].name)
      self.EquipRelique(choice)
    elif type(item) == Item:
      print("you use :", self.inventory[choice].name)
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
    super().__init__(name, "Def", defense_bonus, price)
    self.defense_bonus = defense_bonus
    
  def use(self,target):
    super().use(target)
    target.defense += self.defense_bonus
  
class Amulette(Item):
  def __init__(self, name, hp_bonus,price):
    super().__init__(name,"hp",hp_bonus,price)
    self.hp_bonus = hp_bonus
  
  def use(self,target):
    super().use(target)
    target.hp += self.hp_bonus

#endregion

#region map

class Map():
  def __init__(self) :
    # 0 = Wall, 1 = Random Fight, 2 = Danger Boss, 3 = Boss, 4 = Chest,
    # 5 = Start, 6 = Stairs, 7 = Merchant, 8 = Door, 9 = Goal
    #Map = 20 x 22
    self.map = [
      [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],#0
      [0,5,1,2,2,2,2,2,1,1,1,1,1,1,4,1,1,1,1,0],#1
      [0,0,0,2,2,2,2,2,1,1,1,4,1,1,1,1,1,1,1,0],#2
      [0,1,1,2,2,3,2,2,1,1,1,1,2,2,2,2,2,1,1,0],#3
      [0,1,1,2,2,2,2,2,1,1,1,1,2,2,2,2,2,1,1,0],#4
      [0,1,1,2,2,2,2,2,1,1,1,1,2,2,3,2,2,1,1,0],#5
      [0,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,1,1,0],#6
      [0,1,4,1,2,2,2,2,2,1,1,1,2,2,2,2,2,1,1,0],#7
      [0,1,1,1,2,2,2,2,2,1,4,1,1,1,1,1,1,1,1,0],#8
      [0,1,1,1,2,2,3,2,2,1,1,1,1,1,1,1,4,1,1,0],#9
      [0,1,1,1,2,2,2,2,2,1,1,1,7,1,2,2,2,2,2,0],#10
      [0,1,1,1,2,2,2,2,2,1,1,1,0,1,2,2,2,2,2,0],#11
      [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6,0,0,0],#12   Stair 1
      [0,0,0,0,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],#13   Stair 2
      [0,4,1,1,7,1,1,1,1,1,8,8,1,1,1,1,0,1,1,0],#14
      [0,1,1,1,1,1,1,1,1,1,8,8,1,1,2,2,0,1,1,0],#15
      [0,1,2,2,2,2,2,1,1,1,8,8,1,1,2,2,0,1,1,0],#16
      [0,1,2,2,2,2,2,1,1,1,8,8,1,4,2,2,3,1,9,0],#17
      [0,1,2,2,3,2,2,1,1,1,8,8,1,1,2,2,0,1,1,0],#18
      [0,1,2,2,2,2,2,1,4,1,8,8,1,1,2,2,0,1,1,0],#19
      [0,1,2,2,2,2,2,1,1,1,8,8,1,1,1,1,0,1,1,0],#20
      [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]#21
    ]
    self.PosX = 1
    self.PosY = 1

  #Movement
  def move_map(self,P,count_boss):
    import msvcrt
    print("You are at the position :",self.PosX,";",self.PosY)
    self.action_map(self.PosX,self.PosY,P,count_boss)
    choice_direction = msvcrt.getch()
    if choice_direction == b"d" or choice_direction == b"D": #Right
      if self.wall_map(self.PosX,self.PosY+1) == False:
        self.PosY+=1
      else:
        print("A wall is blocking the road")
    elif choice_direction == b"q" or choice_direction == b"Q": #Left
      if self.wall_map(self.PosX,self.PosY-1) == False:
        self.PosY-=1
      else:
        print("A wall is blocking the road")
    elif choice_direction == b"z" or choice_direction == b"Z": #Up
      if self.wall_map(self.PosX+1,self.PosY) == False:
        self.PosX+=1
      else:
        print("A wall is blocking the road")
    elif choice_direction == b"s" or choice_direction == b"S": #Down
      if self.wall_map(self.PosX-1,self.PosY) == False:
        self.PosX-=1
      else:
        print("\033[1;35;40m A wall is blocking the road")
    if self.action_map == True:
      return True

  #Action to execute for each case (map)
  def action_map(self,X,Y,P,count_boss):
    if P.hp <= 0:
      print("You have,",P.hp,"hp,you lose the game")
      sys.exit()
      return True   ## Censé quitter le jeu , marche pas   
    from random import randint
    if self.map[X][Y] == 1:
      random_number = randint(1,20)
      if random_number == 1:
        print("\033[1;34;40m You encounter a monster")
        random_number = randint(1,3)
        if random_number == 1:
          monster = "Sbire IOT"
        elif random_number == 2:
          monster = "Mec de Pepytes"
        elif random_number == 3:
          monster = "B1 informatique"
        print("He is level 1")
        Fight(monster, P)
      else:
        print("\033[1;34;40m You walk peacefully")
    if self.map[X][Y] == 2:
      print("\033[1;31;40m You feel something near you")
    if self.map[X][Y] == 3:
      print("\033[1;31;40m You meet a boss")
      if X == 3:
        boss = "Guillaume"
        Reading(boss)
        print("He is level 3")
      elif X == 5:
        boss = "Sofiane"
        Reading(boss)
        print("He is level 5")
      elif X == 9:
        boss = "Antoine"
        Reading(boss)
        print("He is level 5")
      elif X == 18:
        boss = "Paul"
        Reading(boss)
        print("He is level 5")
      elif Y == 16:
        boss = "Zouina"
        print("He is level 7")
      elif Y == 18:
        boss = "Janin"
        print("He is level 10")
      killed = Fight(boss, P)
      if killed == True:
        count_boss += 1
        self.map[X][Y] = 1
        self.map[X-2][Y-2] = 1
        self.map[X-2][Y-1] = 1
        self.map[X-2][Y] = 1
        self.map[X-2][Y+1] = 1
        self.map[X-2][Y+2] = 1
        self.map[X-1][Y-2] = 1
        self.map[X-1][Y-1] = 1
        self.map[X-1][Y] = 1
        self.map[X-1][Y+1] = 1
        self.map[X-1][Y+2] = 1
        self.map[X][Y-2] = 1
        self.map[X][Y-1] = 1
        self.map[X][Y+1] = 1
        self.map[X][Y+2] = 1
        self.map[X+1][Y-2] = 1
        self.map[X+1][Y-1] = 1
        self.map[X+1][Y] = 1
        self.map[X+1][Y+1] = 1
        self.map[X+1][Y+2] = 1
        self.map[X+2][Y-2] = 1
        self.map[X+2][Y-1] = 1
        self.map[X+2][Y] = 1
        self.map[X+2][Y+1] = 1
        self.map[X+2][Y+2] = 1
    if self.map[X][Y] == 4:
      print("\033[1;33;40m You find a chest")
      P.money += 5
      print("You find 5 $")
      self.map[X][Y] == 1
    if self.map[X][Y] == 5:
      print("\033[1;32;40m Here is the start of your story")
    if self.map[X][Y] == 6:
      print("\033[1;32;40m You find stairs")
      print("\033[1;32;40m Do you want to take them ?")
      print("\033[1;32;40m yes ? no ?")
      Answer = str(input())
      if Answer == "yes":
        if self.PosX == 12:
          self.PosX = 13
          self.PosY = 4
        else:
          self.PosX = 12
          self.PosY = 16
        print("You are at the position :",self.PosX,";",self.PosY)
    if self.map[X][Y] == 7:
      print("\033[1;32;40m You encounter a merchant")
      merchant = Merchant("johnny",100)
      merchant.buy_item(P)
    if self.map[X][Y] == 8:
      self.door_map(count_boss)
    if self.map[X][Y] == 9:
      print("You finally locate Janin")
      Fight("Janin", P)

  #Check if the player doesn't go in a wall
  def wall_map(self,X,Y):
    if self.map[X][Y] == 0:
      return True
    else:
      return False

  #Unlock the last boss
  def door_map(self, count_boss):
    if count_boss >= 4:
        print("You killed the 4 bosses, now you can open the door")
        return False
    else:
      print("The door seems locked")
      self.PosY-=1
      print("You are at the position :",self.PosX,";",self.PosY)
      return True

#endregion

#region fight

class Attack:
  def __init__(self,name,dmg,crit_chance) -> None:
    self.name = name
    self.dmg = dmg
    self.crit_chance = crit_chance

  def calculate_damage(self, Atq,entity):
    Atq = Attack("Playerattack",entity.strength,entity.critical_chance)
    from random import randint
    R = randint(0,100)
    if R < entity.critical_chance:
      if type(entity) == Player and self.type_adventurer == "Assassin":
        print("critical hit ! 3x damage because you are an assassin")
        return entity.strength *3
      print("critical hit ! 2x damage ")
      return entity.strength *2
    print("No critical hit")
    return entity.strength

def Fight(monster_name, P):
  monster = Monster(monster_name)
  print("You encounter ", monster_name)
  while monster.hp > 0 or P.hp > 0:
    print("")
    print( monster.name," have ", monster.hp,"hp",monster.strength,"strength and",monster.defense,"defense")
    print("You have ", P.hp,"hp",P.strength,"strength and",P.defense,"defense,what do you want to do ?")
    print("You can :")
    print("0 - attack")
    print("1 - Run away and loose 10hp")
    print("2 - Open inventory")
    choose = input()
    if choose == "0":
      player_attack(monster,P)
      if monster.hp <= 0:
        print("You won the fight")
        if monster_name == "Sbire IOT" or monster_name == "Mec de Pepytes" or monster_name == "B1 informatique":
          print("You earn 5 $")
          P.money += 5
          P.xp += 20
          print("You earn 20 xp")
          if P.xp >= P.level*40:
            P.xp = 0
            P.level += 1
            P.strength += 5
            P.defense += 5
            P.hp += 5
            print("You won a level, you are level : ",P.level)
            print("You earn 5 points in strength, hp and defense")
          return None
        else:
          print("You earn 15 $")
          P.money += 15
          P.level += 1
          P.strength += 5
          P.defense += 5
          P.hp += 5
          print("You won a level, you are level : ",P.level)
          print("You earn 5 points in strength, hp and defense")
          return True
      ennemy_attack(monster,P)
      if P.hp < 0:
        print("You are dead")
        return None
    elif choose == "1":
      P.hp = P.hp-10
      print("You run away and loose 10hp, you now have",P.hp,"hp")
      break
    elif choose == "2":
      P.open_inventory()
    else:
      print("incorrect choose, try again")
      Fight(monster.name,P)

def player_attack(monster,P):
  if P.strength > monster.defense:
    dmg = Attack.calculate_damage(Attack,P.strength,P)           # calculate_damage(P)
    print("you did",dmg-monster.defense,"dmg")
    monster.hp = monster.hp - (dmg-monster.defense)
    if monster.hp > 0:

      print("The monster have still,",monster.hp,"hp")
  else:
    print("Not enougth strength , you didn't even touch him")

def ennemy_attack(monster,Player):
  if monster.strength > Player.defense:
    Player.hp = Player.hp - monster.strength
    print("The monster did",monster.strength,"dmg")
  else:
    print("The monster touch you but you didn't feel anything")

#endregion

#region Gameplay

def affichage_inventaire(P):
  Inventaire = []
  for item in P.inventory:      # Affichage de l'inventaire du joueur
    Inventaire.append(item.name)
    #print(item.name)
  return(Inventaire)

def main():
  import keyboard
  Win = 0
  end = False
  count_boss = 0
  map = Map()

  print("What is your name ? ")
  Nom = str(input())
  print("Choose a class between :'Assassin','Archer' and 'Warrior' ")
  type_adventurer = str(input()).lower()
  if type_adventurer != "assassin" and type_adventurer != "archer" and type_adventurer != "warrior":
    print("Error, no such class")
    exit()
  P = Player(Nom,type_adventurer)
  P.money = 10
  print("Your name is ",Nom, "and you choose the class ", type_adventurer)
  print("")
  print("")
  print("you got :" ,P.hp, "hp, a strength of" ,P.strength , "and", P.defense, "point in defense. You have :", P.money , "$")
  print("you have :")
  affichage_inventaire(P)
  #for item in P.inventory:      # Affichage de l'inventaire du joueur
  #  Inventaire.append(item.name)
    #print(item.name)

  print(Inventaire)
  Tuto = "The keys are : I for see inventory , E for the stats et H to reveal this menu"
  print(Tuto)
  print("")
  print("You can move with z , d , s and q ")
  print("To quit this game press m")
  while P.hp >= 0 or Win != 1:
    if keyboard.is_pressed("i"):
      P.open_inventory()
    if keyboard.is_pressed("h"):
      print(Tuto)
    if keyboard.is_pressed("E"):
      print("you got :" ,P.hp, "hp, a strength of" ,P.strength,",", P.defense, "point in defense and", P.money ,"$")
    if keyboard.is_pressed("m"):
      print("Leaving the game")
      break
 #   if keyboard.read_key() ==":i" or keyboard.read_key() == "I":
 #     print(Inventaire)  # affiche l'inventaire
 #  if keyboard.read_key() =="h" or keyboard.read_key() == "H":
 #     print(Tuto)     # affiche le tuto 
    map.move_map(P,count_boss)
    
    

  
#endregion

main()