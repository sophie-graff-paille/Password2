import string
import json
from tkinter import *
import hashlib

# création d'une fenêtre
fenetre = Tk()
fenetre.title("Gestionnaire de mots de passe")
fenetre.geometry("400x250")

# création d'un widget Label pour le nom d'utilisateur
label_user = Label(fenetre, text="Nom d'utilisateur", font=("Comic Sans MS", 10), bg="green", fg="white")
label_user.pack(pady=10)

# création d'une entrée de texte pour le nom d'utilisateur
champ_user = Entry(fenetre, width=50)
champ_user.pack()

# création d'un widget Label pour le mot de passe
label_mdp = Label(fenetre, text="Mot de passe", font=("Comic Sans MS", 10), bg="green", fg="white")
label_mdp.pack(pady=10)

# création d'une entrée de texte pour le mot de passe
champ_mdp = Entry(fenetre, width=50)
champ_mdp.pack()

# fonction qui récupère les données saisies par l'utilisateur
def recuperer_input():
#mdp = input("Veuillez saisir votre mot de passe: ")
    user = champ_user.get() # récupère le nom d'utilisateur
    mdp = champ_mdp.get() # récupère le mot de passe
    print(user)
    print(mdp)
    verif_mdp(mdp, user) # appelle la fonction qui vérifie si le mot de passe est valide

# fonction qui vérifie si le mot de passe est valide
def verif_mdp(mdp, user):
    # variables définissant les caractères à utiliser
    maj = string.ascii_uppercase # majuscules
    u = 0
    min = string.ascii_lowercase # minuscules
    l = 0
    chiffres = string.digits # chiffres
    d = 0
    special = string.punctuation # caractères spéciaux
    s = 0
    
    if (len(mdp) >= 8): # vérifie si le mot de passe fait au moins 8 caractères
        for i in mdp: 
        # vérifie si le mot de passe contient au moins une majuscule, une minuscule, un chiffre et un caractère spécial
            if (i in maj):
                u += 1
            if (i in min):
                l += 1
            if (i in chiffres):
                d += 1
            if (i in special):
                s += 1
    # si le mot de passe contient une majuscule ou plus, une minuscule ou plus, un chiffre ou plus et un caractère spécial ou plus, alors le mot de passe est valide
    if (u >= 1 and l >= 1 and d >= 1 and s >= 1):
        print("Mot de passe valide")
        hasher(user, mdp) # crypte le mot de passe
        remise_a_zero() # remet à zéro les champs de saisie
        open_popup() # ouvre une fenêtre popup
    else:
        print("Mot de passe invalide")

# fonction qui ouvre une fenêtre popup
def open_popup():
   top= Toplevel(fenetre)
   top.geometry("300x100")
   top.title("Avis")
   Label(top, text= "Vos données sont enregistrées", font=("Comic Sans MS", 10), bg="green", fg="white").pack(pady=10)

# fonction qui remet à zéro les champs de saisie
def remise_a_zero():
    champ_user.delete(0, END) # supprime le texte du champ de saisie du nom d'utilisateur
    champ_mdp.delete(0, END) # supprime le texte du champ de saisie du mot de passe

# fonction qui convertit les données en json
def convert_data_to_json(user, hex_hash): # user = nom d'utilisateur, hex_hash = mot de passe hashé
    try: # essaie de lire le fichier data.json
        with open("data.json", "r", encoding='utf-8') as fichier: # ouvre le fichier data.json en mode lecture
            dic = json.load(fichier) # charge le fichier data.json dans la variable dic
    except: # si le fichier data.json n'existe pas, alors il est créé
        dic = {} # crée un dictionnaire vide
    if user in dic: # si le nom d'utilisateur existe déjà dans le fichier data.json
        if hex_hash not in dic[user]: # si le mot de passe hashé n'existe pas déjà dans le fichier data.json
            dic[user] += [hex_hash] # ajoute le mot de passe hashé dans le fichier data.json
    elif user not in dic: # si le nom d'utilisateur n'existe pas dans le fichier data.json
        dic[user] = [hex_hash] # ajoute le nom d'utilisateur et le mot de passe hashé dans le fichier data.json
    with open("data.json", "w", encoding='utf-8') as fichier: # ouvre le fichier data.json en mode écriture
        json.dump(dic, fichier, indent=2, separators=(',', ': '), ensure_ascii=False) # écrit dle dictionnaire dic dans le fichier data.json

# fonction qui hash le mot de passe
def hasher(user, mdp):
    # J'avais choisi de faire une boucle avant de faire l'interface graphique. J'ai donc laissé le code de la boucle en commentaire
    # pour que vous puissiez voir comment j'avais fait avant l'interface graphique

    # while True: # boucle infinie pour demander le mot de passe tant qu'il n'est pas valide
    #     mdp = input("Veuillez saisir votre mot de passe: ") # demande le mot de passe
    #     verif = verif_mdp() # vérifie si le mot de passe est valide
    #     if verif != "Mot de passe valide": # si le mot de passe n'est pas valide, alors on recommence
    #         print("Mot de passe invalide, veuillez recommencer!")
    #         print(verif)
    #     else:
    hash_mdp = str(mdp) # convertit le mot de passe en chaîne de caractères
    print(mdp, "est un mot de passe valide") # affiche le mot de passe
    hash = hashlib.sha256(hash_mdp.encode()) # hash le mot de passe
    hex_hash = hash.hexdigest() # convertit le hash en chaîne de caractères hexadécimale
    print(hex_hash) # affiche le hash
    convert_data_to_json(user, hex_hash) # ajoute le nom d'utilisateur et le mot de passe hashé dans le fichier data.json
        # break # sort de la boucle infinie

# création du bouton "VALIDER"
valider = PhotoImage(file="check.png")
img_label = Label(image=valider)
bouton_valider = Button(fenetre, image=valider, command=recuperer_input, borderwidth=8)
bouton_valider.pack(pady=20)

fenetre.mainloop()