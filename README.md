# IEE2714 — Fundamentos de Procesamiento de Imágenes

## Tarea 1 — Antonia Fibla

La tarea aborda los temas:

1. Ruido Poisson y filtrado Gaussiano adaptativo 
2. Difusión anisotrópica, Variación Total y diseño del coeficiente de difusión 

---

## Estructura del repositorio

La implementación de cada pregunta se desarrolla en un archivo .py independiente y la experimentación y análisis se encuentra en su respectivo Jupiter Notebook

```text
.
├── README.md
│
├── P1_FiltroGaussiano.ipynb
├── P2_.ipynb
│
├── src/
│   ├──p1.py
|   └──p2.py
│
└── results/
│   ├──p1/
|   |   └── ...
|   └──p2/
        └── ...
```

---

# Pregunta 1 — Contenido
```text
p1.py
├── Imágen Sintetica
├── Simulación Poisson con semilla para experimentos
├── Kernel Gaussiano
├── Medición RMSE
├── Filtro Gaussiano
├── Mapeo de sigma
└── Filtro Gaussiano Adaptativo

```

La organización general del notebook es:

```text
P1_FiltroGaussiano.ipynb
└── Análisis y exploración
    ├──Exploración valores $\sigma$ e Identificación mínimo de RMSE por regiones y global
    ├── Grafica $\sigma$ vs RMSE (por región y global)
    ├── Tabla resumen sigma y RMSE
    ├── Análisis Curvas RMSE
    ├── Regla $\sigma = F(\hat{\mu})$ adaptar ancho del gaussiano
    └──  Aplicación Filtro adaptativo, Metricas comparativas, Analisis y comparaciones

```

---

# Pregunta 2 — 


# Librerías utilizadas

La implementación se desarrolla en Python y utiliza principalmente las siguientes librerías:

* **NumPy**: operaciones numéricas y manipulación de arreglos.
* **Matplotlib**: visualización de imágenes, histogramas, curvas y resultados.
* **scipy**: convolución para aplicar filtro gaussiano

Las principales funciones utilizadas incluyen:

```python
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import convolve2d
```


---

# Requisitos

Se requiere:

* Python 3
* Jupyter Notebook o JupyterLab
* NumPy
* Matplotlib
* scipy

---

# Ejecución

Cada pregunta puede ejecutarse de manera independiente desde su respectivo notebook.

```

Se recomienda ejecutar las celdas en orden desde el inicio del notebook para reproducir correctamente las implementaciones, experimentos, figuras y resultados.

---

# Datos e imágenes

Los resultados y figuras generados durante la experimentación pueden almacenarse en la carpeta `results/`.

```text

results/
    figuras y resultados generados
```

---

# Reproducibilidad

Cada notebook contiene los parámetros utilizados en los experimentos y las figuras principales de cada análisis.

Para reproducir los resultados del informe:

1. Clonar o descargar este repositorio.
2. Instalar las dependencias indicadas.
3. Abrir el notebook correspondiente.
4. Ejecutar las celdas en orden.
5. Verificar los parámetros indicados en cada experimento.

Las figuras y comparaciones presentadas en el informe se generan a partir de los experimentos contenidos en estos notebooks.