# Smart Grid OR – EMI 2026

> **Optimisation d'un Réseau Intelligent de Distribution et de Gestion de l'Énergie pour la Mobilité Électrique**

Application de bureau Python/Tkinter développée dans le cadre du cours de **Recherche Opérationnelle** à l'École Mohammadia d'Ingénieurs (EMI), 2026.

---

## 🎯 Contexte

Le projet modélise un réseau électrique intelligent (smart grid) — composé de sources d'énergie (solaire/éolien), de postes de transformation, de lignes électriques et de stations de recharge VE — sous forme de **graphe pondéré**. Plusieurs algorithmes de RO sont appliqués pour optimiser ce réseau.

## ⚙️ Algorithmes implémentés

### Algorithmes de Graphes
| Algorithme | Objectif |
|---|---|
| Welsh-Powell | Coloration des sommets (nombre chromatique) |
| Kruskal | Arbre couvrant minimal (coût minimum) |
| Dijkstra | Plus court chemin (graphe non orienté) |
| Bellman-Ford | Plus court chemin (graphe orienté, poids négatifs) |
| Ford-Fulkerson | Flux maximal dans un réseau |

### Transport & Programmation Linéaire
| Algorithme | Objectif |
|---|---|
| Nord-Ouest | Solution initiale du problème de transport |
| Moindre Coût | Solution initiale optimisée |
| Simplexe | Programmation linéaire (maximisation/minimisation) |

## 🛠️ Technologies

- Python 3.x
- Tkinter (interface graphique)
- Aucune dépendance externe requise

## 🚀 Lancement

```bash
python ibtissamrharib_roprojetfinal2026.py
```

## 👤 Auteure

**Ibtissam Rharib**  
Encadrante : Dr. EL MKHALET MOUNA  
École Mohammadia d'Ingénieurs – Recherche Opérationnelle 2026
