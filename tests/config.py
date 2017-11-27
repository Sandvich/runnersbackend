BASE_URL = "http://localhost:5000"
LOGIN_URL = BASE_URL + "/api/login"
CREATE_PC_URL = BASE_URL + "/api/pcs"
CREATE_NPC_URL = BASE_URL + "/api/npcs"

WORKING_PC = {"name": "Serra", "description": "Serra is a wolf shifter who flies a helicopter with a massive fuck-off gun.", "karma": 15, "nuyen": 20000}
WORKING_NPC = {"name": "someone", "description": "something", "status": "Active", "security": "GM", "connection": 5}

admin_login = {"email": "sanchitsharma1@gmail.com", "password": "password"}
gm_login = admin_login
player_login = {"email": "test@test.com", "password": "password"}
