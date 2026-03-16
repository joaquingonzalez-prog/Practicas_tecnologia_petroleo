# 🛢️ Laboratorio Virtual: Tecnologías del Petróleo y Petroquímica

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-red.svg)
![License](https://img.shields.io/badge/Licencia-CC%20BY--NC--SA%204.0-lightgrey.svg)
![UCA](https://img.shields.io/badge/Universidad-Cádiz-gold.svg)

Bienvenido al repositorio oficial del **Laboratorio Virtual de Refino**, un proyecto desarrollado para la convocatoria OpenCourseWare (OCW) de la **Universidad de Cádiz (UCA)**. 

Este proyecto consta de una suite de tres simuladores interactivos desarrollados en Python y Streamlit, diseñados para que los estudiantes de ingeniería experimenten de forma práctica y segura con las operaciones y la toma de decisiones económicas de una refinería de petróleo.

---

## 🌐 Accesos Directos a los Simuladores (Live Demos)

Las aplicaciones están alojadas en la nube y son de libre acceso. Puedes ejecutarlas directamente desde tu navegador haciendo clic en los siguientes enlaces:

* **[▶️ Práctica 1: Caracterización de Crudos (Crude Oil Assay)](https://practica1tepp.streamlit.app/)**
* **[▶️ Práctica 2: Destilación Atmosférica (Curvas TBP vs ASTM)](https://practica2tepp.streamlit.app/)**
* **[▶️ Práctica 3: Craqueo Catalítico (FCC) y Blending de Gasolinas](https://practica3tepp.streamlit.app/)**

---

## 🚀 Descripción de las Prácticas

El laboratorio está dividido en tres fases secuenciales que abarcan desde la recepción del crudo hasta la formulación final del producto comercial:

### 🔬 Práctica 1: Caracterización de Crudos (Crude Oil Assay)
Simula la recepción de una muestra de crudo desconocido en el laboratorio. El alumno debe corregir la densidad térmica, calcular los grados API, determinar el factor de caracterización K_UOP y justificar la viabilidad económica del crudo en función de su contenido en azufre y curva de destilación.

### 🌡️ Práctica 2: Destilación Atmosférica y Rendimientos
Un simulador gráfico e interactivo donde el alumno ajusta los puntos de corte (Cut Points) de una torre de destilación primaria. Enseña la diferencia termodinámica entre las curvas de destilación ASTM D86 y TBP, y permite optimizar el margen de refino ajustando los rendimientos volumétricos de Nafta, Queroseno, Diésel y Residuo.

### 🏭 Práctica 3: Craqueo Catalítico (FCC) y Blending
El corazón de la refinería. Esta práctica acopla dos unidades:
1. **Reactor FCC:** El alumno debe maximizar el octanaje (RON) controlando la temperatura y la relación C/O, evitando el sobrecraqueo y el límite metalúrgico por generación de coque.
2. **Unidad de Blending:** Utilizando la nafta producida en el FCC, el alumno debe formular una gasolina comercial (RON >= 95) mezclando corrientes (Nafta ligera, Alquilato, Reformado) al menor coste posible.

---

## 💻 Instalación y Ejecución Local

Si deseas ejecutar los simuladores en tu propio ordenador en lugar de usar la versión web, sigue estos pasos:

1. **Clona este repositorio:**
   git clone https://github.com/tu-usuario/nombre-del-repo.git
   cd nombre-del-repo

2. **Instala las dependencias necesarias:**
   Asegúrate de tener Python instalado y ejecuta:
   pip install -r requirements.txt

3. **Ejecuta la aplicación deseada:**
   streamlit run practica1_coa.py
   # o
   streamlit run practica2_TBP.py
   # o
   streamlit run practica3_fcc.py

---

## 🛠️ Tecnologías Utilizadas
* **Python:** Lógica del motor de simulación y cálculos termodinámicos.
* **Streamlit:** Framework para el desarrollo de la interfaz web interactiva.
* **Pandas & NumPy:** Manejo de matrices de datos e interpolación matemática.
* **Plotly:** Generación de gráficas dinámicas y paneles de control interactivos.

---

## 👨‍🏫 Autoría y Contexto Académico
* **Autor:** Prof. José Joaquín González Cortés
* **Asignatura:** Tecnologías del Petróleo y Petroquímica
* **Institución:** Universidad de Cádiz (UCA) - Proyecto OCW

---

## 📄 Licencia

Este material ha sido creado para uso educativo abierto. 

El contenido teórico, los manuales y el código fuente de este repositorio se distribuyen bajo la licencia **Creative Commons Reconocimiento-NoComercial-CompartirIgual 4.0 Internacional (CC BY-NC-SA 4.0)**. 

Eres libre de compartir y adaptar este material, siempre y cuando reconozcas la autoría original, no lo utilices con fines comerciales y distribuyas tus contribuciones bajo la misma licencia.
