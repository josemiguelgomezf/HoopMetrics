# hoopmetrics_gui_v5.py
import json
import math
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# -------------------------
# Funciones estadísticas
# -------------------------
def calcular_efg(fg, tp, fga):
    return (fg + 0.5 * tp) / fga if fga > 0 else 0

def calcular_ts(pts, fga, fta):
    intentos = 2 * (fga + 0.44 * fta)
    return pts / intentos if intentos > 0 else 0

def puntos_por_minuto(pts, min_jugados):
    return pts / min_jugados if min_jugados > 0 else 0

def estadistica_por_minuto(valor, min_jugados):
    return valor / min_jugados if min_jugados > 0 else 0

def convertir_minutos_to_float(min_str):
    """Si MIN viene como 'MM:SS' lo convierte a decimal. Si es número, devuelve tal cual."""
    try:
        if isinstance(min_str, (int, float)):
            return float(min_str)
        if ":" in str(min_str):
            m, s = str(min_str).split(":")
            return round(int(m) + int(s)/60.0, 2)
        return float(min_str)
    except Exception:
        return 0.0

# -------------------------
# Cálculo y enriquecimiento
# -------------------------
def calcular_estadisticas():
    global totales
    # Inicialización totales
    totales = {
        "PTS":0,"REB":0,"AST":0,"FG":0,"FGA":0,"3P":0,"FTA":0,"FT":0,"TOV":0,
        "STL":0,"BLK":0,"MIN":0,"OREB":0,"DREB":0,"PTS_CONTRA":0
    }

    # Primero convertir MIN si está en formato HH:MM o MM:SS y calcular totales base
    for jugadora, stats in estadisticas.items():
        # normalizar nombres de campos esperados
        stats["MIN"] = convertir_minutos_to_float(stats.get("MIN", 0))
        for key in ["PTS","REB","AST","FG","FGA","3P","FTA","FT","TOV","STL","BLK","OREB","DREB","PTS_CONTRA"]:
            totales[key] += stats.get(key, 0)

    # Calcular métricas por jugadora (ahora con totales disponibles)
    for jugadora, stats in estadisticas.items():
        fg = stats.get("FG",0)
        tp = stats.get("3P",0)
        fga = stats.get("FGA",0)
        pts = stats.get("PTS",0)
        fta = stats.get("FTA",0)
        reb = stats.get("REB",0)
        ast = stats.get("AST",0)
        stl = stats.get("STL",0)
        blk = stats.get("BLK",0)
        tov = stats.get("TOV",0)
        min_jugados = stats.get("MIN",0)
        dreb = stats.get("DREB",0)
        oreb = stats.get("OREB",0)
        pts_contra = stats.get("PTS_CONTRA",0)

        # métricas básicas
        stats["eFG%"] = round(calcular_efg(fg,tp,fga)*100,2)
        stats["TS%"] = round(calcular_ts(pts,fga,fta)*100,2)
        stats["PPM"] = round(puntos_por_minuto(pts,min_jugados),3)
        stats["REB/MIN"] = round(estadistica_por_minuto(reb,min_jugados),3)
        stats["AST/MIN"] = round(estadistica_por_minuto(ast,min_jugados),3)

        # posesiones estimadas por jugador (aprox): FGA - FG + 0.44*FTA + TOV
        pos_j = fga - fg + 0.44 * fta + tov
        stats["POS"] = round(pos_j,3)
        stats["TOV/POS"] = round(tov / pos_j,3) if pos_j > 0 else 0

        # % de rebotes respecto al total de equipo (off/def)
        stats["%REB_DEF_TEAM"] = round((dreb / totales["DREB"]) * 100,2) if totales["DREB"] > 0 else 0
        stats["%REB_OFF_TEAM"] = round((oreb / totales["OREB"]) * 100,2) if totales["OREB"] > 0 else 0

    # Totales de equipo (después del bucle detallado)
    totales["eFG%"] = round(calcular_efg(totales["FG"],totales["3P"],totales["FGA"])*100,2)
    totales["TS%"] = round(calcular_ts(totales["PTS"],totales["FGA"],totales["FTA"])*100,2)
    posesiones = totales["FGA"] - totales["FG"] + 0.44*totales["FTA"] + totales["TOV"]
    totales["POSESIONES"] = round(posesiones,3)
    totales["PPP"] = round(totales["PTS"]/posesiones,3) if posesiones>0 else 0
    totales["ORTG"] = round(totales["PPP"]*100,3)
    totales["AST/POS"] = round(totales["AST"]/posesiones,3) if posesiones>0 else 0
    totales["REB/POS"] = round(totales["REB"]/posesiones,3) if posesiones>0 else 0
    totales["TOV/POS"] = round(totales["TOV"]/posesiones,3) if posesiones>0 else 0
    totales["%REB_DEF"] = round(totales["DREB"]/totales["REB"]*100,2) if totales["REB"]>0 else 0
    totales["%REB_OFF"] = round(totales["OREB"]/totales["REB"]*100,2) if totales["REB"]>0 else 0
    totales["DRTG"] = round(totales["PTS_CONTRA"]/posesiones*100,3) if posesiones>0 else 0

