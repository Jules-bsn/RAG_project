Tuto github 

Pour ajouter un fichier : 
git add nomdufichier

--> il faut bien ajouter le fichier au git sinon on ne pourra comit les changements 

Pour faire un commit pour sauvegarder les modifications localement :
git commit -m "Message du commit"

Pour synchroniser les changements avec github : 
git push

Pour mettre à jour ton dépôt local (si des modifications ont été faites en ligne) : 
git pull

Manage branches :
Branches allow to work without affecting the main code

Create a branch : git branch branchname

Show us all the branches and the one with * is the one who you are : 
Git branch 

To go in a branch created : git checkout <nom_de_branche>
or : git switch <branchname>

Rename a branch : git branch -m <new-branch-name>

To delete a branch : git branch -d <branchname>

To push your branch to the remote repository (e.g., GitHub) for the first time and establish a tracking connection: 
git push -u origin <branchname>

After this, for future pushes, you can simply use : git push

--> To merge a branch into another 
Switch to the branch you want to merge into : git checkout main
Merge the other branch into it: git merge <branchname>

Undo changes in branches : 
To discard uncommitted changes : git restore <filename>
To reset everything to the last commit : git reset --hard