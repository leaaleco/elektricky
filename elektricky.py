import tkinter as tk
import random
from PIL import Image, ImageTk 


######################################    NASTAVENIA   #################################################################################################################

# veľkosť obrazovky, deliteľnosť 3 treba kvôli zakrytiu pozadia
sirka = 1200  
vyska = 780
speed = 100 #ako rýchlo sa hýbe električka. čím nižšie číslo, tým rýchlejšie (používame after())


# listok nastavenia
velkost_jedla = 40
farba_jedla = "black"

# elektricka nastavenia
elektricka_velkost = 40      #musi byt delitelne 20 aby round function fungovala ako má
elektricka_farba = "black"
krok = elektricka_velkost

# spawnpoint
elektricka_start_x = sirka//2
elektricka_start_y = vyska//2


okno = tk.Tk()
pole = tk.Canvas(okno, width=sirka, height=vyska)
pole.pack()

# obrázok elektricky
img = Image.open("elektricka_image.png")
resize_img = img.resize((elektricka_velkost,elektricka_velkost))
elektricka_image = ImageTk.PhotoImage(resize_img) 

# obrázok lístka
img2 = Image.open("jedlo_image.png")
resize_img2 = img2.resize((velkost_jedla,velkost_jedla))
jedlo_image = ImageTk.PhotoImage(resize_img2) 



# zoznam obrázkov
obrazky = ["1.JPG","2.JPG","3.JPG","4.JPG","5.JPG","6.JPG","7.JPG","8.JPG"]
# vyberie jeden
path = obrazky[(random.randint(0,7))]

# nastavenie pozadia
image = Image.open(path)
resize_image = image.resize((sirka, vyska))
bg = ImageTk.PhotoImage(resize_image) 
pole.pack(fill = "both", expand = True) 
pole.create_image( 0, 0, image = bg, anchor = "nw") 


 
#------------------------------------------------------------------------ nastavenie zakrytia pozadia
# premenné, aby sme mohli jednoduchšie meniť veľkosť obrazovky
s1 = 0
s2 = round(sirka/3)
s3 = round((sirka/3)*2)
s4 = sirka

v1 = 0 
v2 = round(vyska/3)
v3 = round((vyska/3)*2)
v4 = vyska

# vytvorenie 9 čiernych blokov, ktoré hráč bude postupne odkrývať
blok1 = pole.create_rectangle(s1,v1,s2,v2,fill = "black")
blok2 = pole.create_rectangle(s1,v2,s2,v3,fill = "black")
blok3 = pole.create_rectangle(s1,v3,s2,v4,fill = "black")
blok4 = pole.create_rectangle(s2,v1,s3,v2,fill = "black")
blok5 = pole.create_rectangle(s2,v2,s3,v3,fill = "black")
blok6 = pole.create_rectangle(s2,v3,s3,v4,fill = "black")
blok7 = pole.create_rectangle(s3,v1,s4,v2,fill = "black")
blok8 = pole.create_rectangle(s3,v2,s4,v3,fill = "black")
blok9 = pole.create_rectangle(s3,v3,s4,v4,fill = "black")


######################################    TRIEDY   #################################################################################################################


# trieda Električka, na vytvorenie električiek a hada z "tiel" električiek