# -------------------------
# Funciones GUI
# -------------------------
def cargar_datos():
    archivo = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
    if not archivo:
        return
    global estadisticas
    with open(archivo, "r", encoding="utf-8") as f:
        estadisticas = json.load(f)
    calcular_estadisticas()
    mostrar_individuales()
    mostrar_equipo()
    mostrar_seleccion_default()
    actualizar_grafico_seleccionado()

def mostrar_individuales():
    for i in tree.get_children():
        tree.delete(i)
    for jugadora, s in estadisticas.items():
        tree.insert("", "end", values=(
            jugadora, s.get("PTS",0), s.get("REB",0), s.get("AST",0), s.get("STL",0), s.get("BLK",0),
            s.get("TOV",0), s.get("eFG%",0), s.get("TS%",0), s.get("PPM",0), s.get("REB/MIN",0),
            s.get("AST/MIN",0), s.get("OREB",0), s.get("DREB",0), s.get("PTS_CONTRA",0)
        ))

def mostrar_equipo():
    texto = f"""🏀 ESTADÍSTICAS DEL EQUIPO
PTS: {totales['PTS']} | REB: {totales['REB']} | AST: {totales['AST']}
STL: {totales['STL']} | BLK: {totales['BLK']} | TOV: {totales['TOV']}
eFG%: {totales['eFG%']}% | TS%: {totales['TS%']}%
POSESIONES: {totales['POSESIONES']} | PPP: {totales['PPP']} | ORTG: {totales['ORTG']}
AST/POS: {totales['AST/POS']} | REB/POS: {totales['REB/POS']} | TOV/POS: {totales['TOV/POS']}
%REB_DEF Equipo: {totales['%REB_DEF']} | %REB_OFF Equipo: {totales['%REB_OFF']} | DRTG: {totales['DRTG']}
"""
    lbl_equipo.config(text=texto)

# -------------------------
# Gráficos variados
# -------------------------
def limpiar_frame_grafico():
    for widget in frame_grafico.winfo_children():
        widget.destroy()

def ajustar_fig_xticks(ax, labels):
    ax.set_xticks(range(len(labels)))
    # fuente en función del número de labels
    fontsize = 10 if len(labels) <= 8 else (8 if len(labels) <= 16 else 6)
    ax.set_xticklabels(labels, rotation=45, ha="right", fontsize=fontsize)

