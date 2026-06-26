# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 11:21:08 2026

@author: exe
"""
import tkinter as tk
from tkinter import ttk, messagebox
import math
import random

# ─────────────────────────────────────────────
#  PALETTE & STYLE CONSTANTS
# ─────────────────────────────────────────────
BG_MAIN   = "#F4F6FB"
BG_CARD   = "#FFFFFF"
ACCENT    = "#0234A5"
ACCENT2   = "#0B2545"
GREEN     = "#1B6B3A"
GOLD      = "#B8860B"
TEAL      = "#0D7377"
CRIMSON   = "#9B1D20"
TEXT_MAIN = "#1B1F23"
TEXT_SUB  = "#6C757D"
BORDER    = "#D0D5E8"

CANVAS_BG    = "#EEF1F8"
EDGE_COLOR   = "#8A96B0"
EDGE_SELECT  = GREEN
EDGE_PATH    = "#E85D04"   # orange-red for Dijkstra shortest path
NODE_DEFAULT = ACCENT2
NODE_COLORS  = [CRIMSON, GREEN, TEAL, GOLD, "#7B2FBE", "#C05621",
                "#1A6E8E", "#5C6BC0", "#AD1457", "#00695C"]
WEIGHT_COLOR = GOLD

def _btn(fg, active_bg=None):
    if active_bg is None:
        active_bg = fg
    return {
        "bg": BG_CARD, "fg": fg,
        "activebackground": active_bg, "activeforeground": BG_CARD,
        "relief": "flat", "bd": 0, "cursor": "hand2",
        "font": ("Segoe UI", 10, "bold"),
        "highlightthickness": 1, "highlightbackground": BORDER,
    }

BTN_BLUE   = _btn(ACCENT)
BTN_GREEN  = _btn(GREEN)
BTN_GOLD   = _btn(GOLD)
BTN_RED    = _btn(CRIMSON)
BTN_TEAL   = _btn(TEAL)


# ─────────────────────────────────────────────
#  ALGORITHM IMPLEMENTATIONS
# ─────────────────────────────────────────────

class GraphAlgorithms:

    @staticmethod
    def welsh_powell(adj_matrix, n):
        degrees = {}
        for i in range(n):
            deg = sum(1 for j in range(n) if adj_matrix[i][j] != 0 and i != j)
            degrees[i] = deg
        sorted_vertices = sorted(range(n), key=lambda x: degrees[x], reverse=True)
        steps = ["STEP 1 – Degrés (ordre décroissant) :"]
        for v in sorted_vertices:
            steps.append(f"   deg(S{v+1}) = {degrees[v]}")
        color_names = ["Rouge", "Vert", "Bleu", "Jaune", "Orange",
                       "Violet", "Rose", "Cyan", "Marron", "Gris"]
        color_map = {}
        num_colors = 0
        steps.append("\nSTEP 2 – Affectation des couleurs :")
        for v in sorted_vertices:
            neighbor_colors = set()
            for u in range(n):
                if adj_matrix[v][u] != 0 and v != u and u in color_map:
                    neighbor_colors.add(color_map[u])
            c = 0
            while c in neighbor_colors:
                c += 1
            color_map[v] = c
            if c >= num_colors:
                num_colors = c + 1
            cname = color_names[c] if c < len(color_names) else f"Couleur{c+1}"
            steps.append(f"   S{v+1} → {cname}  (voisins couleurs : {[color_names[x] for x in neighbor_colors]})")
        chi = num_colors
        steps.append(f"\n→ Nombre chromatique χ(G) = {chi}")
        steps.append(f"  Vérification : {chi} ≤ χ(G) ≤ {n} (ordre du graphe)")
        return color_map, chi, steps

    @staticmethod
    def kruskal(adj_matrix, n):
        edges = []
        for i in range(n):
            for j in range(i+1, n):
                if adj_matrix[i][j] > 0:
                    edges.append((adj_matrix[i][j], i, j))
        edges.sort()
        steps = [f"STEP 1 – Critère de stop : n={n} sommets → n-1={n-1} arêtes\n",
                 "STEP 2 – Sélection des arêtes (sans cycle) :\n"]
        parent = list(range(n))
        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x
        def union(a, b):
            ra, rb = find(a), find(b)
            if ra == rb:
                return False
            parent[ra] = rb
            return True
        selected = []
        total_cost = 0
        for w, i, j in edges:
            if union(i, j):
                selected.append((w, i, j))
                total_cost += w
                steps.append(f"   ✓ S{i+1}–S{j+1}  coût={w}")
                if len(selected) == n - 1:
                    break
            else:
                steps.append(f"   ✗ S{i+1}–S{j+1}  coût={w}  → cycle ignoré")
        steps.append(f"\nSTEP 3 – Calcul du coût total :")
        detail = " + ".join(f"{w}" for w, _, _ in selected)
        steps.append(f"   Coût = {detail} = {total_cost}")
        return selected, total_cost, steps

    @staticmethod
    def dijkstra(adj_matrix, n, source):
        INF = float('inf')
        dist = [INF] * n
        pred = [-1] * n
        visited = [False] * n
        dist[source] = 0
        steps = [f"Point de départ : S{source+1}",
                 f"Critère de stop : {n} sommets = {n} itérations\n"]
        for iteration in range(n):
            u = -1
            for v in range(n):
                if not visited[v] and (u == -1 or dist[v] < dist[u]):
                    u = v
            if dist[u] == INF:
                break
            visited[u] = True
            steps.append(f"Itération {iteration+1} – Sommet dominant : S{u+1}")
            for v in range(n):
                if not visited[v] and adj_matrix[u][v] > 0:
                    new_dist = dist[u] + adj_matrix[u][v]
                    steps.append(f"   S{v+1} : ({dist[u]:.0f} + {adj_matrix[u][v]}) = {new_dist:.0f} · S{u+1}")
                    if new_dist < dist[v]:
                        dist[v] = new_dist
                        pred[v] = u
        steps.append("\n── Calcul des distances ──")
        for v in range(n):
            if v == source:
                continue
            path, cur, seen = [], v, set()
            while cur != -1 and cur not in seen:
                seen.add(cur)
                path.append(f"S{cur+1}")
                cur = pred[cur]
            path.reverse()
            d = dist[v] if dist[v] != INF else "∞"
            steps.append(f"   S{source+1}→S{v+1} : {' → '.join(path)}  =  {d} km")
        return dist, pred, steps

    @staticmethod
    def bellman_ford(adj_matrix, n, source):
        INF = float('inf')
        dist = [INF] * n
        pred = [-1] * n
        dist[source] = 0
        steps = [f"Point de départ : S{source+1}",
                 f"Critère de stop : n={n} → n-1={n-1} itérations\n"]
        prev_dist = list(dist)
        stable_count = 0
        for it in range(n - 1):
            updated = False
            for u in range(n):
                for v in range(n):
                    if adj_matrix[u][v] > 0 and dist[u] != INF:
                        new_d = dist[u] + adj_matrix[u][v]
                        if new_d < dist[v]:
                            dist[v] = new_d
                            pred[v] = u
                            updated = True
            steps.append(f"Itération {it+2} :")
            for v in range(n):
                if v == source:
                    continue
                if dist[v] != INF and pred[v] != -1:
                    steps.append(f"   d(S{v+1}) = d(S{pred[v]+1}) + {adj_matrix[pred[v]][v]}"
                                 f" = {dist[pred[v]]:.0f} + {adj_matrix[pred[v]][v]} = {dist[v]:.0f}")
                elif dist[v] == INF:
                    steps.append(f"   d(S{v+1}) = +∞")
            if dist == prev_dist:
                stable_count += 1
                if stable_count >= 2:
                    steps.append(f"\n⚡ Convergence détectée → arrêt anticipé.")
                    break
            else:
                stable_count = 0
            prev_dist = list(dist)
        steps.append("\n── Calcul des distances ──")
        for v in range(n):
            if v == source:
                continue
            path, cur, seen = [], v, set()
            while cur != -1 and cur not in seen:
                seen.add(cur)
                path.append(f"S{cur+1}")
                cur = pred[cur]
            path.reverse()
            d = dist[v] if dist[v] != INF else "∞"
            steps.append(f"   S{source+1}→S{v+1} : {' → '.join(path)}  =  {d}")
        return dist, pred, steps

    @staticmethod
    def ford_fulkerson(capacity, n, source, sink):
        import copy
        residual = copy.deepcopy(capacity)
        max_flow = 0
        steps = [f"Source : S{source+1}   Puits : S{sink+1}\n"]
        path_num = 0
        while True:
            parent = [-1] * n
            visited = [False] * n
            visited[source] = True
            queue = [source]
            found = False
            while queue and not found:
                u = queue.pop(0)
                for v in range(n):
                    if not visited[v] and residual[u][v] > 0:
                        visited[v] = True
                        parent[v] = u
                        if v == sink:
                            found = True
                            break
                        queue.append(v)
            if not found:
                break
            path_flow = float('inf')
            v = sink
            path = []
            while v != source:
                u = parent[v]
                path.append(v)
                path_flow = min(path_flow, residual[u][v])
                v = u
            path.append(source)
            path.reverse()
            path_num += 1
            path_str = " → ".join(f"S{x+1}" for x in path)
            steps.append(f"Chemin augmentant {path_num} : {path_str}  (flux = {path_flow})")
            v = sink
            while v != source:
                u = parent[v]
                residual[u][v] -= path_flow
                residual[v][u] += path_flow
                v = u
            max_flow += path_flow
        steps.append(f"\n→ Flux maximal = {max_flow}")
        return max_flow, residual, steps


class TransportAlgorithms:

    @staticmethod
    def nord_ouest(supply, demand, costs):
        m, n_d = len(supply), len(demand)
        alloc = [[0]*n_d for _ in range(m)]
        sup = list(supply)
        dem = list(demand)
        steps = [f"Total offre = {sum(supply)}   Total demande = {sum(demand)}\n",
                 "Attribution coin Nord-Ouest :\n"]
        i, j = 0, 0
        while i < m and j < n_d:
            qty = min(sup[i], dem[j])
            alloc[i][j] = qty
            steps.append(f"   Usine {i+1} → Magasin {j+1} : {qty}  "
                         f"(offre restante={sup[i]-qty}, demande restante={dem[j]-qty})")
            sup[i] -= qty
            dem[j] -= qty
            if sup[i] == 0 and i < m-1:
                i += 1
            elif dem[j] == 0 and j < n_d-1:
                j += 1
            else:
                i += 1
                j += 1
        cost = sum(alloc[i][j]*costs[i][j] for i in range(m) for j in range(n_d))
        steps.append(f"\nCoût solution Nord-Ouest = {cost}")
        steps.append("\nTableau d'allocation :")
        for i in range(m):
            row = [alloc[i][j] for j in range(n_d)]
            steps.append(f"   Usine {i+1} : {row}")
        return alloc, cost, steps

    @staticmethod
    def moindre_cout(supply, demand, costs):
        m, n_d = len(supply), len(demand)
        alloc = [[0]*n_d for _ in range(m)]
        sup = list(supply)
        dem = list(demand)
        steps = ["Méthode du Moindre Coût :\n"]
        assigned_rows = set()
        assigned_cols = set()
        while True:
            best, best_cost = None, float('inf')
            for i in range(m):
                for j in range(n_d):
                    if i not in assigned_rows and j not in assigned_cols:
                        if sup[i] > 0 and dem[j] > 0 and costs[i][j] < best_cost:
                            best_cost = costs[i][j]
                            best = (i, j)
            if best is None:
                break
            i, j = best
            qty = min(sup[i], dem[j])
            alloc[i][j] = qty
            sup[i] -= qty
            dem[j] -= qty
            steps.append(f"   Coût min={best_cost} → Usine {i+1} → Magasin {j+1} : {qty}")
            if sup[i] == 0:
                assigned_rows.add(i)
            if dem[j] == 0:
                assigned_cols.add(j)
            if len(assigned_rows) == m or len(assigned_cols) == n_d:
                break
        cost = sum(alloc[i][j]*costs[i][j] for i in range(m) for j in range(n_d))
        steps.append(f"\nCoût solution Moindre Coût = {cost}")
        steps.append("\nTableau d'allocation :")
        for i in range(m):
            row = [alloc[i][j] for j in range(n_d)]
            steps.append(f"   Usine {i+1} : {row}")
        return alloc, cost, steps

    @staticmethod
    def simplexe(c, A, b, maximize=True):
        n_vars = len(c)
        n_cons = len(b)
        steps = []
        obj_str = " + ".join(f"{c[i]}·x{i+1}" for i in range(n_vars))
        steps.append(f"{'Maximisation' if maximize else 'Minimisation'} : Z = {obj_str}\n")
        steps.append("Contraintes :")
        for i in range(n_cons):
            row_str = " + ".join(f"{A[i][j]}·x{j+1}" for j in range(n_vars))
            steps.append(f"   {row_str} ≤ {b[i]}")
        steps.append("   xi ≥ 0\n")
        obj = list(c) if maximize else [-ci for ci in c]
        ncols = n_vars + n_cons + 1
        nrows = n_cons + 1
        tableau = []
        for i in range(n_cons):
            row = [0.0] * (ncols + 1)
            for j in range(n_vars):
                row[j] = float(A[i][j])
            row[n_vars + i] = 1.0
            row[-1] = float(b[i])
            tableau.append(row)
        z_row = [0.0] * (ncols + 1)
        for j in range(n_vars):
            z_row[j] = -float(obj[j])
        tableau.append(z_row)
        basis = list(range(n_vars, n_vars + n_cons))
        def pivot_col():
            row = tableau[-1]
            mc = min(range(ncols), key=lambda j: row[j])
            return mc if row[mc] < -1e-9 else -1
        def pivot_row(col):
            ratios = [(tableau[i][-1] / tableau[i][col], i)
                      for i in range(n_cons) if tableau[i][col] > 1e-9]
            return min(ratios)[1] if ratios else -1
        for iteration in range(50):
            pc = pivot_col()
            if pc == -1:
                steps.append(f"Itération {iteration} – Critère d'optimalité atteint.\n")
                break
            pr = pivot_row(pc)
            if pr == -1:
                steps.append("Problème non borné.")
                break
            pivot_val = tableau[pr][pc]
            var_in  = f"x{pc+1}" if pc < n_vars else f"s{pc-n_vars+1}"
            var_out = f"x{basis[pr]+1}" if basis[pr] < n_vars else f"s{basis[pr]-n_vars+1}"
            steps.append(f"Itération {iteration+1} – Pivot : entrée={var_in}, "
                         f"sortie={var_out}, valeur pivot={pivot_val:.2f}")
            tableau[pr] = [v / pivot_val for v in tableau[pr]]
            for i in range(nrows):
                if i != pr and abs(tableau[i][pc]) > 1e-9:
                    factor = tableau[i][pc]
                    tableau[i] = [tableau[i][k] - factor * tableau[pr][k]
                                  for k in range(ncols + 1)]
            basis[pr] = pc
        solution = [0.0] * n_vars
        for i, b_var in enumerate(basis):
            if b_var < n_vars:
                solution[b_var] = tableau[i][-1]
        z_val = tableau[-1][-1]
        if not maximize:
            z_val = -z_val
        steps.append("\n── Solution optimale ──")
        for i in range(n_vars):
            steps.append(f"   x{i+1} = {solution[i]:.4f}")
        steps.append(f"   Z* = {z_val:.4f}")
        return solution, z_val, steps


# ─────────────────────────────────────────────
#  RANDOM DATA GENERATORS
# ─────────────────────────────────────────────

def generate_random_graph(n, density_pct, directed=False, weighted=True,
                          min_w=1, max_w=50):
    matrix = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            if directed:
                if random.random() < density_pct / 100:
                    matrix[i][j] = random.randint(min_w, max_w) if weighted else 1
            else:
                if j > i and random.random() < density_pct / 100:
                    w = random.randint(min_w, max_w) if weighted else 1
                    matrix[i][j] = w
                    matrix[j][i] = w
    for i in range(n-1):
        if not any(matrix[i][j] > 0 for j in range(n)):
            w = random.randint(min_w, max_w) if weighted else 1
            matrix[i][i+1] = w
            if not directed:
                matrix[i+1][i] = w
    return matrix


# ─────────────────────────────────────────────
#  CANVAS GRAPH DRAWING
# ─────────────────────────────────────────────

def canvas_graph(parent, matrix, n, color_map=None, selected_edges=None,
                 directed=False, weighted=True, title="Graphe",
                 path_edges=None, path_nodes=None):
    """
    path_edges : set of (i,j) tuples for the shortest-path edges (orange highlight)
    path_nodes : set of vertex indices on the shortest path
    """
    cw, ch = 500, 340
    c = tk.Canvas(parent, width=cw, height=ch, bg=CANVAS_BG,
                  highlightthickness=1, highlightbackground=BORDER)
    c.create_text(cw//2, 16, text=title, fill=ACCENT2,
                  font=("Segoe UI", 11, "bold"))
    if n == 0:
        return c
    cx_c, cy_c = cw // 2, ch // 2 + 10
    radius = min(cw, ch) // 2 - 48
    angles = [2 * math.pi * i / n for i in range(n)]
    pos = [(int(cx_c + radius * math.cos(a - math.pi/2)),
            int(cy_c + radius * math.sin(a - math.pi/2))) for a in angles]

    if path_edges is None:
        path_edges = set()
    if path_nodes is None:
        path_nodes = set()

    drawn = set()
    for i in range(n):
        for j in range(n):
            if matrix[i][j] == 0:
                continue
            if not directed and j <= i:
                continue
            key = (i, j) if directed else (min(i,j), max(i,j))
            if key in drawn:
                continue
            drawn.add(key)

            # Check if this edge is on the shortest path
            on_path = (i, j) in path_edges or (j, i) in path_edges

            is_selected = False
            if selected_edges:
                for item in selected_edges:
                    if len(item) == 3:
                        _, a, b = item
                        if (a == i and b == j) or (not directed and a == j and b == i):
                            is_selected = True
                            break

            if on_path:
                color = EDGE_PATH
                width = 3
            elif is_selected:
                color = EDGE_SELECT
                width = 2
            else:
                color = EDGE_COLOR
                width = 1

            x1, y1 = pos[i]
            x2, y2 = pos[j]
            if directed:
                dx, dy = x2 - x1, y2 - y1
                dist_e = math.hypot(dx, dy)
                if dist_e > 0:
                    r_node = 18
                    rx = dx / dist_e * r_node
                    ry = dy / dist_e * r_node
                    ex, ey = int(x2 - rx), int(y2 - ry)
                else:
                    ex, ey = x2, y2
                c.create_line(x1, y1, ex, ey, fill=color, width=width,
                              arrow=tk.LAST, arrowshape=(10, 13, 4))
            else:
                c.create_line(x1, y1, x2, y2, fill=color, width=width)

            if weighted and matrix[i][j] > 0:
                mid_x = (x1 + x2) // 2
                mid_y = (y1 + y2) // 2
                nx = -(y2 - y1)
                ny = (x2 - x1)
                norm = math.hypot(nx, ny) or 1
                off = 10
                lx = int(mid_x + nx/norm * off)
                ly = int(mid_y + ny/norm * off)
                c.create_text(lx, ly, text=str(matrix[i][j]),
                              fill=WEIGHT_COLOR, font=("Segoe UI", 8, "bold"))

    r_node = 18
    for i, (x, y) in enumerate(pos):
        # Determine node color
        if i in path_nodes and color_map and i in color_map:
            # source/dest override path coloring
            node_color = NODE_COLORS[color_map[i] % len(NODE_COLORS)]
        elif i in path_nodes:
            node_color = EDGE_PATH  # orange for path nodes
        elif color_map and i in color_map:
            node_color = NODE_COLORS[color_map[i] % len(NODE_COLORS)]
        else:
            node_color = NODE_DEFAULT

        outline_color = EDGE_PATH if i in path_nodes else ACCENT
        outline_width = 3 if i in path_nodes else 2
        c.create_oval(x-r_node, y-r_node, x+r_node, y+r_node,
                      fill=node_color, outline=outline_color, width=outline_width)
        c.create_text(x, y, text=f"S{i+1}", fill="white",
                      font=("Segoe UI", 9, "bold"))
    return c


# ─────────────────────────────────────────────
#  UI HELPERS
# ─────────────────────────────────────────────

def styled_btn(parent, text, command, style=BTN_BLUE, width=22, pady=7):
    btn = tk.Button(parent, text=text, command=command,
                    width=width, pady=pady, **style)
    btn.bind("<Enter>", lambda e: btn.config(
        bg=style["activebackground"], fg=style.get("activeforeground", "white")))
    btn.bind("<Leave>", lambda e: btn.config(bg=BG_CARD, fg=style["fg"]))
    return btn


def scrolled_text(parent, **kw):
    frame = tk.Frame(parent, bg=BG_CARD, relief="flat",
                     highlightthickness=1, highlightbackground=BORDER)
    txt = tk.Text(frame, bg=BG_CARD, fg=TEXT_MAIN,
                  font=("Consolas", 10), wrap="word",
                  relief="flat", bd=6, **kw)
    sb = tk.Scrollbar(frame, command=txt.yview, bg=BG_MAIN,
                      troughcolor=BG_MAIN)
    txt.config(yscrollcommand=sb.set)
    sb.pack(side="right", fill="y")
    txt.pack(side="left", fill="both", expand=True)
    return frame, txt


def section_label(parent, text, color=ACCENT):
    tk.Label(parent, text=text, bg=BG_CARD, fg=color,
             font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=12, pady=(6, 1))


# ─────────────────────────────────────────────
#  BASE GRAPH ALGORITHM WINDOW
# ─────────────────────────────────────────────

class GraphAlgoWindow(tk.Toplevel):
    def __init__(self, master, title, directed=False, weighted=True,
                 show_source=False, show_sink=False):
        super().__init__(master)
        self.title(title)
        self.configure(bg=BG_MAIN)
        self.geometry("1100x720")
        self.resizable(True, True)
        self.directed = directed
        self.weighted = weighted
        self.show_source = show_source
        self.show_sink = show_sink
        self._title = title
        self.matrix = []
        self.n = 6
        self._build_ui()

    def _build_ui(self):
        hdr = tk.Frame(self, bg=ACCENT2, pady=10)
        hdr.pack(fill="x")
        tk.Label(hdr, text=self._title, bg=ACCENT2, fg="white",
                 font=("Segoe UI", 13, "bold")).pack(side="left", padx=20)
        tk.Button(hdr, text="✕  Fermer", bg=ACCENT2, fg="#FFAAAA",
                  relief="flat", font=("Segoe UI", 10),
                  activebackground=CRIMSON, activeforeground="white",
                  command=self.destroy).pack(side="right", padx=16)

        body = tk.Frame(self, bg=BG_MAIN)
        body.pack(fill="both", expand=True, padx=12, pady=8)

        left = tk.Frame(body, bg=BG_CARD, width=260,
                        relief="flat", highlightthickness=1,
                        highlightbackground=BORDER)
        left.pack(side="left", fill="y", padx=(0, 10))
        left.pack_propagate(False)
        self._build_controls(left)

        right = tk.Frame(body, bg=BG_MAIN)
        right.pack(side="left", fill="both", expand=True)

        self.canvas_frame = tk.Frame(right, bg=BG_MAIN)
        self.canvas_frame.pack(fill="x")

        tf, self.result_text = scrolled_text(right, height=16)
        tf.pack(fill="both", expand=True, pady=(8, 0))

        self._generate()

    def _build_controls(self, parent):
        tk.Label(parent, text="Paramètres du graphe", bg=BG_CARD, fg=ACCENT2,
                 font=("Segoe UI", 11, "bold")).pack(pady=(12, 4))
        tk.Frame(parent, bg=BORDER, height=1).pack(fill="x", padx=10)

        section_label(parent, "Nombre de sommets (3–20):")
        self.n_var = tk.IntVar(value=6)
        tk.Spinbox(parent, from_=3, to=20, textvariable=self.n_var,
                   bg=BG_MAIN, fg=TEXT_MAIN, font=("Segoe UI", 10),
                   relief="flat", width=8,
                   buttonbackground=BG_MAIN).pack(padx=14, pady=3, anchor="w")

        section_label(parent, "Densité du graphe (10–100%):")
        self.density_var = tk.IntVar(value=45)
        tk.Scale(parent, from_=10, to=100, orient="horizontal",
                 variable=self.density_var, bg=BG_CARD, fg=TEXT_MAIN,
                 troughcolor=BORDER, highlightthickness=0,
                 activebackground=ACCENT,
                 font=("Segoe UI", 8)).pack(fill="x", padx=14, pady=2)

        if self.show_source:
            section_label(parent, "Sommet source (1–n):")
            self.src_var = tk.IntVar(value=1)
            tk.Spinbox(parent, from_=1, to=20, textvariable=self.src_var,
                       bg=BG_MAIN, fg=TEXT_MAIN, font=("Segoe UI", 10),
                       relief="flat", width=8,
                       buttonbackground=BG_MAIN).pack(padx=14, pady=3, anchor="w")

        if self.show_sink:
            section_label(parent, "Sommet d'arrivée (1–n):")
            self.sink_var = tk.IntVar(value=6)
            tk.Spinbox(parent, from_=1, to=20, textvariable=self.sink_var,
                       bg=BG_MAIN, fg=TEXT_MAIN, font=("Segoe UI", 10),
                       relief="flat", width=8,
                       buttonbackground=BG_MAIN).pack(padx=14, pady=3, anchor="w")

        tk.Frame(parent, bg=BORDER, height=1).pack(fill="x", padx=10, pady=8)

        styled_btn(parent, "🎲  Générer graphe aléatoire", self._generate,
                   BTN_GOLD, width=24).pack(padx=14, pady=4)
        styled_btn(parent, "▶  Lancer l'algorithme", self._run,
                   BTN_GREEN, width=24).pack(padx=14, pady=4)

    def _generate(self):
        self.n = self.n_var.get()
        density = self.density_var.get()
        self.matrix = generate_random_graph(
            self.n, density, self.directed, self.weighted)
        if self.show_sink:
            self.sink_var.set(self.n)
        self._draw_graph()

    def _draw_graph(self, color_map=None, selected_edges=None,
                    path_edges=None, path_nodes=None):
        for w in self.canvas_frame.winfo_children():
            w.destroy()
        c = canvas_graph(self.canvas_frame, self.matrix, self.n,
                         color_map, selected_edges,
                         directed=self.directed,
                         weighted=self.weighted,
                         title=self._title,
                         path_edges=path_edges,
                         path_nodes=path_nodes)
        c.pack(pady=4)

    def _write_result(self, lines):
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", "end")
        text = "\n".join(lines) if isinstance(lines, list) else lines
        self.result_text.insert("end", text)
        self.result_text.config(state="disabled")

    def _run(self):
        pass


# ─────────────────────────────────────────────
#  SPECIFIC GRAPH ALGORITHM WINDOWS
# ─────────────────────────────────────────────

class WelshPowellWindow(GraphAlgoWindow):
    def __init__(self, master):
        super().__init__(master, "Welsh-Powell – Coloration des Sommets",
                         directed=False, weighted=False,
                         show_source=False, show_sink=False)

    def _run(self):
        if self.n < 1:
            return
        color_map, chi, steps = GraphAlgorithms.welsh_powell(self.matrix, self.n)
        self._draw_graph(color_map=color_map)
        self._write_result(steps)


class KruskalWindow(GraphAlgoWindow):
    def __init__(self, master):
        super().__init__(master, "Kruskal – Arbre Couvrant Minimal",
                         directed=False, weighted=True,
                         show_source=False, show_sink=False)

    def _run(self):
        selected, cost, steps = GraphAlgorithms.kruskal(self.matrix, self.n)
        self._draw_graph(selected_edges=selected)
        self._write_result(steps)


class DijkstraWindow(GraphAlgoWindow):
    def __init__(self, master):
        super().__init__(master, "Dijkstra – Plus Court Chemin (G.N.O)",
                         directed=False, weighted=True,
                         show_source=True, show_sink=True)

    def _run(self):
        src  = min(self.src_var.get()  - 1, self.n - 1)
        dest = min(self.sink_var.get() - 1, self.n - 1)

        # Clamp and avoid src == dest
        if src == dest:
            dest = (src + 1) % self.n
            self.sink_var.set(dest + 1)

        dist, pred, steps = GraphAlgorithms.dijkstra(self.matrix, self.n, src)

        # Reconstruct shortest path from src to dest
        INF = float('inf')
        path_edges = set()
        path_nodes = set()

        if dist[dest] != INF:
            cur = dest
            seen = set()
            while cur != -1 and cur not in seen:
                seen.add(cur)
                path_nodes.add(cur)
                p = pred[cur]
                if p != -1:
                    path_edges.add((min(p, cur), max(p, cur)))
                cur = p

        # Add annotation about the highlighted path
        steps.append(f"\n── Chemin mis en évidence (orange) ──")
        if dist[dest] != INF:
            # Rebuild ordered path for display
            ordered = []
            cur, seen = dest, set()
            while cur != -1 and cur not in seen:
                seen.add(cur)
                ordered.append(f"S{cur+1}")
                cur = pred[cur]
            ordered.reverse()
            steps.append(f"   S{src+1} → S{dest+1} : {' → '.join(ordered)}  =  {dist[dest]:.0f} km")
        else:
            steps.append(f"   Aucun chemin entre S{src+1} et S{dest+1}.")

        # color_map: source = index 0 (CRIMSON), dest = index 2 (TEAL)
        color_map = {src: 0, dest: 2}

        self._draw_graph(color_map=color_map,
                         path_edges=path_edges,
                         path_nodes=path_nodes)
        self._write_result(steps)


class BellmanFordWindow(GraphAlgoWindow):
    def __init__(self, master):
        super().__init__(master, "Bellman-Ford – Plus Court Chemin (G.O)",
                         directed=True, weighted=True,
                         show_source=True, show_sink=True)

    def _run(self):
        src  = min(self.src_var.get()  - 1, self.n - 1)
        dest = min(self.sink_var.get() - 1, self.n - 1)

        if src == dest:
            dest = (src + 1) % self.n
            self.sink_var.set(dest + 1)

        dist, pred, steps = GraphAlgorithms.bellman_ford(self.matrix, self.n, src)

        # Reconstruct shortest path from src to dest
        INF = float('inf')
        path_edges = set()
        path_nodes = set()

        if dist[dest] != INF:
            cur = dest
            seen = set()
            while cur != -1 and cur not in seen:
                seen.add(cur)
                path_nodes.add(cur)
                p = pred[cur]
                if p != -1:
                    # Directed: keep edge as (p, cur) — order matters for arrows
                    path_edges.add((p, cur))
                cur = p

        # Add annotation about the highlighted path
        steps.append(f"\n── Chemin mis en évidence (orange) ──")
        if dist[dest] != INF:
            ordered = []
            cur, seen = dest, set()
            while cur != -1 and cur not in seen:
                seen.add(cur)
                ordered.append(f"S{cur+1}")
                cur = pred[cur]
            ordered.reverse()
            steps.append(f"   S{src+1} → S{dest+1} : {' → '.join(ordered)}  =  {dist[dest]:.0f}")
        else:
            steps.append(f"   Aucun chemin entre S{src+1} et S{dest+1}.")

        # source = CRIMSON (0), dest = TEAL (2)
        color_map = {src: 0, dest: 2}

        self._draw_graph(color_map=color_map,
                         path_edges=path_edges,
                         path_nodes=path_nodes)
        self._write_result(steps)


class FordFulkersonWindow(GraphAlgoWindow):
    def __init__(self, master):
        super().__init__(master, "Ford-Fulkerson – Flux Maximal",
                         directed=True, weighted=True,
                         show_source=True, show_sink=True)

    def _run(self):
        src  = min(self.src_var.get()  - 1, self.n - 1)
        sink = min(self.sink_var.get() - 1, self.n - 1)
        if src == sink:
            sink = (src + 1) % self.n
        flow, residual, steps = GraphAlgorithms.ford_fulkerson(
            self.matrix, self.n, src, sink)
        color_map = {src: 0, sink: 2}
        self._draw_graph(color_map=color_map)
        self._write_result(steps)


# ─────────────────────────────────────────────
#  TRANSPORT DATA ENTRY WIDGET
# ─────────────────────────────────────────────

class TransportDataEntry(tk.Frame):
    def __init__(self, parent, m, n_d):
        super().__init__(parent, bg=BG_CARD)
        self.m = m
        self.n_d = n_d
        self._build(m, n_d)

    def _build(self, m, n_d):
        for w in self.winfo_children():
            w.destroy()

        self.cost_vars = [[tk.StringVar(value=str(random.randint(1, 10)))
                           for _ in range(n_d)] for _ in range(m)]
        self.supply_vars = [tk.StringVar(value=str(random.randint(50, 200)))
                            for _ in range(m)]
        self.demand_vars = [tk.StringVar(value=str(random.randint(50, 150)))
                            for _ in range(n_d)]

        entry_kw = dict(width=7, font=("Consolas", 10), relief="flat",
                        bg=BG_MAIN, fg=TEXT_MAIN, justify="center",
                        highlightthickness=1, highlightbackground=BORDER)
        hdr_kw = dict(bg=ACCENT2, fg="white", font=("Segoe UI", 9, "bold"),
                      padx=6, pady=4)

        tk.Label(self, text="Usines \\ Magasins", **hdr_kw).grid(
            row=0, column=0, sticky="nsew", padx=1, pady=1)
        for j in range(n_d):
            tk.Label(self, text=f"M{j+1}", **hdr_kw).grid(
                row=0, column=j+1, sticky="nsew", padx=1, pady=1)
        tk.Label(self, text="Offre", **hdr_kw).grid(
            row=0, column=n_d+1, sticky="nsew", padx=1, pady=1)

        row_kw = dict(bg=BG_CARD, fg=ACCENT2, font=("Segoe UI", 9, "bold"),
                      padx=6, pady=4, width=12)
        for i in range(m):
            tk.Label(self, text=f"Usine {i+1}", **row_kw).grid(
                row=i+1, column=0, sticky="nsew", padx=1, pady=1)
            for j in range(n_d):
                tk.Entry(self, textvariable=self.cost_vars[i][j], **entry_kw).grid(
                    row=i+1, column=j+1, padx=1, pady=1)
            tk.Entry(self, textvariable=self.supply_vars[i], **entry_kw).grid(
                row=i+1, column=n_d+1, padx=1, pady=1)

        tk.Label(self, text="Demande", **row_kw).grid(
            row=m+1, column=0, sticky="nsew", padx=1, pady=1)
        for j in range(n_d):
            tk.Entry(self, textvariable=self.demand_vars[j], **entry_kw).grid(
                row=m+1, column=j+1, padx=1, pady=1)
        tk.Label(self, text="", bg=BG_CARD).grid(row=m+1, column=n_d+1)

    def rebuild(self, m, n_d):
        self.m = m
        self.n_d = n_d
        self._build(m, n_d)

    def get_data(self):
        try:
            supply = [int(self.supply_vars[i].get()) for i in range(self.m)]
            demand = [int(self.demand_vars[j].get()) for j in range(self.n_d)]
            costs  = [[int(self.cost_vars[i][j].get())
                       for j in range(self.n_d)] for i in range(self.m)]
        except ValueError:
            raise ValueError("Veuillez entrer uniquement des nombres entiers.")
        if any(s <= 0 for s in supply):
            raise ValueError("L'offre de chaque usine doit être > 0.")
        if any(d <= 0 for d in demand):
            raise ValueError("La demande de chaque magasin doit être > 0.")
        if sum(supply) != sum(demand):
            raise ValueError(
                f"Offre totale ({sum(supply)}) ≠ Demande totale ({sum(demand)}).\n"
                "Ajustez les valeurs pour équilibrer le problème.")
        return supply, demand, costs

    def randomize(self):
        m, n_d = self.m, self.n_d
        supply = [random.randint(50, 200) for _ in range(m)]
        demand = [random.randint(30, 150) for _ in range(n_d)]
        diff = sum(supply) - sum(demand)
        if diff > 0:
            demand[-1] += diff
        elif diff < 0:
            supply[-1] -= diff
        for i in range(m):
            self.supply_vars[i].set(str(supply[i]))
        for j in range(n_d):
            self.demand_vars[j].set(str(demand[j]))
            for i in range(m):
                self.cost_vars[i][j].set(str(random.randint(1, 10)))


# ─────────────────────────────────────────────
#  BASE TRANSPORT WINDOW
# ─────────────────────────────────────────────

class TransportWindow(tk.Toplevel):
    def __init__(self, master, title):
        super().__init__(master)
        self.title(title)
        self.configure(bg=BG_MAIN)
        self.geometry("980x700")
        self.resizable(True, True)
        self._title = title
        self._build_ui()

    def _build_ui(self):
        hdr = tk.Frame(self, bg=ACCENT2, pady=10)
        hdr.pack(fill="x")
        tk.Label(hdr, text=self._title, bg=ACCENT2, fg="white",
                 font=("Segoe UI", 13, "bold")).pack(side="left", padx=20)
        tk.Button(hdr, text="✕  Fermer", bg=ACCENT2, fg="#FFAAAA",
                  relief="flat", font=("Segoe UI", 10),
                  activebackground=CRIMSON, activeforeground="white",
                  command=self.destroy).pack(side="right", padx=16)

        body = tk.Frame(self, bg=BG_MAIN)
        body.pack(fill="both", expand=True, padx=12, pady=8)

        left = tk.Frame(body, bg=BG_CARD, width=200,
                        relief="flat", highlightthickness=1,
                        highlightbackground=BORDER)
        left.pack(side="left", fill="y", padx=(0, 10))
        left.pack_propagate(False)
        self._build_controls(left)

        right = tk.Frame(body, bg=BG_MAIN)
        right.pack(side="left", fill="both", expand=True)

        table_frame = tk.Frame(right, bg=BG_CARD, relief="flat",
                               highlightthickness=1, highlightbackground=BORDER)
        table_frame.pack(fill="x", pady=(0, 8))

        tk.Label(table_frame,
                 text="Tableau des données (entrez les valeurs) :",
                 bg=BG_CARD, fg=ACCENT2,
                 font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=10, pady=(8, 4))

        self.table_container = tk.Frame(table_frame, bg=BG_CARD)
        self.table_container.pack(padx=10, pady=(0, 10))

        self.m_var = tk.IntVar(value=3)
        self.nd_var = tk.IntVar(value=3)
        self.data_entry = TransportDataEntry(self.table_container, 3, 3)
        self.data_entry.pack()

        tf, self.result_text = scrolled_text(right, height=16)
        tf.pack(fill="both", expand=True)

    def _build_controls(self, parent):
        tk.Label(parent, text="Dimensions", bg=BG_CARD, fg=ACCENT2,
                 font=("Segoe UI", 11, "bold")).pack(pady=(12, 4))
        tk.Frame(parent, bg=BORDER, height=1).pack(fill="x", padx=10)

        section_label(parent, "Nb usines (2–6):")
        self.m_ctrl = tk.IntVar(value=3)
        tk.Spinbox(parent, from_=2, to=6, textvariable=self.m_ctrl,
                   bg=BG_MAIN, fg=TEXT_MAIN, font=("Segoe UI", 10),
                   relief="flat", width=8,
                   buttonbackground=BG_MAIN).pack(padx=14, pady=3, anchor="w")

        section_label(parent, "Nb magasins (2–6):")
        self.nd_ctrl = tk.IntVar(value=3)
        tk.Spinbox(parent, from_=2, to=6, textvariable=self.nd_ctrl,
                   bg=BG_MAIN, fg=TEXT_MAIN, font=("Segoe UI", 10),
                   relief="flat", width=8,
                   buttonbackground=BG_MAIN).pack(padx=14, pady=3, anchor="w")

        tk.Frame(parent, bg=BORDER, height=1).pack(fill="x", padx=10, pady=8)

        styled_btn(parent, "🔄  Redimensionner", self._resize,
                   BTN_TEAL, width=20).pack(padx=10, pady=3)
        styled_btn(parent, "🎲  Données aléatoires", self._randomize,
                   BTN_GOLD, width=20).pack(padx=10, pady=3)

        tk.Frame(parent, bg=BORDER, height=1).pack(fill="x", padx=10, pady=8)

        styled_btn(parent, "▶  Lancer", self._run,
                   BTN_GREEN, width=20).pack(padx=10, pady=3)

        tk.Label(parent,
                 text="ℹ Offre totale\ndoit = Demande\ntotale",
                 bg=BG_CARD, fg=TEXT_SUB,
                 font=("Segoe UI", 8), justify="center").pack(pady=10)

    def _resize(self):
        m = self.m_ctrl.get()
        nd = self.nd_ctrl.get()
        self.data_entry.rebuild(m, nd)

    def _randomize(self):
        m = self.m_ctrl.get()
        nd = self.nd_ctrl.get()
        self.data_entry.rebuild(m, nd)
        self.data_entry.randomize()

    def _write_result(self, lines):
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", "end")
        text = "\n".join(lines) if isinstance(lines, list) else lines
        self.result_text.insert("end", text)
        self.result_text.config(state="disabled")

    def _run(self):
        pass


class NordOuestWindow(TransportWindow):
    def __init__(self, master):
        super().__init__(master, "Nord-Ouest – Solution Initiale de Transport")

    def _run(self):
        try:
            supply, demand, costs = self.data_entry.get_data()
        except ValueError as e:
            messagebox.showerror("Erreur de saisie", str(e), parent=self)
            return
        alloc, cost, steps = TransportAlgorithms.nord_ouest(supply, demand, costs)
        self._write_result(steps)


class MoindreCoutWindow(TransportWindow):
    def __init__(self, master):
        super().__init__(master, "Moindre Coût – Solution Initiale Optimisée")

    def _run(self):
        try:
            supply, demand, costs = self.data_entry.get_data()
        except ValueError as e:
            messagebox.showerror("Erreur de saisie", str(e), parent=self)
            return
        alloc, cost, steps = TransportAlgorithms.moindre_cout(supply, demand, costs)
        self._write_result(steps)


# ─────────────────────────────────────────────
#  SIMPLEX WINDOW
# ─────────────────────────────────────────────

class SimplexeWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Simplexe – Programmation Linéaire")
        self.configure(bg=BG_MAIN)
        self.geometry("1000x700")
        self.resizable(True, True)
        self.n_v = 2
        self.n_c = 2
        self._build()

    def _build(self):
        hdr = tk.Frame(self, bg=ACCENT2, pady=10)
        hdr.pack(fill="x")
        tk.Label(hdr, text="Simplexe – Programmation Linéaire",
                 bg=ACCENT2, fg="white",
                 font=("Segoe UI", 13, "bold")).pack(side="left", padx=20)
        tk.Button(hdr, text="✕  Fermer", bg=ACCENT2, fg="#FFAAAA", relief="flat",
                  activebackground=CRIMSON, activeforeground="white",
                  command=self.destroy).pack(side="right", padx=16)

        body = tk.Frame(self, bg=BG_MAIN)
        body.pack(fill="both", expand=True, padx=12, pady=8)

        left = tk.Frame(body, bg=BG_CARD, width=200,
                        relief="flat", highlightthickness=1,
                        highlightbackground=BORDER)
        left.pack(side="left", fill="y", padx=(0, 10))
        left.pack_propagate(False)
        self._build_left(left)

        right = tk.Frame(body, bg=BG_MAIN)
        right.pack(side="left", fill="both", expand=True)
        self._build_right(right)

    def _build_left(self, parent):
        tk.Label(parent, text="Configuration", bg=BG_CARD, fg=ACCENT2,
                 font=("Segoe UI", 11, "bold")).pack(pady=(12, 4))
        tk.Frame(parent, bg=BORDER, height=1).pack(fill="x", padx=10)

        section_label(parent, "Nb variables (2–5):")
        self.nv_var = tk.IntVar(value=2)
        tk.Spinbox(parent, from_=2, to=5, textvariable=self.nv_var,
                   bg=BG_MAIN, fg=TEXT_MAIN, font=("Segoe UI", 10),
                   relief="flat", width=8,
                   buttonbackground=BG_MAIN).pack(padx=14, pady=3, anchor="w")

        section_label(parent, "Nb contraintes (1–6):")
        self.nc_var = tk.IntVar(value=2)
        tk.Spinbox(parent, from_=1, to=6, textvariable=self.nc_var,
                   bg=BG_MAIN, fg=TEXT_MAIN, font=("Segoe UI", 10),
                   relief="flat", width=8,
                   buttonbackground=BG_MAIN).pack(padx=14, pady=3, anchor="w")

        section_label(parent, "Type d'optimisation:")
        self.mode_var = tk.StringVar(value="Max")
        frame_mode = tk.Frame(parent, bg=BG_CARD)
        frame_mode.pack(padx=14, pady=3, anchor="w")
        for val in ["Max", "Min"]:
            tk.Radiobutton(frame_mode, text=val, variable=self.mode_var, value=val,
                           bg=BG_CARD, fg=TEXT_MAIN,
                           font=("Segoe UI", 10),
                           selectcolor=BG_CARD,
                           activebackground=BG_CARD).pack(side="left", padx=4)

        tk.Frame(parent, bg=BORDER, height=1).pack(fill="x", padx=10, pady=8)

        styled_btn(parent, "🔄  Redimensionner", self._resize,
                   BTN_TEAL, width=20).pack(padx=10, pady=3)
        styled_btn(parent, "🎲  Données aléatoires", self._randomize,
                   BTN_GOLD, width=20).pack(padx=10, pady=3)

        tk.Frame(parent, bg=BORDER, height=1).pack(fill="x", padx=10, pady=8)

        styled_btn(parent, "▶  Lancer le Simplexe", self._run,
                   BTN_GREEN, width=20).pack(padx=10, pady=3)

        tk.Label(parent,
                 text="ℹ Toutes les\ncontraintes sont ≤\navec xi ≥ 0",
                 bg=BG_CARD, fg=TEXT_SUB,
                 font=("Segoe UI", 8), justify="center").pack(pady=10)

    def _build_right(self, parent):
        input_frame = tk.Frame(parent, bg=BG_CARD, relief="flat",
                               highlightthickness=1, highlightbackground=BORDER)
        input_frame.pack(fill="x", pady=(0, 8))

        tk.Label(input_frame,
                 text="Saisie du problème de programmation linéaire",
                 bg=BG_CARD, fg=ACCENT2,
                 font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=10, pady=(8, 4))

        self.input_container = tk.Frame(input_frame, bg=BG_CARD)
        self.input_container.pack(padx=10, pady=(0, 10), fill="x")

        self._build_input_table(2, 2)

        tf, self.txt = scrolled_text(parent, height=18)
        tf.pack(fill="both", expand=True)

    def _build_input_table(self, n_v, n_c):
        for w in self.input_container.winfo_children():
            w.destroy()
        self.n_v = n_v
        self.n_c = n_c

        entry_kw = dict(width=6, font=("Consolas", 10), relief="flat",
                        bg=BG_MAIN, fg=TEXT_MAIN, justify="center",
                        highlightthickness=1, highlightbackground=BORDER)
        lbl_kw = dict(bg=BG_CARD, fg=ACCENT2, font=("Segoe UI", 9, "bold"), padx=5, pady=3)

        obj_frame = tk.Frame(self.input_container, bg=BG_CARD)
        obj_frame.pack(anchor="w", pady=4)
        tk.Label(obj_frame, text="Z =", **lbl_kw).pack(side="left")
        self.c_vars = []
        for j in range(n_v):
            v = tk.StringVar(value=str(random.randint(1, 10)))
            self.c_vars.append(v)
            tk.Entry(obj_frame, textvariable=v, **entry_kw).pack(side="left", padx=2)
            tk.Label(obj_frame, text=f"·x{j+1}" + (" + " if j < n_v-1 else ""),
                     bg=BG_CARD, fg=TEXT_MAIN, font=("Segoe UI", 9)).pack(side="left")

        hdr_row = tk.Frame(self.input_container, bg=BG_CARD)
        hdr_row.pack(anchor="w", pady=(6, 2))
        tk.Label(hdr_row, text="Contraintes :", bg=BG_CARD, fg=TEXT_SUB,
                 font=("Segoe UI", 9, "italic")).pack(side="left")

        self.a_vars = []
        self.b_vars = []
        constraints_frame = tk.Frame(self.input_container, bg=BG_CARD)
        constraints_frame.pack(anchor="w")
        for i in range(n_c):
            row_frame = tk.Frame(constraints_frame, bg=BG_CARD)
            row_frame.pack(anchor="w", pady=2)
            a_row = []
            for j in range(n_v):
                v = tk.StringVar(value=str(random.randint(1, 8)))
                a_row.append(v)
                tk.Entry(row_frame, textvariable=v, **entry_kw).pack(side="left", padx=2)
                tk.Label(row_frame, text=f"·x{j+1}" + (" + " if j < n_v-1 else ""),
                         bg=BG_CARD, fg=TEXT_MAIN, font=("Segoe UI", 9)).pack(side="left")
            tk.Label(row_frame, text=" ≤ ", bg=BG_CARD, fg=CRIMSON,
                     font=("Segoe UI", 10, "bold")).pack(side="left")
            b_v = tk.StringVar(value=str(random.randint(20, 150)))
            self.b_vars.append(b_v)
            tk.Entry(row_frame, textvariable=b_v, **entry_kw).pack(side="left", padx=2)
            self.a_vars.append(a_row)

        tk.Label(self.input_container,
                 text="  et  xi ≥ 0  pour tout i",
                 bg=BG_CARD, fg=TEXT_SUB, font=("Segoe UI", 9, "italic")).pack(anchor="w", pady=2)

    def _resize(self):
        self._build_input_table(self.nv_var.get(), self.nc_var.get())

    def _randomize(self):
        self._build_input_table(self.nv_var.get(), self.nc_var.get())

    def _run(self):
        try:
            c_vec = [float(self.c_vars[j].get()) for j in range(self.n_v)]
            A_mat = [[float(self.a_vars[i][j].get()) for j in range(self.n_v)]
                     for i in range(self.n_c)]
            b_vec = [float(self.b_vars[i].get()) for i in range(self.n_c)]
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer uniquement des nombres.", parent=self)
            return
        if any(bv < 0 for bv in b_vec):
            messagebox.showerror("Erreur", "Les membres droits (b) doivent être ≥ 0.", parent=self)
            return
        maximize = self.mode_var.get() == "Max"
        sol, z, steps = TransportAlgorithms.simplexe(c_vec, A_mat, b_vec, maximize)
        self.txt.config(state="normal")
        self.txt.delete("1.0", "end")
        self.txt.insert("end", "\n".join(steps))
        self.txt.config(state="disabled")


# ─────────────────────────────────────────────
#  SPLASH SCREEN
# ─────────────────────────────────────────────

class SplashWindow(tk.Toplevel):
    def __init__(self, master, on_start):
        super().__init__(master)
        self.title("EMI – Recherche Opérationnelle 2026")
        self.configure(bg=BG_MAIN)
        self.geometry("740x500")
        self.resizable(False, False)
        self.on_start = on_start
        self._build()

    def _build(self):
        outer = tk.Frame(self, bg=BG_MAIN)
        outer.pack(fill="both", expand=True)

        hdr_band = tk.Frame(outer, bg=ACCENT2, pady=14)
        hdr_band.pack(fill="x")
        tk.Label(hdr_band,
                 text="EMI – École Mohammadia d'Ingénieurs",
                 bg=ACCENT2, fg="white",
                 font=("Segoe UI", 13, "bold")).pack()

        card = tk.Frame(outer, bg=BG_CARD, relief="flat",
                        highlightthickness=1, highlightbackground=BORDER)
        card.pack(fill="x", padx=50, pady=20)

        tk.Label(card,
                 text="Optimisation d'un Réseau Intelligent",
                 bg=BG_CARD, fg=ACCENT,
                 font=("Segoe UI", 17, "bold")).pack(pady=(18, 0))
        tk.Label(card,
                 text="de Distribution et de Gestion de l'Énergie",
                 bg=BG_CARD, fg=ACCENT,
                 font=("Segoe UI", 13, "bold")).pack()
        tk.Label(card, text="pour la Mobilité Électrique",
                 bg=BG_CARD, fg=GREEN,
                 font=("Segoe UI", 13, "bold")).pack(pady=(0, 14))

        tk.Frame(card, bg=BORDER, height=1).pack(fill="x", padx=30)

        form = tk.Frame(card, bg=BG_CARD)
        form.pack(pady=12)

        tk.Label(form, text="Étudiante :", bg=BG_CARD, fg=TEXT_MAIN,
                 font=("Segoe UI", 10, "bold")).grid(
            row=0, column=0, padx=12, pady=6, sticky="e")
        tk.Label(form, text="Ibtissam Rharib",
                 bg=BG_CARD, fg=ACCENT,
                 font=("Segoe UI", 11, "bold")).grid(
            row=0, column=1, padx=12, pady=6, sticky="w")

        tk.Label(form, text="Encadrante :", bg=BG_CARD, fg=TEXT_MAIN,
                 font=("Segoe UI", 10, "bold")).grid(
            row=1, column=0, padx=12, pady=6, sticky="e")
        tk.Label(form, text="Dr. EL MKHALET MOUNA",
                 bg=BG_CARD, fg=GOLD,
                 font=("Segoe UI", 10, "bold")).grid(
            row=1, column=1, padx=12, pady=6, sticky="w")

        tk.Frame(card, bg=BORDER, height=1).pack(fill="x", padx=30)

        start_btn = tk.Button(card,
                              text="  ▶   START  –  Lancer l'Application  ",
                              bg=ACCENT, fg="white",
                              font=("Segoe UI", 12, "bold"),
                              relief="flat", pady=10,
                              activebackground=GREEN, activeforeground="white",
                              command=self._start)
        start_btn.pack(pady=16)

        tk.Label(outer, text="Recherche Opérationnelle 2026",
                 bg=BG_MAIN, fg=TEXT_SUB,
                 font=("Segoe UI", 8)).pack(pady=(0, 6))

    def _start(self):
        self.destroy()
        self.on_start("Ibtissam Rharib")


# ─────────────────────────────────────────────
#  MAIN APPLICATION WINDOW
# ─────────────────────────────────────────────

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Smart Grid OR – EMI 2026")
        self.configure(bg=BG_MAIN)
        self.geometry("900x620")
        self.resizable(True, True)
        self.withdraw()
        self._show_splash()

    def _show_splash(self):
        SplashWindow(self, self._launch_main)

    def _launch_main(self, student_name):
        self.student_name = student_name
        self.deiconify()
        self._build_main()

    def _build_main(self):
        hdr = tk.Frame(self, bg=ACCENT2, pady=12)
        hdr.pack(fill="x")
        tk.Label(hdr, text="EMI", bg=ACCENT2, fg="white",
                 font=("Segoe UI", 22, "bold")).pack(side="left", padx=18)
        info = tk.Frame(hdr, bg=ACCENT2)
        info.pack(side="left", padx=8)
        tk.Label(info,
                 text="Optimisation – Réseau Intelligent de Distribution d'Énergie",
                 bg=ACCENT2, fg="white",
                 font=("Segoe UI", 11, "bold")).pack(anchor="w")
        tk.Label(info,
                 text=f"Étudiante : {self.student_name}   |   "
                      "Dr. EL MKHALET MOUNA   |   EMI 2026",
                 bg=ACCENT2, fg="#A0C4F8",
                 font=("Segoe UI", 9)).pack(anchor="w")

        desc_frame = tk.Frame(self, bg=BG_CARD,
                              highlightthickness=1, highlightbackground=BORDER)
        desc_frame.pack(fill="x", padx=20, pady=(14, 6))
        tk.Label(desc_frame,
                 text="Mobilité Électrique – Smart Grid",
                 bg=BG_CARD, fg=GREEN,
                 font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=14, pady=(8, 2))
        tk.Label(desc_frame,
                 text="Réseau intelligent : sources (solaire/éolien), postes de transformation, "
                      "lignes électriques et stations de recharge — représentés sous forme de graphe.",
                 bg=BG_CARD, fg=TEXT_SUB,
                 font=("Segoe UI", 9), justify="left",
                 wraplength=820).pack(anchor="w", padx=14, pady=(0, 8))

        tk.Label(self,
                 text="Recherche Opérationnelle – Sélectionner un algorithme",
                 bg=BG_MAIN, fg=ACCENT2,
                 font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=20, pady=(10, 4))

        groups_frame = tk.Frame(self, bg=BG_MAIN)
        groups_frame.pack(fill="both", expand=True, padx=20, pady=(0, 14))

        g1 = tk.LabelFrame(groups_frame, text="  Algorithmes de Graphes  ",
                           bg=BG_MAIN, fg=ACCENT2,
                           font=("Segoe UI", 10, "bold"),
                           relief="flat",
                           highlightthickness=1, highlightbackground=BORDER)
        g1.pack(side="left", fill="both", expand=True, padx=(0, 8))

        graph_buttons = [
            ("Welsh-Powell\nColoration Sommets",  lambda: WelshPowellWindow(self),  BTN_TEAL),
            ("Kruskal\nArbre Couvrant",            lambda: KruskalWindow(self),       BTN_BLUE),
            ("Dijkstra\nPlus Court Chemin",        lambda: DijkstraWindow(self),      BTN_GREEN),
            ("Bellman-Ford\nGraphe Orienté",       lambda: BellmanFordWindow(self),   BTN_GREEN),
            ("Ford-Fulkerson\nFlux Maximal",       lambda: FordFulkersonWindow(self), BTN_BLUE),
        ]

        for idx, (label, cmd, style) in enumerate(graph_buttons):
            row = idx // 2
            col = idx % 2
            btn = tk.Button(g1, text=label, command=cmd,
                            width=18, height=3, **style,
                            wraplength=140, justify="center")
            btn.grid(row=row, column=col, padx=8, pady=6, sticky="nsew")
            btn.bind("<Enter>", lambda e, b=btn, s=style: b.config(
                bg=s["activebackground"], fg=s.get("activeforeground", "white")))
            btn.bind("<Leave>", lambda e, b=btn, s=style: b.config(
                bg=BG_CARD, fg=s["fg"]))
        for c in range(2):
            g1.columnconfigure(c, weight=1)

        g2 = tk.LabelFrame(groups_frame, text="  Transport & Programmation Linéaire  ",
                           bg=BG_MAIN, fg=GOLD,
                           font=("Segoe UI", 10, "bold"),
                           relief="flat",
                           highlightthickness=1, highlightbackground=BORDER)
        g2.pack(side="left", fill="both", expand=True)

        transport_buttons = [
            ("Nord-Ouest\nSolution Initiale",      lambda: NordOuestWindow(self),     BTN_GOLD),
            ("Moindre Coût\nSolution Optimisée",   lambda: MoindreCoutWindow(self),   BTN_GOLD),
            ("Simplexe\nProgrammation Linéaire",   lambda: SimplexeWindow(self),      BTN_RED),
        ]

        for idx, (label, cmd, style) in enumerate(transport_buttons):
            row = idx // 2
            col = idx % 2
            btn = tk.Button(g2, text=label, command=cmd,
                            width=18, height=3, **style,
                            wraplength=140, justify="center")
            btn.grid(row=row, column=col, padx=8, pady=6, sticky="nsew")
            btn.bind("<Enter>", lambda e, b=btn, s=style: b.config(
                bg=s["activebackground"], fg=s.get("activeforeground", "white")))
            btn.bind("<Leave>", lambda e, b=btn, s=style: b.config(
                bg=BG_CARD, fg=s["fg"]))
        for c in range(2):
            g2.columnconfigure(c, weight=1)


# ─────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
