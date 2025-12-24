import streamlit as st
import time
import random
import requests

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="El Desafío de Lalo",
    page_icon="⏱️",
    layout="centered"
)

# --- ESTILOS CSS ---
st.markdown("""
    <style>
    /* PANEL DE LETRAS */
    .board-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 5px;
        margin-bottom: 20px;
        background-color: #263238;
        padding: 15px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .letter-box {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 35px;
        height: 45px;
        background-color: #ffffff;
        color: #000000;
        font-size: 20px;
        font-weight: bold;
        border-radius: 5px;
        border: 2px solid #333;
    }
    .letter-hidden { background-color: #cfd8dc; color: transparent; }
    .space-box { width: 15px; }

    /* PREGUNTA Y RELOJ */
    .question-box {
        font-size: 20px;
        font-weight: bold;
        text-align: center;
        margin-top: 10px;
        margin-bottom: 10px;
        color: #1565C0;
        background-color: #E3F2FD;
        padding: 20px;
        border-radius: 15px;
        border: 2px solid #2196F3;
    }
    
    /* ZONA DE RESOLVER (DESTACADA) */
    .solve-zone {
        background-color: #FFF3E0;
        border: 2px dashed #FF9800;
        padding: 15px;
        border-radius: 10px;
        margin-top: 30px;
        text-align: center;
    }

    /* BOTONES */
    div.stButton > button {
        width: 100%;
        height: 60px !important;
        font-size: 18px !important;
        font-weight: 500;
        border-radius: 10px;
        border: 1px solid #ddd;
        transition: transform 0.1s;
    }
    div.stButton > button:active { transform: scale(0.98); }

    /* BOTÓN REVELAR */
    .reveal-btn-style {
        background-color: #FFD700 !important;
        color: #000 !important;
        font-weight: 800 !important;
        border: 3px solid #ff8f00 !important;
    }

    /* TARJETA FINAL */
    .winner-card {
        background-color: #f0fdf4;
        border: 3px solid #4CAF50;
        border-radius: 20px;
        padding: 20px;
        text-align: center;
        margin-top: 10px;
        animation: fadeIn 1s;
    }
    .winner-phrase { color: #1b5e20; font-size: 24px; font-weight: 900; margin: 15px 0; text-transform: uppercase; }
    </style>
""", unsafe_allow_html=True)

# --- JAVASCRIPT PARA EL CRONÓMETRO VISUAL ---
# Esto inyecta un contador en pantalla que no depende de Python
def show_timer():
    timer_html = """
        <div id="timer_div" style="font-size:24px; font-weight:bold; color:red; text-align:center; margin-bottom:10px;">
            ⏱️ Tiempo: <span id="time_left">30</span>s
        </div>
        <script>
            var timeleft = 30;
            var downloadTimer = setInterval(function(){
            if(timeleft <= 0){
                clearInterval(downloadTimer);
                document.getElementById("time_left").innerHTML = "0";
                document.getElementById("timer_div").style.color = "darkred";
                document.getElementById("timer_div").innerHTML = "⌛ ¡TIEMPO AGOTADO!";
            } else {
                document.getElementById("time_left").innerHTML = timeleft;
            }
            timeleft -= 1;
            }, 1000);
        </script>
    """
    st.components.v1.html(timer_html, height=50)

# --- DATOS DEL JUEGO ---
SECRET_PHRASE = "NOS VAMOS AL CAMINITO DEL REY"
TEAM_NAMES = "María, Mamá, Lala, Miguel y Lalo"
IMAGE_URL = "https://images.unsplash.com/photo-1597920787680-7b2498263721?q=80&w=1000&auto=format&fit=crop"

# --- PREGUNTAS ---
questions = [
    {
        "q": "1. ¿Cuál es el deporte que MÁS he practicado?",
        "options": ["Fútbol", "Golf", "Tenis", "Pádel"],
        "answer": "Tenis",
        "error": "❌ ¡Falso! Ese lo he tocado poco."
    },
    {
        "q": "2. ¿En qué año me saqué el carné de conducir?",
        "options": ["2017", "2018", "2019", "2020"],
        "answer": "2019",
        "error": "❌ Incorrecto. Yo iba en bus en esa época."
    },
    {
        "q": "3. ¿Qué Máster estudio actualmente?",
        "options": ["Banca Privada", "Big Data e IA", "Asesoramiento Financiero", "Dirección Bancaria"],
        "answer": "Big Data e IA",
        "error": "❌ ¡No! Buscad algo más 'tech'."
    },
    {
        "q": "4. ¿Qué prefiero comer si me dais a elegir?",
        "options": ["Pizza 2x1", "Buffet de Sushi", "Cachopo", "Chuleta de 1,5kg"],
        "answer": "Chuleta de 1,5kg",
        "error": "❌ Rico, pero... prefiero la carne."
    },
    {
        "q": "5. ¿Qué competiciones haré en 2026?",
        "options": ["Media maratón Madrid", "Desafío Guerreros", "Hyrox Málaga", "Todas las anteriores"],
        "answer": "Todas las anteriores",
        "error": "❌ ¡Te quedas corto! Las haré todas."
    }
]

# --- ESTADO ---
if 'current_q_index' not in st.session_state:
    st.session_state.current_q_index = 0
if 'revealed_indices' not in st.session_state:
    st.session_state.revealed_indices = set()
if 'phase' not in st.session_state:
    st.session_state.phase = 'question'
if 'game_won' not in st.session_state:
    st.session_state.game_won = False
if 'q_start_time' not in st.session_state:
    st.session_state.q_start_time = time.time()

