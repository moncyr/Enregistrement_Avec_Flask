from flask import Flask, render_template, request, redirect
import sqlite3
from os import*

# Création de la base de données et de la table produits
with sqlite3.connect('Stock.db') as conn:
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produits (
            ID_Code INTEGER PRIMARY KEY AUTOINCREMENT,
            Type_Produit TEXT NOT NULL,
            Categorie TEXT NOT NULL,
            Nom TEXT NOT NULL,
            Marque TEXT,
            Quantite INTEGER
        );
    ''')

# Déploiement du serveur Flask
templates=getcwd() # recuper le repertoire de travail
app = Flask(__name__, template_folder=templates+"\\templates")

# Route principale pour afficher les produits
@app.route('/')
def lire():
    with sqlite3.connect('Stock.db') as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM produits')
        produits = c.fetchall()
        message=1
    return render_template('produits.html', produits=produits)

# Route pour ajouter un produit
@app.route('/add', methods=['POST'])
def ajoute():
    # Récupération des données du formulaire
    Nom = request.form['Nom']
    Categorie = request.form['Categorie']
    Type = request.form['Type']
    Marque = request.form['Marque']
    Quantite = request.form['Quantite']

    message ="La liste a ete mise a jour"
    # Vérification et conversion de la quantité
    
    Quantite = int(Quantite)
    
    with sqlite3.connect('Stock.db') as conn:
        c = conn.cursor()
        # Vérifier si le produit existe déjà (Type, Categorie, Nom, Marque)
        c.execute('''
            SELECT ID_Code, Quantite FROM produits 
            WHERE Type_Produit = ? AND Categorie = ? AND Nom = ? AND Marque = ?
        ''', (Type, Categorie, Nom, Marque))
        produit_existant = c.fetchone() 

        if produit_existant:
            # Si le produit existe, on met à jour la quantité
            nouveau_stock = produit_existant[1] + Quantite
            
            # Si la quantite a enlever est superieure a la quanite presente
            if Quantite <0 and abs(Quantite)> produit_existant[1] :
                nouveau_stock = produit_existant[1]
                
                  
            c.execute('''
                UPDATE produits 
                SET Quantite = ? 
                WHERE ID_Code = ?
            ''', (nouveau_stock, produit_existant[0]))

        else:
            # Sinon, on insère le nouveau produit si la quantite est positive
            if Quantite >0 :
                c.execute('''
                INSERT INTO produits (Type_Produit, Categorie, Nom, Marque, Quantite) 
                VALUES (?, ?, ?, ?, ?)
            ''', (Type, Categorie, Nom, Marque, Quantite))
        conn.commit()

    return redirect('/')

# Lancement de l'application
if __name__ == '__main__':
    app.run(port=5001)
