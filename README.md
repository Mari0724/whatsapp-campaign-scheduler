# Estructura del proyecto

```

whatsapp-campaign/
│
├── src/
│   ├── main.py               # Punto de entrada
│   ├── sender.py             # Envía mensajes
│   ├── scheduler.py          # Decide si hoy toca enviar
│   ├── config.py             # Configuración
│   └── logger.py             # Registros
│
├── data/
│   ├── schedule.json         # Calendario de envíos
│   ├── sent.json             # Registro de enviados
│   └── templates.json        # Los mensajes
│
├── images/
│   ├── portada.png
│   ├── pildora01.png
│   ├── pildora02.png
│   └── ...
│
├── logs/
│
├── chrome-profile/
│
├── requirements.txt
│
├── .gitignore
│
└── README.md

```