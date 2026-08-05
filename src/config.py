# ==========================================
# MODO DE EJECUCIÓN
# ==========================================

TEST_MODE = True

# ==========================================
# CHATS
# ==========================================

TEST_CHAT = "Mami >:3"

PRODUCTION_CHAT = "Adultos Mayores MAIA"

# ==========================================
# HORARIOS
# ==========================================

TEST_TIME = "16:00"

PRODUCTION_TIME = "10:00"

# ==========================================
# ARCHIVOS
# ==========================================

if TEST_MODE:
    SCHEDULE_FILE = "schedule_test.json"
else:
    SCHEDULE_FILE = "schedule.json"