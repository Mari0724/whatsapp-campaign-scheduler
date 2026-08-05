# WhatsApp Campaign Scheduler

Automatiza el envío programado de campañas por **WhatsApp Web** utilizando **Python** y **Playwright**.

Este proyecto fue desarrollado para facilitar el envío de campañas informativas de forma completamente automática, permitiendo programar mensajes con imágenes para fechas específicas, reutilizar plantillas de texto y mantener un registro de los envíos realizados.

Aunque inicialmente fue creado para una campaña de **ciberseguridad dirigida a adultos mayores**, su arquitectura permite reutilizarlo fácilmente para cualquier otro tipo de campaña simplemente modificando la configuración, las plantillas y el cronograma de envíos.

---

# 📋 Información del proyecto

| Característica | Detalle |
|----------------|---------|
| Lenguaje | Python 3.12 |
| Automatización | Playwright |
| Navegador | Google Chrome |
| Plataforma | Windows |
| Ejecución programada | Programador de tareas de Windows |
| Estado | ✅ Funcional |
| Tipo de proyecto | Automatización de procesos |
| Licencia | MIT |

---

# 🎯 Objetivo

Este proyecto busca demostrar cómo automatizar campañas programadas en WhatsApp Web utilizando herramientas gratuitas y buenas prácticas de desarrollo.

Su diseño separa claramente la configuración, la lógica de negocio y la automatización del navegador, facilitando el mantenimiento y permitiendo reutilizar la herramienta en futuras campañas sin modificar el código principal.

---

# ✨ Características

- Envío automático de mensajes mediante WhatsApp Web.
- Envío de imágenes junto con el mensaje.
- Programación de campañas por fecha y hora.
- Sistema de plantillas reutilizables.
- Configuración centralizada.
- Modo de pruebas y modo producción.
- Registro automático de envíos exitosos y errores.
- Prevención de envíos duplicados.
- Reutilización de la sesión de Chrome mediante un perfil persistente.
- Integración con el Programador de tareas de Windows.
- Arquitectura modular y fácil de extender.

---

# 🛠️ Tecnologías utilizadas

- Python 3.12
- Playwright
- Google Chrome
- WhatsApp Web
- JSON
- Windows Task Scheduler

---

# 🏗️ Arquitectura del proyecto

El proyecto está dividido en módulos independientes, donde cada archivo tiene una única responsabilidad.

```text
Programador de tareas
        │
        ▼
main.py
        │
        ▼
Scheduler
        │
        ├── ¿Es la hora?
        ├── ¿Existe campaña para hoy?
        ├── ¿Ya fue enviada?
        ▼
Sender
        │
        ▼
Playwright
        │
        ▼
Google Chrome
        │
        ▼
WhatsApp Web
        │
        ▼
Logger
```

Cada componente puede evolucionar de forma independiente, reduciendo el acoplamiento y facilitando el mantenimiento del proyecto.

---

# 📂 Estructura del proyecto

```text
whatsapp-campaign-scheduler/
│
├── src/
│   ├── main.py
│   ├── sender.py
│   ├── scheduler.py
│   ├── logger.py
│   └── config.py
│
├── data/
│   ├── schedule.json
│   ├── schedule_test.json
│   └── templates.json
│
├── images/
│
├── logs/
│
├── chrome-profile/
│
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

---

# 🚀 Instalación

## 1. Clonar el repositorio

Clona el repositorio desde GitHub y entra en la carpeta del proyecto.

```bash
git clone https://github.com/Mari0724/whatsapp-campaign-scheduler.git