def mostrar_grafico_pts_reb_ast():
    limpiar_frame_grafico()
    jugadoras = list(estadisticas.keys())
    pts = [s.get("PTS",0) for s in estadisticas.values()]
    reb = [s.get("REB",0) for s in estadisticas.values()]
    ast = [s.get("AST",0) for s in estadisticas.values()]

    ancho = max(8, len(jugadoras) * 0.6)
    fig, ax = plt.subplots(figsize=(ancho, 4))
    ax.bar(range(len(jugadoras)), pts, label="PTS")
    ax.bar(range(len(jugadoras)), reb, bottom=pts, label="REB")
    ax.bar(range(len(jugadoras)), ast, bottom=[i+j for i,j in zip(pts,reb)], label="AST")

    ax.set_ylabel("Conteo")
    ax.set_title("Puntos, Rebotes y Asistencias por Jugadora")
    ax.legend()
    ajustar_fig_xticks(ax, jugadoras)
    plt.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=frame_grafico)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

def mostrar_grafico_eficiencia():
    limpiar_frame_grafico()
    jugadoras = list(estadisticas.keys())
    ts = [s.get("TS%",0) for s in estadisticas.values()]
    efg = [s.get("eFG%",0) for s in estadisticas.values()]

    ancho = max(8, len(jugadoras) * 0.6)
    fig, ax = plt.subplots(figsize=(ancho, 4))
    ax.bar(range(len(jugadoras)), ts, width=0.4, label="TS%")
    ax.bar([i+0.4 for i in range(len(jugadoras))], efg, width=0.4, label="eFG%")
    ax.set_ylabel("%")
    ax.set_title("Eficiencia de tiro por Jugadora")
    ax.legend()
    ajustar_fig_xticks(ax, jugadoras)
    plt.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=frame_grafico)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

def mostrar_grafico_tov_per_pos():
    limpiar_frame_grafico()
    jugadoras = list(estadisticas.keys())
    tovpos = [s.get("TOV/POS",0) for s in estadisticas.values()]

    ancho = max(8, len(jugadoras) * 0.6)
    fig, ax = plt.subplots(figsize=(ancho, 4))
    ax.bar(range(len(jugadoras)), tovpos, label="TOV/POS")
    ax.set_ylabel("Pérdidas por posesión")
    ax.set_title("TOV / POS por Jugadora")
    ajustar_fig_xticks(ax, jugadoras)
    plt.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=frame_grafico)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

def mostrar_grafico_radar(jugador_key=None):
    limpiar_frame_grafico()
    # si no hay jugador elegido, mostrar radar del equipo (promedios)
    labels = ["PPM","eFG%","TS%","REB/MIN","AST/MIN"]
    if jugador_key and jugador_key in estadisticas:
        values = [
            estadisticas[jugador_key].get("PPM",0),
            estadisticas[jugador_key].get("eFG%",0),
            estadisticas[jugador_key].get("TS%",0),
            estadisticas[jugador_key].get("REB/MIN",0),
            estadisticas[jugador_key].get("AST/MIN",0)
        ]
        title = f"Radar: {jugador_key}"
    else:
        # valores promedio (normalizados)
        n = len(estadisticas)
        values = [
            sum(s.get("PPM",0) for s in estadisticas.values())/n if n>0 else 0,
            sum(s.get("eFG%",0) for s in estadisticas.values())/n if n>0 else 0,
            sum(s.get("TS%",0) for s in estadisticas.values())/n if n>0 else 0,
            sum(s.get("REB/MIN",0) for s in estadisticas.values())/n if n>0 else 0,
            sum(s.get("AST/MIN",0) for s in estadisticas.values())/n if n>0 else 0
        ]
        title = "Radar (promedio equipo)"

    # normalizar para que el radar sea proporcional: escala por máximos razonables
    max_vals = [max( max([s.get("PPM",0) for s in estadisticas.values()]+[1]), 1),
                max( max([s.get("eFG%",0) for s in estadisticas.values()]+[50]), 50),
                max( max([s.get("TS%",0) for s in estadisticas.values()]+[50]), 50),
                max( max([s.get("REB/MIN",0) for s in estadisticas.values()]+[0.1]), 0.1),
                max( max([s.get("AST/MIN",0) for s in estadisticas.values()]+[0.1]), 0.1)
               ]
    vals_norm = [v/m if m>0 else 0 for v,m in zip(values, max_vals)]

    # radar
    N = len(labels)
    angles = np.linspace(0, 2*np.pi, N, endpoint=False).tolist()
    vals_plot = vals_norm + vals_norm[:1]
    angles_plot = angles + angles[:1]

    fig = plt.figure(figsize=(6,6))
    ax = fig.add_subplot(111, polar=True)
    ax.plot(angles_plot, vals_plot, 'o-', linewidth=2)
    ax.fill(angles_plot, vals_plot, alpha=0.25)
    ax.set_thetagrids(np.degrees(angles), labels)
    ax.set_title(title)
    ax.set_ylim(0,1)
    plt.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=frame_grafico)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

