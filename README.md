# ☀️ MeteoAnalitica: Tu Herramienta de Análisis Climático

MeteoAnalitica es una aplicación interactiva desarrollada con Streamlit que te permite explorar y visualizar datos climáticos históricos. Diseñada para ser intuitiva y fácil de usar, MeteoAnalitica transforma tus datos brutos en gráficos y análisis significativos, ayudándote a comprender mejor los patrones y extremos climáticos de una ubicación específica (actualmente, optimizada para La Pobla Tornesa).

## 🚀 Funcionalidades Principales

Dashboard del Último Mes: Obtén una visión rápida y detallada del mes más reciente en tus datos, incluyendo un resumen de temperaturas diarias.

- Comparación Mensual Detallada: Selecciona un mes y una variable para comparar su evolución diaria a lo largo de todos los años disponibles en tu dataset. Ideal para identificar tendencias interanuales.
- Promedios Históricos: Visualiza la evolución del promedio diario de una variable a lo largo de todo el año, y compara un año específico con este promedio histórico.
- Análisis de Extremos Climáticos: Identifica y muestra los días con los valores más altos o más bajos para cualquier variable numérica en tus registros históricos.

## 🛠️ Tecnologías Utilizadas

- Python: El lenguaje de programación principal.
- Streamlit: Framework para la creación rápida y sencilla de aplicaciones web de datos.
- Pandas: Para la manipulación y análisis de datos.
- Matplotlib: Para la creación de gráficos estáticos.

## 📊 Datos

La aplicación está diseñada para funcionar con un archivo CSV llamado datos_clima.csv ubicado en la carpeta data/ de la raíz del proyecto. Asegúrate de que tu archivo CSV contenga una columna de fechas llamada DAY (en formato DD/MM/AAAA o el especificado en app.py) y las columnas numéricas con las variables climáticas que desees analizar (Temperatura_Maxima, Precipitacion, etc.).

## ⚙️ Cómo Ejecutar la Aplicación Localmente

Si quieres ejecutar MeteoAnalitica en tu propio ordenador:

### Clona el Repositorio:

```Bash

git clone https://github.com/tu_usuario/MeteoAnalitica.git
cd MeteoAnalitica
(Reemplaza tu_usuario con tu nombre de usuario de GitHub)
```

### Crea y Activa un Entorno Virtual:

Es altamente recomendable usar un entorno virtual para gestionar las dependencias.

```Bash

python3 -m venv .venv
source .venv/bin/activate
(En Windows CMD: .\.venv\Scripts\activate.bat / En Windows PowerShell: .\.venv\Scripts\Activate.ps1)
```

### Instala las Dependencias:

```Bash

pip install -r requirements.txt
```

### Coloca tus Datos:

Asegúrate de tener tu archivo datos_clima.csv dentro de la carpeta data/ en la raíz del proyecto. Si la carpeta data/ no existe, créala.

### Ejecuta la Aplicación:

```Bash

streamlit run app.py
La aplicación se abrirá automáticamente en tu navegador web.
```

## 🌐 Ver la Aplicación Desplegada

MeteoAnalitica está desplegada y disponible públicamente en Streamlit Community Cloud:

Accede a MeteoAnalitica [aquí](https://poblaclima.streamlit.app/)

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Si tienes ideas para mejorar la aplicación, no dudes en abrir un issue o enviar un pull request.

## 📧 Contacto

Conecta o contacta conmigo a través de:

- [![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/qserrano/)
- [![X (Twitter)](https://img.shields.io/badge/X-000000?style=for-the-badge&logo=x&logoColor=white)](https://x.com/qserrano)
- [![Correo Electrónico](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:qode66@gmail.com)
- [![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/qserrano)
