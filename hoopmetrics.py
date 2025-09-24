# hoopmetrics_gui_v4.py
import json
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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
    mostrar_grafico()
    mostrar_definiciones()

def calcular_estadisticas():
    global totales
    totales = {
        "PTS":0,"REB":0,"AST":0,"FG":0,"FGA":0,"3P":0,"FTA":0,"TOV":0,
        "STL":0,"BLK":0,"MIN":0,"OREB":0,"DREB":0,"PTS_CONTRA":0
    }

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

        stats["eFG%"] = round(calcular_efg(fg,tp,fga)*100,2)
        stats["TS%"] = round(calcular_ts(pts,fga,fta)*100,2)
        stats["PPM"] = round(puntos_por_minuto(pts,min_jugados),2)
        stats["REB/MIN"] = round(estadistica_por_minuto(reb,min_jugados),2)
        stats["AST/MIN"] = round(estadistica_por_minuto(ast,min_jugados),2)

        for key in ["PTS","REB","AST","FG","FGA","3P","FTA","TOV","STL","BLK","MIN","OREB","DREB","PTS_CONTRA"]:
            totales[key] += stats.get(key,0)

    totales["eFG%"] = round(calcular_efg(totales["FG"],totales["3P"],totales["FGA"])*100,2)
    totales["TS%"] = round(calcular_ts(totales["PTS"],totales["FGA"],totales["FTA"])*100,2)

    posesiones = totales["FGA"] - totales["FG"] + 0.44*totales["FTA"] + totales["TOV"]

    totales["PPP"] = round(totales["PTS"]/posesiones,2) if posesiones>0 else 0
    totales["ORTG"] = round(totales["PPP"]*100,2)
    totales["AST/POS"] = round(totales["AST"]/posesiones,2) if posesiones>0 else 0
    totales["REB/POS"] = round(totales["REB"]/posesiones,2) if posesiones>0 else 0
    totales["TOV/POS"] = round(totales["TOV"]/posesiones,2) if posesiones>0 else 0

    # Métricas defensivas
    totales["%REB_DEF"] = round(totales["DREB"]/totales["REB"]*100,2) if totales["REB"]>0 else 0
    totales["%REB_OFF"] = round(totales["OREB"]/totales["REB"]*100,2) if totales["REB"]>0 else 0
    totales["DRTG"] = round(totales["PTS_CONTRA"]/posesiones*100,2) if posesiones>0 else 0

def mostrar_individuales():
    for i in tree.get_children():
        tree.delete(i)
    for jugadora, s in estadisticas.items():
        tree.insert("", "end", values=(
            jugadora, s["PTS"], s["REB"], s["AST"], s["STL"], s["BLK"], s["TOV"],
            s["eFG%"], s["TS%"], s["PPM"], s["REB/MIN"], s["AST/MIN"],
            s.get("OREB",0), s.get("DREB",0), s.get("PTS_CONTRA",0)
        ))

def mostrar_equipo():
    texto = f"""
🏀 ESTADÍSTICAS DEL EQUIPO
PTS: {totales['PTS']} | REB: {totales['REB']} | AST: {totales['AST']}
STL: {totales['STL']} | BLK: {totales['BLK']} | TOV: {totales['TOV']}
eFG%: {totales['eFG%']}% | TS%: {totales['TS%']}%
PPP: {totales['PPP']} | ORTG: {totales['ORTG']}
AST/POS: {totales['AST/POS']} | REB/POS: {totales['REB/POS']} | TOV/POS: {totales['TOV/POS']}
%REB_DEF: {totales['%REB_DEF']} | %REB_OFF: {totales['%REB_OFF']} | DRTG: {totales['DRTG']}
"""
    lbl_equipo.config(text=texto)

def mostrar_grafico():
    for widget in frame_grafico.winfo_children():
        widget.destroy()

    jugadoras = list(estadisticas.keys())
    pts = [s["PTS"] for s in estadisticas.values()]
    reb = [s["REB"] for s in estadisticas.values()]
    ast = [s["AST"] for s in estadisticas.values()]

    fig, ax = plt.subplots(figsize=(7,3))
    ax.bar(jugadoras, pts, label="PTS")
    ax.bar(jugadoras, reb, bottom=pts, label="REB")
    ax.bar(jugadoras, ast, bottom=[i+j for i,j in zip(pts,reb)], label="AST")
    ax.set_ylabel("Estadísticas")
    ax.set_title("Puntos, Rebotes y Asistencias por Jugadora")
    ax.legend()
    ax.set_xticklabels(jugadoras, rotation=45, ha="right")

    canvas = FigureCanvasTkAgg(fig, master=frame_grafico)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