class Elektricka:

    def __init__(self, stred, farba, dieta=None):
        self.kid = dieta

        #center = [x,y]
        self.center = stred   
        self.x = stred[0]
        self.y = stred[1]

        self.x0 = round(self.x-(elektricka_velkost//2))
        self.y0 = round(self.y-(elektricka_velkost//2))
        self.x1 = round(self.x+(elektricka_velkost//2))
        self.y1 = round(self.y+(elektricka_velkost//2))


        self.id = pole.create_rectangle(self.x0,self.y0,self.x1,self.y1,fill = farba, outline = elektricka_farba)  
        self.skin = pole.create_image(round(stred[0]), round(stred[1]), image = elektricka_image)



# trieda Listok = objekt, ktorý sa hráč snaží získať
class Listok:
    def __init__(self,spawnpoint_x,spawnpoint_y):
        self.x0 = spawnpoint_x
        self.y0 = spawnpoint_y
        self.x1 = spawnpoint_x + velkost_jedla
        self.y1 = spawnpoint_y + velkost_jedla

        self.id = pole.create_oval(spawnpoint_x,spawnpoint_y,spawnpoint_x + velkost_jedla, spawnpoint_y + velkost_jedla, outline = "black", fill="black") 
        self.skin = pole.create_image(spawnpoint_x + (velkost_jedla//2),spawnpoint_y + (velkost_jedla//2), image = jedlo_image)




######################################    FUNKCIE   #################################################################################################################

# ----------------------------------------------------------------pomocné/nezaradené


# zaokrúhľuje na desiatky nadol, používame hlavne pri upravovaní pozícií zobrazenia napojených štvorčekov (update_center v sekcii pohyb)
def round(cislo):
    return int(cislo/10)*10


# zistí aktuálne súradnice štvorčeka a vráti list
def get_position(stvorcek):
    pozicia = pole.coords(stvorcek)  
    return pozicia

# odstráni jeden čierny blok blokujúci pozadie a pridá hráčovi bod do skóre
def odstran_blok():
    global score
    if score==9:                         
        return
    bloky = [blok4,blok2,blok9,blok7,blok3,blok1,blok8,blok6,blok5]  #bloky sa pri každom spustení hry odkrývajú v rovnakom poradí, tu sa dá meniť, prípadne nastaviť menenie
    pole.delete(bloky[score])
    score+=1
   
# vráti opačný smer
def oppositeDir(dir):
    if dir=="left":
        return "right"  
    elif dir=="right":
        return "left" 
    elif dir=="up":
        return "down" 
    elif dir=="down":
        return "up" 
    

# prepíše aktuálne súradnice do vlastností stvorceka = typ Električka
def update_center(stvorcek):
    suradnice = get_position(stvorcek.id)
    stvorcek.center = [round(suradnice[0]+(elektricka_velkost//2)),round(suradnice[1]+(elektricka_velkost//2))]
    stvorcek.x0 = round(suradnice[0])
    stvorcek.y0 = round(suradnice[1])
    stvorcek.x1 = round(suradnice[2])
    stvorcek.y1 = round(suradnice[3])

# zavolá odstran_blok a zmaže z obrazovky zjedený lístok, vygeneruje nový, ak hráč ešte nevyhral
def scorujes():
    global v
    odstran_blok()
    pole.delete(v.id)
    pole.delete(v.skin)
    if score!=9:
        v = Listok(random.randint(0,sirka-velkost_jedla),random.randint(0,vyska-velkost_jedla))


# po detekovaní kolízie s lístočkom pripojí ďalšiu električku k telu
def pridaj_elektricku(dir,hlava):      
    # dir = smer, ktorým sa práve električka pohla, aby zjedla lístoček. pridávame na koniec tela na opačnú stranu dir
    # hlava = typ Električka

    # telo električky ukladáme ako lineárny spojový zoznam
    # prechádzame na koniec zoznamu, aby sme mohli pripojiť novú Električku
    while hlava.kid!=None:
        hlava = hlava.kid

    if dir=="up":   #pridám pod seba, lebo sme sa pohli hore, zvyšné analogicky
        new_center = [round(hlava.x),round(hlava.y-elektricka_velkost)]
        hlava.kid = Elektricka(new_center,elektricka_farba)

    if dir=="down":
        new_center = [round(hlava.x),round(hlava.y+elektricka_velkost)]
        hlava.kid = Elektricka(new_center,elektricka_farba)

    if dir=="right":
        new_center = [round(hlava.x-elektricka_velkost),round(hlava.y)]
        hlava.kid = Elektricka(new_center,elektricka_farba)

    if dir=="left":
        new_center = [round(hlava.x+elektricka_velkost),round(hlava.y)]
        hlava.kid = Elektricka(new_center,elektricka_farba)

# mení parameter 
def gameover():
    global GAME_OVER
    GAME_OVER = True

#---------------------------------------------------------- pohyb


# na presun každého štvorčeka električky (okrem prvého)
def move_next_bodypart(stvorcek, suradnice):  
    # stvorcek = typ Električka 
    # suradnice = starý stred predošlého štvorčeka električky, kam sa máme posunúť
   
    # voláme kým sa dostaneme na koniec zoznamu = tela električky
    if stvorcek is not None:
        #uložíme aktuálne súradnice, aby sme vedeli povedať ďalšiemu štvorčeku, kam sa posunúť
        stary_center = stvorcek.center
        stvorcek.center = suradnice

        #posunieme štvorček električku
        pole.moveto(stvorcek.id, round(suradnice[0] - (elektricka_velkost // 2)), round(suradnice[1] - (elektricka_velkost // 2)))
        #posunieme grafiku
        pole.moveto(stvorcek.skin, round(suradnice[0] - (elektricka_velkost // 2)), round(suradnice[1] - (elektricka_velkost // 2)))
        # zavoláme funkciu na ďalší štvorček v poradí
        update_center(stvorcek)
        move_next_bodypart(stvorcek.kid, stary_center)


# overí, či je ťah povolený, True/False
def can_we_move(object,dir):  #co hybeme, kam.   ci je to povolene vrati 
    # object = čím hýbeme, typ Električka 
    # dir = smer, ktorým sa pokúša hráč pohnúť
    
    # ak má električka jediný dielik, môže sa hýbať do každého smeru
    global PREVIOUS_MOVE
    if object.kid == None:
        return True

    if PREVIOUS_MOVE!=oppositeDir(dir):
        return True
    
    else:
        return False



# hlavná herná funkcia, hýbe električkou a na každom kroku volá overovacie funkcie
def move(dir):
    global score
    global v
    global PREVIOUS_MOVE
    global GAME_OVER
    if GAME_OVER!=True and score!=9:
    # či je ťah povolený
        if can_we_move(elektricka,dir):
            if dir == "left":
                x = -krok
                y = 0
            elif dir == "right":
                x = krok
                y = 0
            elif dir == "up":
                x = 0
                y = -krok
            elif dir == "down":
                x = 0
                y = krok 
            

            pole.move(elektricka.id,round(x),round(y))
            pole.move(elektricka.skin,round(x),round(y))


            # kolízia so stenou?  
            if check_wall_collision(elektricka.id):
                gameover()

            # kolízia s jedlom? 
            if check_food_collision(elektricka.id,v):
                pridaj_elektricku(dir,elektricka)
                scorujes()


            #uloží súradnice stredu pre ďalšie štvorčeky
            previous_center = elektricka.center
            update_center(elektricka)
            # pohne telom
            move_next_bodypart(elektricka.kid, previous_center)
            

            # kolízia s telom? môžeme overovať až teraz, keď už sme telo posunuli
            if check_body_collision(elektricka, elektricka.kid):
                gameover()

            # update smeru
            PREVIOUS_MOVE = dir


            # overí prehru
            if GAME_OVER==True:
                
                # vytlačí hráčovi na obrazovku oznam, že prehral
                sign = pole.create_text((sirka//2),(vyska//2), font = ('Comic Sans MS', 60),text = "Prehra", fill = "red")
                textik = pole.create_rectangle(pole.bbox(sign), fill = "black")
                pole.tag_lower(textik,sign)

            # overí výhru
            if score==9:

                # vytlačí hráčovi na obrazovku oznam, že vyhral
                sign2 = pole.create_text((sirka//2),(vyska//2), font = ('Comic Sans MS', 60),text = " Výhra ", fill = "red")
                textik2 = pole.create_rectangle(pole.bbox(sign2), fill = "black")
                pole.tag_lower(textik2,sign2)
        else:
            move(oppositeDir(dir))
    



# tieto smerové funkcie sú viazané na klávesnicu, menia smer a volajú pohybové

def changeLeft(event):
    global DIR
    DIR="left"
    moveLeft()

def changeRight(event):
    global DIR
    DIR="right"
    moveRight()

def changeDown(event):
    global DIR
    DIR="down"
    moveDown()

def changeUp(event):
    global DIR
    DIR="up"
    moveUp()

okno.bind("<a>",changeLeft)
okno.bind("<d>",changeRight)
okno.bind("<s>",changeDown)
okno.bind("<w>",changeUp)



# pohybové

def moveLeft():
    global DIR
    global speed
    if DIR=="left":  # opakovane zavolá funkciu len ak sa dovtedy nezmenil smer
        if GAME_OVER!=True:
            move("left")
            okno.after(speed,moveLeft) 

def moveRight():
    global DIR
    global speed
    if DIR=="right":
        if GAME_OVER!=True:
            move("right")
            okno.after(speed,moveRight) 

def moveDown():
    global DIR
    global speed
    if DIR=="down":
       if GAME_OVER!=True:
            move("down")
            okno.after(speed,moveDown) 

def moveUp():
    global DIR
    global speed
    if DIR=="up":
       if GAME_OVER!=True:
            move("up")
            okno.after(speed,moveUp) 




#---------------------------------------------------------- kolízie

# overuje kolíziu s lístočkom
def check_food_collision(mobile_object,immobile_object):

    # mobile_object   je pohyblivá "hlava", teda prvá časť električky, funkcia dostáva na vstupe už self.id (preto voláme get_position pre súradnice)
    # immobile_object  je lístoček = typ Lístok
    x0 = immobile_object.x0 
    x1 = immobile_object.x1 
    y0 = immobile_object.y0 
    y1 = immobile_object.y1 
    p = get_position(mobile_object)          #p[0]  p[1]  p[2]  p[3]  

    #ak je ľavý horný alebo pravý dolný roh hlavy v lístočku
    if (x0<=p[0]<=x1 and y0<=p[1]<=y1) or (x0<=p[2]<=x1 and y0<=p[3]<=y1): 
        return True   
    
    #ak je pravý horný alebo ľavý dolný roh hlavy v lístočku
    elif (x0<=p[2]<=x1 and y0<=p[1]<=y1) or (x0<=p[0]<=x1 and y0<=p[3]<=y1):  
        return True
    
    #ak hlava prekrýva lístoček zhora alebo zdola
    elif  p[0]<=x0 and p[2]>x1 and ((y0<=p[1]<=y1) or (y0<=p[3]<=y1)):  
        return True
    
    #ak hlava prekrýva lístoček zľava alebo sprava
    elif p[1]<=y0 and p[3]>y1 and ((x0<=p[0]<=x1) or (x0<=p[2]<=x1)):
        return True
    
    #ak hlava prekrýva lístoček úplne
    elif p[0]<=x0 and p[2]>x1 and p[1]<=y0 and p[3]>y1:
        return True
    
    else:
        return False
    
# overuje kolíziu so stenami obrazovky
def check_wall_collision(stvorcek):  # funkcia dostáva na vstupe už self.id (preto voláme get_position pre súradnice)
    p = get_position(stvorcek)
    if p[0]<0 or p[1]<0:
        return True
    if p[2]>sirka or p[3]>vyska:
        return True 
    else:
        return False  


#overuje kolíziu hlavy s jedným štvorčekom tela, používame pri prechádzaní overovania kolízie s celým telom
def check_center_collision(mobile_object,immobile_object):
    # mobile_object  je hlava električky = typ Električka
    # immobile_object  je časť tela električky = typ Električka

    #štvorčeky majú rovnakú veľkosť, aj ich kroky, čiže ak nastane kolízia tak sa budú hlava a časť tela pretínať takmer celé a podmienky môžeme napísať jednoduchšie ako pri lístočkoch
    x,y = mobile_object.center[0],mobile_object.center[1]
    x0,y0,x1,y1 = immobile_object.x0,immobile_object.y0,immobile_object.x1,immobile_object.y1
    if x0<x<x1 and y0<y<y1:
        return True
    else:
        return False
    

# overuje kolíziu hlavy = prvej Električky, so štvorčekmi všetkých napojených štvorčekov = Električiek = "teločastí"
# rekurzívne volá check_center_collision na každú časť tela
def check_body_collision(hlava,telocast):  
    if telocast==None:
        return False
    #update_center(hlava)
    #update_center(telocast)
    if check_center_collision(hlava,telocast):
        return True
    else:
        return check_body_collision(hlava,telocast.kid)


################################################################ exe setup

PREVIOUS_MOVE = None
GAME_OVER = False
DIR = "up"
score = 0
elektricka = Elektricka([round(elektricka_start_x), round(elektricka_start_y)],elektricka_farba)
v = Listok(random.randint(10,sirka-velkost_jedla-10),random.randint(10,vyska-velkost_jedla-10))

# začína hýbať električkou
moveUp()

okno.mainloop()