cd whatsapp-campaign-scheduler
```

---

## 2. Crear un entorno virtual

Se recomienda utilizar un entorno virtual para aislar las dependencias del proyecto.

```bash
python -m venv .venv
```

---

## 3. Activar el entorno virtual

### Windows (PowerShell)

```powershell
.venv\Scripts\Activate.ps1
```

### Windows (CMD)

```cmd
.venv\Scripts\activate.bat
```

Cuando el entorno esté activo, el nombre del entorno aparecerá al inicio de la consola:

```text
(.venv)
```

---

## 4. Instalar las dependencias

Instala todas las librerías necesarias utilizando el archivo `requirements.txt`.

```bash
pip install -r requirements.txt
```

---

## 5. Instalar Playwright

Además de instalar la librería, Playwright necesita descargar los navegadores que utilizará para la automatización.

Ejecuta:

```bash
python -m playwright install
```

Este paso solo debe realizarse una vez.

---

# ⚙️ Configuración inicial

Antes de utilizar el proyecto por primera vez es necesario realizar una configuración inicial.

---

## Paso 1. Configurar el modo de ejecución

Abre el archivo:

```text
src/config.py
```

Allí encontrarás:

```python
TEST_MODE = True
```

### Modo prueba

```python
TEST_MODE = True
```

Utiliza:

- El chat de pruebas.
- El horario de pruebas.
- El archivo `schedule_test.json`.

>⚠️ Se recomienda realizar todas las pruebas utilizando TEST_MODE = True antes de ejecutar una campaña real. Esto evita el envío accidental de mensajes al grupo de producción.

### Modo producción

```python
TEST_MODE = False
```

Utiliza:

- El grupo de producción.
- El horario oficial.
- El archivo `schedule.json`.

---

## Paso 2. Configurar el chat

En el mismo archivo configura el nombre exacto del chat de WhatsApp.

```python
TEST_CHAT = "Chat de prueba"
PRODUCTION_CHAT = "Chat de producción"
```

El nombre debe coincidir exactamente con el nombre mostrado en WhatsApp Web con espacios o caracteres especiales.

---

## Paso 3. Configurar la hora de envío

También es posible modificar la hora del envío automático.

```python
TEST_TIME = "14:00"

PRODUCTION_TIME = "10:00"
```

El formato utilizado es de 24 horas (`HH:MM`).

Ejemplos:

```text
09:00
14:30
18:45
```

---

## Paso 4. Configurar el cronograma

El proyecto incluye dos cronogramas:

| Archivo | Uso |
|----------|-----|
| `schedule_test.json` | Pruebas del sistema. |
| `schedule.json` | Campaña oficial. |

Cada campaña contiene:

- Fecha de envío.
- Número de la píldora.
- Imagen correspondiente.
- Plantilla de mensaje.

Ejemplo:

```json
{
    "date": "2026-08-17",
    "number": 1,
    "image": "01-Pildora.png",
    "template": "weekly"
}
```

---

## Paso 5. Configurar las plantillas

Los mensajes se almacenan en:

```text
data/templates.json
```

Actualmente existen tres plantillas:

| Plantilla | Descripción |
|------------|-------------|
| `presentation` | Mensaje de presentación de la campaña. |
| `weekly` | Mensaje semanal reutilizable. |
| `farewell` | Mensaje de cierre de la campaña. |

La plantilla semanal utiliza la variable:

```text
{number}
```

La cual es reemplazada automáticamente por el número de la píldora correspondiente.

---

## Paso 6. Agregar las imágenes

Todas las imágenes deben almacenarse dentro de la carpeta:

```text
images/
```

Se recomienda mantener una nomenclatura consistente, por ejemplo:

```text
00-Portada.png
01-Pildora.png
02-Pildora.png
...
12-Pildora-final.png
```

Los nombres deben coincidir exactamente con los definidos en `schedule.json`.

---

## Paso 7. Primer inicio de sesión

La primera vez que se ejecuta el proyecto será necesario iniciar sesión en WhatsApp Web.

Ejecuta:

```bash
python src/main.py
```

Se abrirá automáticamente Google Chrome.

1. Escanea el código QR con tu teléfono.
2. Espera a que WhatsApp Web cargue completamente.
3. Cierra el programa normalmente.

A partir de ese momento la sesión quedará almacenada dentro de la carpeta:

```text
chrome-profile/
```

Mientras dicha carpeta no sea eliminada, no será necesario volver a escanear el código QR.

> **Importante:** El contenido de la carpeta `chrome-profile` se excluye mediante `.gitignore`, ya que almacena la sesión de WhatsApp del usuario. El repositorio únicamente conserva la estructura de la carpeta utilizando un archivo `.gitkeep`.

---

# 📄 Licencia

Este proyecto se distribuye bajo la licencia **MIT**.

Consulta el archivo `LICENSE` para obtener más información.

---

# 👩‍💻 Autora

**María Ximena Marín Delgado**

Desarrollado como un proyecto de automatización utilizando Python, Playwright y WhatsApp Web.