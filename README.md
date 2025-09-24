# HoopMetrics GUI

HoopMetrics es una herramienta en Python para **calcular y visualizar estadísticas de baloncesto** de jugadores y equipos. Esta versión incluye una interfaz gráfica (GUI) simple y moderna utilizando Tkinter, con gráficos y definiciones de métricas.

---

## 🏀 Características

- Cálculo de estadísticas individuales:
  - PTS, REB, AST, STL, BLK, TOV, MIN
  - eFG% (Effective Field Goal %)
  - TS% (True Shooting %)
  - PPM (Puntos por minuto)
  - REB/MIN y AST/MIN

- Cálculo de estadísticas de equipo:
  - Totales de PTS, REB, AST, STL, BLK, TOV
  - eFG% y TS% del equipo
  - PPP (Puntos por posesión)
  - ORTG (Offensive Rating)
  - AST/POS y REB/POS

- Visualización:
  - Tabla de estadísticas individuales
  - Panel con estadísticas de equipo
  - Gráfico de barras apiladas de PTS, REB y AST por jugadora
  - Logo de HoopMetrics
  - Glosario completo de métricas con scroll

---

## 📦 Requisitos

- Python 3.8+
- Librerías Python:
  - `tkinter` (incluida en Python)
  - `Pillow` (para cargar imágenes)
  - `matplotlib` (para gráficos)

Instalación de librerías adicionales:

```bash
pip install pillow matplotlib
⚡ Uso

Clonar el repositorio:

git clone https://github.com/tuusuario/hoopmetrics.git
cd hoopmetrics


Guardar el archivo de estadísticas JSON en el mismo directorio (ejemplo: estadisticas.json).

Ejecutar la aplicación:

python hoopmetrics_gui_v3.py


Dentro de la GUI:

Haz clic en "Cargar estadísticas" para seleccionar tu archivo JSON.

Visualiza las estadísticas individuales y de equipo.

Consulta el gráfico de PTS, REB y AST por jugadora.

Revisa el glosario de métricas con definiciones completas.

📁 Estructura del repositorio
hoopmetrics/
├── hoopmetrics_gui_v3.py   # Script principal con GUI
├── hoopmetrics_logo.png    # Logo de la aplicación
├── estadisticas.json       # Archivo de ejemplo con estadísticas
└── README.md

📝 Notas

La aplicación ajusta automáticamente los gráficos y el texto según el tamaño de la ventana.

Requiere que el archivo de estadísticas tenga la siguiente estructura por jugadora:

{
  "Jugadora1": {"PTS":10,"REB":5,"AST":3,"STL":1,"BLK":0,"TOV":2,"FG":4,"FGA":8,"3P":1,"FTA":2,"MIN":20},
  "Jugadora2": {...}
}


Puedes modificar el tamaño de la ventana para mejorar la visualización del gráfico y del glosario.

📌 Licencia

Este proyecto está bajo la licencia MIT.

👤 Autor

José Miguel Gómez Fernández
