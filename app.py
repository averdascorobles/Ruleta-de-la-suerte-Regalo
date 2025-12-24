import streamlit as st
import time
import random
import requests

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="¿Sorpresa o Broma?",
    page_icon="🎁",
    layout="centered"
)

# --- ESTILOS CSS (Diseño Tarjeta y Móvil) ---
st.markdown("""
    <style>
    /* Estilo para el juego (letras) */
    .letter-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 4px;
        margin-bottom: 15px;
        padding: 5px;
    }
    .letter-box {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 32px;
        height: 42px;
        background-color: #ffffff;
        color: #000000;
        font-size: 18px;
        font-weight: bold;
        border-radius: 6px;
        border: 2px solid #333;
        box-shadow: 1px 1px 3px rgba(0,0,0,0.15);
    }
    .space-box { width: 10px; display: inline-block; }

    /* Estilo botones teclado */
    div.stButton > button {
        width: 100%;
        padding: 0px !important;
        height: 50px !important; 
        font-size: 18px !important;
        font-weight: 600;
        margin: 2px 0px; 
        border-radius: 8px;
        border: 1px solid #ccc;
        background-color: #f9f9f9;
    }

    /* ESTILO DE LA TARJETA FINAL (POP-UP) */
    .winner-card {
        background-color: #f0fdf4; /* Fondo verde muy clarito */
        border: 2px solid #4CAF50; /* Borde verde */
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        margin-top: 10px;
        margin-bottom: 20px;
    }
    .winner-title {
        color: #2e7d32;
        font-size: 28px;
        font-weight: bold;
        margin-bottom: 5px;
    }
    .winner-phrase {
        color: #1b5e20;
        font-size: 24px;
        font-weight: bold;
        margin: 15px 0;
        text-transform: uppercase;
        line-height: 1.2;
    }
    .team-section {
        margin-top: 15px;
        font-size: 16px;
        color: #333;
        background-color: rgba(255,255,255,0.6);
        padding: 10px;
        border-radius: 10px;
    }
    
    h1 { text-align: center; font-size: 1.6rem !important; }
    </style>
""", unsafe_allow_html=True)

# --- CONFIGURACIÓN ---
SECRET_PHRASE = "NOS VAMOS AL CAMINITO DEL REY"
HINT_TEXT = "Se necesitan cascos y valentía. (Aunque sea 28 de diciembre... ¡NO es broma!)."
# NOMBRES DE LOS VIAJEROS
TEAM_NAMES = "María, Mamá, Lala, Miguel y Lalo"
# Imagen segura (Unsplash)
IMAGE_URL = "https://images.unsplash.com/photo-1597920787680-7b2498263721?q=80&w=1000&auto=format&fit=crop"

# --- ESTADO DEL JUEGO ---
if 'guessed_letters' not in st.session_state:
    st.session_state.guessed_letters = set()
if 'game_over' not in st.session_state:
    st.session_state.game_over = False

# --- FUNCIONES ---
def check_win(phrase, guessed):
    phrase_no_spaces = phrase.replace(" ", "")
    return all(char in guessed for char in phrase_no_spaces)

def solve_puzzle():
    for char in SECRET_PHRASE:
        if char != " ":
            st.session_state.guessed_letters.add(char)
    st.session_state.game_over = True

# --- LÓGICA PRINCIPAL ---

# 1. PANTALLA FINAL (POP-UP DE VICTORIA)
if st.session_state.game_over:
    st.balloons()
    
    # Tarjeta con los nombres incluidos
    st.markdown(f"""
        <div class="winner-card">
            <div class="winner-title">🎉 ¡FELICIDADES! 🎉</div>
            <p style="margin:0;">Destino desbloqueado:</p>
            <div class="winner-phrase">{SECRET_PHRASE}</div>
            <div class="team-section">
                <strong>👥 Aventureros:</strong><br>
                {TEAM_NAMES}
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Imagen con seguridad anti-fallos
    try:
        response = requests.head(IMAGE_URL, timeout=3)
        if response.status_code == 200:
             st.image(IMAGE_URL, use_column_width=True)
    except Exception:
        pass 
        
    st.success("✅ Regalo confirmado. ¡No es una inocentada!")
    st.info("📅 **Fecha:** Sábado, 28 de Diciembre.\n\n👟 **Nota:** Llevad calzado deportivo.")
    
    if st.button("🔄 Jugar otra vez"):
        st.session_state.guessed_letters = set()
        st.session_state.game_over = False
        st.rerun()
        
    st.stop() # Detiene el resto para que solo se vea la victoria

# 2. PANTALLA DE JUEGO
st.title("🎁 Misión: 28 de Diciembre 🎁")
st.write("Adivinad el regalo letra a letra o escribid la frase.")

# Panel
html_content = '<div class="letter-container">'
for char in SECRET_PHRASE:
    if char == " ":
        html_content += '<div class="space-box"></div>'
    elif char in st.session_state.guessed_letters:
        html_content += f'<div class="letter-box" style="background-color: #4CAF50; color: white;">{char}</div>'
    else:
        html_content += '<div class="letter-box">_</div>'
html_content += "</div>"
st.markdown(html_content, unsafe_allow_html=True)

# Resolver Rápido
col_in, col_bt = st.columns([3, 1])
with col_in:
    guess = st.text_input("Resolver", placeholder="Escribe la frase...", label_visibility="collapsed")
with col_bt:
    if st.button("Validar"):
        if guess and guess.upper().strip() == SECRET_PHRASE:
            solve_puzzle()
            st.rerun()
        else:
            st.toast("❌ Incorrecto", icon="🚫")

# Ayudas
with st.expander("🔍 Pista y Comodín"):
    st.info(HINT_TEXT)
    if st.button("🃏 Usar Comodín"):
        missing = [c for c in SECRET_PHRASE if c not in st.session_state.guessed_letters and c != " "]
        if missing:
            new_l = random.choice(missing)
            st.session_state.guessed_letters.add(new_l)
            if check_win(SECRET_PHRASE, st.session_state.guessed_letters):
                st.session_state.game_over = True
            st.rerun()

st.write("---")

# Teclado (Compacto)
alphabet = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
cols = st.columns(6)
for index, letter in enumerate(alphabet):
    disabled = letter in st.session_state.guessed_letters
    if cols[index % 6].button(letter, key=letter, disabled=disabled):
        st.session_state.guessed_letters.add(letter)
        if check_win(SECRET_PHRASE, st.session_state.guessed_letters):
            st.session_state.game_over = True
        st.rerun()

