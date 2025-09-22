# app.py
# HoopMetrics - Versión inicial
# Programa de estadística avanzada para baloncesto

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

# -------------------------
# Plantilla del equipo
# -------------------------

jugadoras = [
    "Jugador 1", "Jugador 2", "Jugador 3", "Jugador 4",
    "Jugador 5", "Jugador 6", "Jugador 7", "Jugador 8",
    "Jugador 9", "Jugador 10", "Jugador 11", "Jugador 12"
]

# Diccionario para guardar las estadísticas
estadisticas = {jugadora: {} for jugadora in jugadoras}

# -------------------------
# Entrada de datos
# -------------------------

print("🏀 HoopMetrics - Registro de estadísticas")
print("Introduce las estadísticas de cada jugadora (números enteros).")
print("Si no jugó, introduce 0 en todo.\n")

for jugadora in jugadoras:
    print(f"\n📊 Estadísticas de {jugadora}:")
    pts = int(input("  Puntos: "))
    fga = int(input("  Tiros de campo intentados (FGA): "))
    fg = int(input("  Tiros de campo anotados (FG): "))
    tpa = int(input("  Triples intentados (3PA): "))
    tp = int(input("  Triples anotados (3P): "))
    fta = int(input("  Tiros libres intentados (FTA): "))
    ft = int(input("  Tiros libres anotados (FT): "))
    reb = int(input("  Rebotes totales: "))
    ast = int(input("  Asistencias: "))
    stl = int(input("  Robos: "))
    blk = int(input("  Tapones: "))
    tov = int(input("  Pérdidas: "))

    # Guardamos las estadísticas
    estadisticas[jugadora] = {
        "PTS": pts,
        "FGA": fga, "FG": fg,
        "3PA": tpa, "3P": tp,
        "FTA": fta, "FT": ft,
        "REB": reb, "AST": ast, "STL": stl, "BLK": blk, "TOV": tov,
        "eFG%": round(calcular_efg(fg, tp, fga) * 100, 2),
        "TS%": round(calcular_ts(pts, fga, fta) * 100, 2)
    }

# -------------------------
# Resultados
# -------------------------

print("\n📋 Resumen de estadísticas del partido:\n")
for jugadora, stats in estadisticas.items():
    print(f"{jugadora}:")
    print(f"  PTS: {stats['PTS']} | REB: {stats['REB']} | AST: {stats['AST']} | STL: {stats['STL']} | BLK: {stats['BLK']} | TOV: {stats['TOV']}")
    print(f"  eFG%: {stats['eFG%']}% | TS%: {stats['TS%']}%\n")
