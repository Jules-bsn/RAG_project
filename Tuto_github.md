# **Tuto GitHub**

## **Ajouter et gérer des fichiers**

- **Pour ajouter un fichier** :  
  ```bash
  git add <nom_du_fichier>
  ```
  ➡️ **Important** : Il faut bien ajouter le fichier à Git sinon il sera impossible de commit les changements.

- **Pour faire un commit** (sauvegarder les modifications localement) :  
  ```bash
  git commit -m "Message du commit"
  ```

- **Pour synchroniser les changements avec GitHub** :  
  ```bash
  git push
  ```

- **Pour mettre à jour ton dépôt local** (si des modifications ont été faites en ligne) :  
  ```bash
  git pull
  ```

---

## **Gestion des branches**
Les branches permettent de travailler sur différentes fonctionnalités sans affecter le code principal.

- **Créer une branche** :  
  ```bash
  git branch <branchname>
  ```

- **Afficher toutes les branches** (la branche avec `*` est celle sur laquelle vous êtes actuellement) :  
  ```bash
  git branch
  ```

- **Aller dans une branche existante** :  
  ```bash
  git checkout <nom_de_branche>
  ```
  OU :  
  ```bash
  git switch <nom_de_branche>
  ```

- **Renommer une branche** :  
  ```bash
  git branch -m <nouveau_nom>
  ```

- **Supprimer une branche** :  
  ```bash
  git branch -d <branchname>
  ```

- **Pousser une branche sur GitHub pour la première fois et établir une connexion** :  
  ```bash
  git push -u origin <branchname>
  ```
  ➡️ Après cela, pour les prochains push :  
  ```bash
  git push
  ```

---

## **Fusion de branches**
- **Changer vers la branche dans laquelle vous voulez fusionner** :  
  ```bash
  git checkout main
  ```

- **Fusionner une autre branche dans la branche actuelle** :  
  ```bash
  git merge <branchname>
  ```

---

## **Annuler des changements**
- **Pour annuler des modifications non commit (working directory)** :  
  ```bash
  git restore <fichier>
  ```

- **Pour réinitialiser tout à l’état du dernier commit** :  
  ```bash
  git reset --hard
  