def mostrar_grafico_ortg_drtg():
    limpiar_frame_grafico()
    # ORTG y DRTG del equipo (barras comparativas)
    fig, ax = plt.subplots(figsize=(6,3))
    labels = ['Equipo']
    ortg = [totales.get('ORTG',0)]
    drtg = [totales.get('DRTG',0)]
    x = np.arange(len(labels))
    width = 0.35
    ax.bar(x - width/2, ortg, width, label='ORTG')
    ax.bar(x + width/2, drtg, width, label='DRTG')
    ax.set_ylabel('Rating (por 100 posesiones)')
    ax.set_title('ORTG vs DRTG (Equipo)')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    plt.tight_layout()
    canvas = FigureCanvasTkAgg(fig, master=frame_grafico)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

# -------------------------
# Selector de gráficos y binding
# -------------------------
def cambiar_grafico(event=None):
    seleccion = combo_grafico.get()
    if seleccion == "PTS/REB/AST":
        mostrar_grafico_pts_reb_ast()
    elif seleccion == "Eficiencia (TS% vs eFG%)":
        mostrar_grafico_eficiencia()
    elif seleccion == "TOV por posesión":
        mostrar_grafico_tov_per_pos()
    elif seleccion == "Radar (métricas avanzadas)":
        # radar de la jugadora seleccionada
        sel = obtener_jugadora_seleccionada()
        mostrar_grafico_radar(sel)
    elif seleccion == "ORTG vs DRTG":
        mostrar_grafico_ortg_drtg()

def actualizar_grafico_seleccionado():
    # redibuja gráfico actual (útil después de cargar datos)
    cambiar_grafico()

# -------------------------
# Barra lateral (derecha)
# -------------------------
def mostrar_seleccion_default():
    # mostrar primeras informaciones
    lbl_selected_name.config(text="Selecciona una jugadora")
    lbl_selected_stats.config(text="Detalle de jugadora aquí")

def obtener_jugadora_seleccionada():
    sel = tree.selection()
    if not sel:
        return None
    item = tree.item(sel[0])
    nombre = item['values'][0]
    return nombre

def on_tree_select(event):
    nombre = obtener_jugadora_seleccionada()
    if not nombre:
        return
    s = estadisticas.get(nombre, {})
    texto = f"{nombre}\n\nPTS: {s.get('PTS',0)} | MIN: {s.get('MIN',0)}\nPPM: {s.get('PPM',0)}\nTOV/POS: {s.get('TOV/POS',0)}\neFG%: {s.get('eFG%',0)} | TS%: {s.get('TS%',0)}\nREB: {s.get('REB',0)} (O:{s.get('OREB',0)} D:{s.get('DREB',0)})\nREB/MIN: {s.get('REB/MIN',0)}\nAST: {s.get('AST',0)} | AST/MIN: {s.get('AST/MIN',0)}\n%REB_DEF_team: {s.get('%REB_DEF_TEAM',0)}% | %REB_OFF_team: {s.get('%REB_OFF_TEAM',0)}%"
    lbl_selected_name.config(text=nombre)
    lbl_selected_stats.config(text=texto)
    # si el combo está en Radar, actualizar radar al jugador seleccionado
    if combo_grafico.get() == "Radar (métricas avanzadas)":
        mostrar_grafico_radar(nombre)