def mostrar_definiciones():
    definiciones_text.delete(1.0, tk.END)
    definiciones = """
📘 DEFINICIONES DE MÉTRICAS:

PTS: Puntos anotados.
REB: Rebotes totales.
AST: Asistencias.
STL: Robos de balón.
BLK: Tapones.
TOV: Pérdidas de balón.
MIN: Minutos jugados.
OREB: Rebotes ofensivos.
DREB: Rebotes defensivos.
PTS_CONTRA: Puntos permitidos.
eFG% (Effective Field Goal %): Ajusta el porcentaje de tiro considerando triples.
TS% (True Shooting %): Eficiencia total de tiro.
PPM: Puntos por minuto.
REB/MIN: Rebotes por minuto.
AST/MIN: Asistencias por minuto.
PPP: Puntos por posesión.
ORTG: Offensive Rating.
AST/POS: Asistencias por posesión.
REB/POS: Rebotes por posesión.
TOV/POS: Pérdidas por posesión.
%REB_DEF: % de rebotes defensivos capturados.
%REB_OFF: % de rebotes ofensivos capturados.
DRTG: Defensive Rating, puntos permitidos por 100 posesiones.
"""
    definiciones_text.insert(tk.END, definiciones)

# -------------------------
# GUI principal
# -------------------------
root = tk.Tk()
root.title("HoopMetrics GUI Avanzado")
root.geometry("950x750")

# Logo
logo_img = Image.open("hoopmetrics_logo.png")
logo_img = logo_img.resize((120,120))
logo = ImageTk.PhotoImage(logo_img)
lbl_logo = tk.Label(root, image=logo)
lbl_logo.pack(pady=5)

btn_cargar = tk.Button(root, text="Cargar estadísticas", command=cargar_datos)
btn_cargar.pack(pady=5)

# Frame contenedor para la tabla con scroll
frame_tabla = tk.Frame(root)
frame_tabla.pack(pady=5, fill="both", expand=False)

# Scrollbar vertical
scroll_y = tk.Scrollbar(frame_tabla, orient=tk.VERTICAL)
scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

# Scrollbar horizontal
scroll_x = tk.Scrollbar(frame_tabla, orient=tk.HORIZONTAL)
scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

# Tabla estadísticas individuales
cols = ("Jugadora","PTS","REB","AST","STL","BLK","TOV","eFG%","TS%","PPM","REB/MIN","AST/MIN","OREB","DREB","PTS_CONTRA")
tree = ttk.Treeview(frame_tabla, columns=cols, show="headings",
                    yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set, height=8)

for c in cols:
    tree.heading(c, text=c)
    tree.column(c, width=80, anchor="center")  # Ajusta ancho de columnas

tree.pack(side=tk.LEFT, fill="both", expand=True)

# Configurar scrollbars
scroll_y.config(command=tree.yview)
scroll_x.config(command=tree.xview)

# Estadísticas de equipo
lbl_equipo = tk.Label(root, text="Estadísticas de equipo aparecerán aquí", justify="left", font=("Arial",11))
lbl_equipo.pack(pady=5)

# Frame para gráfico
frame_grafico = tk.Frame(root)
frame_grafico.pack(fill="both", expand=True, padx=10, pady=10)

# Frame para definiciones con scroll
frame_def = tk.Frame(root)
frame_def.pack(fill="both", expand=True, padx=10, pady=5)

scroll = tk.Scrollbar(frame_def)
scroll.pack(side=tk.RIGHT, fill=tk.Y)
definiciones_text = tk.Text(frame_def, height=10, yscrollcommand=scroll.set, wrap=tk.WORD)
definiciones_text.pack(fill="both", expand=True)
scroll.config(command=definiciones_text.yview)

root.mainloop()
