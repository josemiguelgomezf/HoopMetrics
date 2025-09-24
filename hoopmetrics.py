# hoopmetrics_pro.py
# HoopMetrics - Versión avanzada con estadísticas de equipo y definiciones

import json

# -------------------------
# Funciones de estadísticas
# -------------------------

def calcular_efg(fg, tp, fga):
    """Effective Field Goal Percentage"""
    if fga == 0:
        return 0
    return (fg + 0.5 * tp) / fga

def calcular_ts(pts, fga, fta):
    """True Shooting Percentage"""
    intentos = (2 * (fga + 0.44 * fta))
    if intentos == 0:
        return 0
    return pts / intentos

def puntos_por_minuto(pts, min_jugados):
    return pts / min_jugados if min_jugados > 0 else 0

def estadistica_por_minuto(valor, min_jugados):
    return valor / min_jugados if min_jugados > 0 else 0

# -------------------------
# Cargar datos
# -------------------------

with open("estadisticas.json", "r", encoding="utf-8") as f:
    estadisticas = json.load(f)

# -------------------------
# Calcular estadísticas individuales
# -------------------------

for jugadora, stats in estadisticas.items():
    fg = stats.get("FG", 0)
    tp = stats.get("3P", 0)
    fga = stats.get("FGA", 0)
    pts = stats.get("PTS", 0)
    fta = stats.get("FTA", 0)
    reb = stats.get("REB", 0)
    ast = stats.get("AST", 0)
    min_jugados = stats.get("MIN", 0)

    stats["eFG%"] = round(calcular_efg(fg, tp, fga) * 100, 2)
    stats["TS%"] = round(calcular_ts(pts, fga, fta) * 100, 2)
    stats["PPM"] = round(puntos_por_minuto(pts, min_jugados), 2)
    stats["REB/MIN"] = round(estadistica_por_minuto(reb, min_jugados), 2)
    stats["AST/MIN"] = round(estadistica_por_minuto(ast, min_jugados), 2)

# -------------------------
# Estadísticas de equipo
# -------------------------

totales = {
    "PTS": sum(p["PTS"] for p in estadisticas.values()),
    "REB": sum(p["REB"] for p in estadisticas.values()),
    "AST": sum(p["AST"] for p in estadisticas.values()),
    "FG": sum(p["FG"] for p in estadisticas.values()),
    "FGA": sum(p["FGA"] for p in estadisticas.values()),
    "3P": sum(p["3P"] for p in estadisticas.values()),
    "FTA": sum(p["FTA"] for p in estadisticas.values()),
    "TOV": sum(p["TOV"] for p in estadisticas.values()),   # ✅ añadido
    "MIN": sum(p["MIN"] for p in estadisticas.values())
}

totales["eFG%"] = round(calcular_efg(totales["FG"], totales["3P"], totales["FGA"]) * 100, 2)
totales["TS%"] = round(calcular_ts(totales["PTS"], totales["FGA"], totales["FTA"]) * 100, 2)

# ✅ Cálculo de posesiones estimadas (fórmula estándar)
posesiones = totales["FGA"] - totales["FG"] + 0.44 * totales["FTA"] + totales["TOV"]
totales["PPP"] = round(totales["PTS"] / posesiones, 2) if posesiones > 0 else 0
totales["ORTG"] = round(totales["PPP"] * 100, 2)

# -------------------------
# Resultados individuales
# -------------------------

print("\n📊 ESTADÍSTICAS INDIVIDUALES:\n")
for jugadora, s in estadisticas.items():
    print(f"{jugadora}:")
    print(f"  PTS: {s['PTS']} | REB: {s['REB']} | AST: {s['AST']} | STL: {s['STL']} | BLK: {s['BLK']} | TOV: {s['TOV']} | MIN: {s['MIN']}")
    print(f"  eFG%: {s['eFG%']}% | TS%: {s['TS%']}% | PPM: {s['PPM']} | REB/MIN: {s['REB/MIN']} | AST/MIN: {s['AST/MIN']}\n")

# -------------------------
# Resultados de equipo
# -------------------------

print("\n🏀 ESTADÍSTICAS DEL EQUIPO:\n")
print(f"  Puntos totales: {totales['PTS']}")
print(f"  Rebotes totales: {totales['REB']}")
print(f"  Asistencias totales: {totales['AST']}")
print(f"  eFG% equipo: {totales['eFG%']}%")
print(f"  TS% equipo: {totales['TS%']}%")
print(f"  Puntos por posesión (PPP): {totales['PPP']}")
print(f"  Rating ofensivo (ORTG): {totales['ORTG']}\n")

# -------------------------
# Glosario de métricas
# -------------------------

print("📘 DEFINICIONES DE MÉTRICAS:\n")
print("PTS: Puntos anotados.")
print("REB: Rebotes totales.")
print("AST: Asistencias.")
print("STL: Robos de balón.")
print("BLK: Tapones.")
print("TOV: Pérdidas de balón.")
print("MIN: Minutos jugados.")
print("eFG% (Effective Field Goal %): Ajusta el porcentaje de tiro considerando el valor adicional de los triples.")
print("TS% (True Shooting %): Mide la eficiencia total de tiro considerando tiros de campo y tiros libres.")
print("PPM (Puntos por minuto): Promedio de puntos anotados por cada minuto jugado.")
print("REB/MIN: Rebotes capturados por minuto jugado.")
print("AST/MIN: Asistencias repartidas por minuto jugado.")
print("PPP (Puntos por posesión): Promedio de puntos anotados por cada posesión del equipo.")
print("ORTG (Offensive Rating): Puntos anotados por cada 100 posesiones. Indica la eficiencia ofensiva del equipo.")