# -------------------------
# GUI principal
# -------------------------
root = tk.Tk()
root.title("HoopMetrics GUI v5 — Gráficos y Sidebar")
root.geometry("1200x800")

# Marco principal (left: contenido, right: sidebar)
main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True)

left_frame = tk.Frame(main_frame)
left_frame.pack(side=tk.LEFT, fill="both", expand=True)

right_frame = tk.Frame(main_frame, width=300, padx=10)
right_frame.pack(side=tk.RIGHT, fill="y")

# Logo en sidebar (pequeño)
try:
    logo_img = Image.open("hoopmetrics_logo.png")
    logo_img = logo_img.resize((100,100))
    logo = ImageTk.PhotoImage(logo_img)
    lbl_logo = tk.Label(right_frame, image=logo)
    lbl_logo.pack(pady=5)
except Exception:
    lbl_logo = tk.Label(right_frame, text="HoopMetrics", font=("Arial",14,"bold"))
    lbl_logo.pack(pady=5)

# Botón cargar
btn_cargar = tk.Button(left_frame, text="Cargar estadísticas", command=cargar_datos)
btn_cargar.pack(pady=5, anchor="w")

# Selector de gráficos
combo_grafico = ttk.Combobox(left_frame, values=[
    "PTS/REB/AST",
    "Eficiencia (TS% vs eFG%)",
    "TOV por posesión",
    "Radar (métricas avanzadas)",
    "ORTG vs DRTG"
], state="readonly")
combo_grafico.set("PTS/REB/AST")
combo_grafico.bind("<<ComboboxSelected>>", cambiar_grafico)
combo_grafico.pack(pady=5, anchor="w")

# Frame contenedor para la tabla con scroll (ocupa la parte superior izquierda)
frame_tabla = tk.Frame(left_frame)
frame_tabla.pack(pady=5, fill="both", expand=False)

# Scrollbars para la tabla
scroll_y = tk.Scrollbar(frame_tabla, orient=tk.VERTICAL)
scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
scroll_x = tk.Scrollbar(frame_tabla, orient=tk.HORIZONTAL)
scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

# Tabla estadísticas individuales
cols = ("Jugadora","PTS","REB","AST","STL","BLK","TOV","eFG%","TS%","PPM","REB/MIN","AST/MIN","OREB","DREB","PTS_CONTRA")
tree = ttk.Treeview(frame_tabla, columns=cols, show="headings",
                    yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set, height=10)

for c in cols:
    tree.heading(c, text=c)
    tree.column(c, width=90, anchor="center")

tree.pack(side=tk.LEFT, fill="both", expand=True)
scroll_y.config(command=tree.yview)
scroll_x.config(command=tree.xview)

tree.bind("<<TreeviewSelect>>", on_tree_select)

# Label con estadísticas de equipo (arriba del gráfico en left)
lbl_equipo = tk.Label(left_frame, text="Estadísticas de equipo aparecerán aquí", justify="left", font=("Arial",11))
lbl_equipo.pack(pady=5, anchor="w")

# Frame para gráfico (ocupa el resto izq)
frame_grafico = tk.Frame(left_frame)
frame_grafico.pack(fill="both", expand=True, padx=10, pady=10)

# -- Sidebar derecho: información del equipo y jugadora seleccionada --
lbl_team_title = tk.Label(right_frame, text="Resumen Equipo", font=("Arial",12,"bold"))
lbl_team_title.pack(pady=(10,0))
lbl_equipo_sidebar = tk.Label(right_frame, text="", justify="left", anchor="w")
lbl_equipo_sidebar.pack(fill="x", pady=5)

sep = ttk.Separator(right_frame, orient='horizontal')
sep.pack(fill='x', pady=5)

