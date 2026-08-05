# ==========================================
# MODO DE EJECUCIÓN
# ==========================================

TEST_MODE = True

# ==========================================
# CHATS
# ==========================================

TEST_CHAT = "Chat de prueba"
PRODUCTION_CHAT = "Chat de producción"

# ==========================================
# HORARIOS
# ==========================================

TEST_TIME = "14:51"
PRODUCTION_TIME = "10:00"

# ==========================================
# ARCHIVOS
# ==========================================

if TEST_MODE:
    SCHEDULE_FILE = "schedule_test.json"
else:
    SCHEDULE_FILE = "schedule.json"