# --- LÓGICA DE REVELADO ---
total_letters_count = len([c for c in SECRET_PHRASE if c != " "])
letters_per_turn = (total_letters_count // len(questions)) + 1

def reveal_random_letters():
    hidden_indices = [i for i, char in enumerate(SECRET_PHRASE) 
                      if char != " " and i not in st.session_state.revealed_indices]
    if hidden_indices:
        to_reveal = random.sample(hidden_indices, min(len(hidden_indices), letters_per_turn))
        st.session_state.revealed_indices.update(to_reveal)

def draw_board():
    html = '<div class="board-container">'
    for i, char in enumerate(SECRET_PHRASE):
        if char == " ":
            html += '<div class="space-box"></div>'
        elif i in st.session_state.revealed_indices or st.session_state.game_won:
            bg = "#4CAF50" if st.session_state.game_won else "#ffffff"
            color = "#fff" if st.session_state.game_won else "#000"
            html += f'<div class="letter-box" style="background-color: {bg}; color: {color};">{char}</div>'
        else:
            html += '<div class="letter-box letter-hidden">_</div>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)

# --- PANTALLA DE VICTORIA ---
if st.session_state.game_won:
    st.balloons()
    time.sleep(0.5)
    st.markdown(f"""
        <div class="winner-card">
            <div class="winner-title">🎉 ¡ENHORABUENA! 🎉</div>
            <p>Habéis desbloqueado el regalo:</p>
            <div class="winner-phrase">{SECRET_PHRASE}</div>
            <div style="margin-top:15px; padding:10px; background:rgba(255,255,255,0.7); border-radius:10px;">
                <strong>👥 Aventureros:</strong><br>{TEAM_NAMES}
            </div>
        </div>
    """, unsafe_allow_html=True)
    try:
        response = requests.head(IMAGE_URL, timeout=3)
        if response.status_code == 200:
             st.image(IMAGE_URL, use_column_width=True)
    except: pass
    st.success("✅ Regalo confirmado (No es broma).")
    st.info("📅 Fecha: Sábado, 28 de Diciembre.")
    if st.button("🔄 Reiniciar"):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()
    st.stop()

# --- INTERFAZ JUEGO ---
st.title("⏱️ Misión: Contrarreloj")
draw_board()

# FASE DE PREGUNTA
if st.session_state.phase == 'question':
    # Reiniciar reloj si acabamos de entrar a la pregunta
    # (Usamos un truco para detectar si es la primera vez que se renderiza esta pregunta)
    current_time = time.time()
    # Si el tiempo guardado es "muy viejo" (de la pregunta anterior), lo reseteamos
    # Nota: Simplificamos reseteando el start_time al cambiar de index, pero aquí
    # lo hacemos visualmente con el componente.
    
    # Mostramos el cronómetro VISUAL
    show_timer()
    
    current_idx = st.session_state.current_q_index
    q_data = questions[current_idx]
    
    st.markdown(f'<div class="question-box">Pregunta {current_idx + 1}:<br>{q_data["q"]}</div>', unsafe_allow_html=True)
    
    # Guardamos el tiempo de inicio de esta pregunta específica si no está fijado
    if f"start_q_{current_idx}" not in st.session_state:
        st.session_state[f"start_q_{current_idx}"] = time.time()
    
    # Botones
    for option in q_data["options"]:
        if st.button(option):
            # 1. Comprobar TIEMPO
            elapsed = time.time() - st.session_state[f"start_q_{current_idx}"]
            
            # Damos un margen de 32 segundos por retardos de red
            if elapsed > 32:
                st.error("⌛ ¡TIEMPO AGOTADO! Habéis tardado demasiado.")
                st.toast("Pierdes el turno de revelar letras...", icon="🐢")
                time.sleep(2)
                # Pasan a la siguiente pero SIN PREMIO
                if st.session_state.current_q_index + 1 < len(questions):
                    st.session_state.current_q_index += 1
                    st.rerun()
                else:
                    # Si era la última, dejamos que resuelvan abajo
                    st.warning("¡Se acabaron las preguntas! Tenéis que resolver a mano.")
            
            # 2. Comprobar RESPUESTA
            elif option == q_data["answer"]:
                st.session_state.phase = 'reward'
                st.rerun()
            else:
                st.error(q_data["error"])

# FASE DE PREMIO
elif st.session_state.phase == 'reward':
    st.success("✅ ¡A TIEMPO Y CORRECTO!")
    st.markdown("<h3 style='text-align: center;'>¡Ganasteis letras!</h3>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        if st.button("🔓 REVELAR PISTAS", type="primary"):
            reveal_random_letters()
            if st.session_state.current_q_index + 1 < len(questions):
                st.session_state.current_q_index += 1
                st.session_state.phase = 'question'
            else:
                # Se acabaron las preguntas, solo queda resolver
                pass 
            st.rerun()

# --- ZONA PARA RESOLVER (SIEMPRE VISIBLE ABAJO) ---
st.markdown("<div class='solve-zone'>", unsafe_allow_html=True)
st.write("### 🧠 ¿Ya tenéis la frase?")
st.write("Si falláis, no pasa nada, pero cuidado con los nervios.")

col_in, col_bt = st.columns([3, 1])
with col_in:
    guess = st.text_input("Escribe la solución aquí:", key="solver", label_visibility="collapsed")
with col_bt:
    if st.button("🚀 RESOLVER"):
        if guess.upper().strip() == SECRET_PHRASE:
            st.session_state.game_won = True
            st.rerun()
        else:
            st.toast("❌ ¡Incorrecto!", icon="🚫")
            st.error("Esa no es la frase. ¡Seguid jugando!")
st.markdown("</div>", unsafe_allow_html=True)
