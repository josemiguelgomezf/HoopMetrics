🏀 HoopMetrics
Aplicación de estadística avanzada para baloncesto desarrollada en Python, compatible con PC y móviles.

HoopMetrics permite registrar partidos, calcular métricas tradicionales (puntos, rebotes, asistencias, robos, tapones) y estadísticas avanzadas (PER, eFG%, TS%, ORtg, DRtg, Win Shares, entre otras). Su objetivo es proporcionar a entrenadores, jugadores y analistas una herramienta sencilla pero potente para mejorar el análisis del rendimiento individual y colectivo.

🚀 Características principales (v1.0)
Registro de jugadores y equipos.

Introducción rápida de estadísticas por partido.

Cálculo automático de:

Puntos, rebotes, asistencias, robos, tapones.

eFG% (Effective Field Goal Percentage).

TS% (True Shooting Percentage).

Exportación de estadísticas en CSV/Excel.

📦 Instalación
Clona este repositorio:

git clone [https://github.com/tuusuario/HoopMetrics.git](https://github.com/tuusuario/HoopMetrics.git)
cd HoopMetrics

Crea un entorno virtual (opcional pero recomendado):

python -m venv venv

En Linux/Mac:

source venv/bin/activate

En Windows:

venv\Scripts\activate

Instala las dependencias:

pip install -r requirements.txt

▶️ Uso
Ejecuta la aplicación:

python app.py

En la versión inicial, la aplicación se ejecuta en terminal y permite:

Registrar jugadores.

Introducir estadísticas de un partido.

Obtener un resumen de métricas tradicionales y avanzadas.

📱 Compatibilidad
PC: Windows, Linux, MacOS.

Móviles: A través de navegadores o empaquetando la app con Kivy o BeeWare (roadmap).

🛣️ Roadmap
[ ] Interfaz gráfica básica (Tkinter / Kivy).

[ ] Dashboard con gráficas de rendimiento.

[ ] Base de datos para almacenar temporadas completas.

[ ] Exportación en formatos PDF y Excel.

[ ] Versión instalable en Android/iOS.

🤝 Contribución
¡Las contribuciones son bienvenidas! Sigue estos pasos para contribuir:

Haz un fork del proyecto.

Crea tu rama (ej: git checkout -b feature/nueva-funcion).

Haz commit de tus cambios (git commit -m 'Agregada nueva función').

Haz push a la rama (git push origin feature/nueva-funcion).

Abre un Pull Request.

📜 Licencia
Este proyecto está bajo la licencia MIT.