lbl_selected_name = tk.Label(right_frame, text="Selecciona una jugadora", font=("Arial",11,"bold"), wraplength=260, justify="left")
lbl_selected_name.pack(pady=(5,2), anchor="w")
lbl_selected_stats = tk.Label(right_frame, text="Detalle de jugadora aquí", justify="left", wraplength=260, anchor="w")
lbl_selected_stats.pack(pady=(0,5), anchor="w")

# Definiciones con scroll al final del sidebar
sep2 = ttk.Separator(right_frame, orient='horizontal')
sep2.pack(fill='x', pady=5)
lbl_gloss = tk.Label(right_frame, text="Glosario", font=("Arial",11,"bold"))
lbl_gloss.pack(anchor="w")
text_gloss = tk.Text(right_frame, height=18, wrap=tk.WORD)
text_gloss.pack(fill="both", expand=True)
gloss_content = """
PTS: Puntos anotados.
REB: Rebotes totales.
AST: Asistencias.
STL: Robos de balón.
BLK: Tapones.
TOV: Pérdidas de balón.
MIN: Minutos jugados.
OREB: Rebotes ofensivos.
DREB: Rebotes defensivos.
PTS_CONTRA: Puntos permitidos (plus/minus o valoración recibida).
eFG% (Effective Field Goal %): Ajusta el porcentaje de tiro considerando triples.
TS% (True Shooting %): Eficiencia total de tiro.
PPM: Puntos por minuto.
REB/MIN: Rebotes por minuto.
AST/MIN: Asistencias por minuto.
PPP: Puntos por posesión.
ORTG: Offensive Rating.
DRTG: Defensive Rating.
TOV/POS: Pérdidas por posesión.
%REB_DEF: % de rebotes defensivos del equipo.
%REB_OFF: % de rebotes ofensivos del equipo.
%REB_DEF_TEAM / %REB_OFF_TEAM: participación individual en los rebotes del equipo.
"""
text_gloss.insert(tk.END, gloss_content)
text_gloss.config(state=tk.DISABLED)

# -------------------------
# Funciones de actualización de sidebar y equipo
# -------------------------
def actualizar_sidebar_equipo():
    # mostrar resumen compacto en sidebar
    texto = f"PTS: {totales['PTS']}  |  REB: {totales['REB']}\nORTG: {totales['ORTG']}  |  DRTG: {totales['DRTG']}\nPPP: {totales['PPP']}  |  POS: {totales['POSESIONES']}"
    lbl_equipo_sidebar.config(text=texto)
    # y en el label grande de la izquierda
    mostrar_equipo()

# Llamadas iniciales
mostrar_seleccion_default()

# -------------------------
# Hook para cuando se cierre (limpiar matplotlib)
# -------------------------
def on_close():
    plt.close('all')
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)

# -------------------------
# Atajos para el combobox y redibujo
# -------------------------
# botón para forzar actualización del gráfico actual
btn_update_graph = tk.Button(left_frame, text="Actualizar gráfico", command=actualizar_grafico_seleccionado)
btn_update_graph.pack(pady=4, anchor="w")

# pack final: colocar combo y por defecto dibujar
combo_grafico.pack_forget()
combo_grafico.pack(pady=5, anchor="w")  # re-pack para orden correcto

# cuando cargues datos, se calcula; si quieres probar con datos ya en memoria:
# si existe variable 'estadisticas' definida previamente, la usamos
try:
    estadisticas  # si existe
    calcular_estadisticas()
    mostrar_individuales()
    actualizar_sidebar_equipo()
    actualizar_grafico_seleccionado()
except NameError:
    pass

# sobrescribir mostrar_equipo para que también actualice sidebar
_old_mostrar_equipo = mostrar_equipo
def mostrar_equipo_wrapper():
    _old_mostrar_equipo()
    actualizar_sidebar_equipo()
mostrar_equipo = mostrar_equipo_wrapper

root.mainloop()
