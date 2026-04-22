# Project taskr

Ce projet a été réalisé dans le cadre du module de CLI durant le semestre 8 à Télécom Saint-Étienne. Ce projet est un gestionnaire de tâches en ligne de commande (CLI). Développé en **Python**, il exploite **Typer** afin de garantir des commandes fluides et documentées, ainsi que **Rich** pour offrir un affichage coloré et structuré.

## Requirements
- Python >= 3.10
- rich
- typer

## Installation
pip install -e .

## Usage

* **Ajouter une tâche** : 
  * exemple : `taskr add "Titre de la tâche" --priority high --due 2026-03-25`
* **Lister toutes les tâches** : 
  `taskr list`
* **Filtrer et Trier la liste** :
  * exemples :
    * Filtrer par statut : `taskr list --status done` (ou `todo`)
    * Filtrer par priorité : `taskr list --priority high`
    * Trier par date d'échéance : `taskr list --sort-due`
* **Modifier une tâche existante** : 
  * exemple : `taskr edit <id> --title "Nouveau Titre" --priority low --due 2026-04-01`
* **Marquer une tâche comme terminée** : 
  `taskr done <id>`
* **Supprimer une tâche** : 
  `taskr delete <id>` (demande une confirmation interactive)
* **Afficher les statistiques** : 
  `taskr stats`

## Développement et Tests
Pour vérifier la robustesse de l'application, lancez la suite de tests (5) automatisés :
```bash
pip install pytest
pytest tests/ -v
```

---

*Projet réalisé par Paulin Gasquet*