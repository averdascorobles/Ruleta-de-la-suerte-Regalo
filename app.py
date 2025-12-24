import streamlit as st
import time
import random
import requests # Importamos esta librería para comprobar la conexión

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="¿Sorpresa o Broma?",
    page_icon="🎁",
    layout="centered"
)

# --- ESTILOS CSS (Compacto para iPhone) ---
st.markdown("""
    <style>
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
    h1 { text-align: center; font-size: 1.6rem !important; margin-bottom: 10px; }
    .stTextInput { margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- CONFIGURACIÓN ---
SECRET_PHRASE = "NOS VAMOS AL CAMINITO DEL REY"
HINT_TEXT = "Se necesitan cascos y valentía. (Aunque sea 28 de diciembre... ¡NO es broma!)."
# URL de una imagen de alta calidad y muy fiable (Unsplash)
IMAGE_URL = "https://images.unsplash.com/photo-1597920787680-7b2498263721?q=80&w=1000&auto=format&fit=crop"

# Estado
if 'guessed_letters' not in st.session_state:
    st.session_state.guessed_letters = set()
if 'game_over' not in st.session_state:
    st.session_state.game_over = False

# --- FUNCIONES ---
def display_word(phrase, guessed):
    html_content = '<div class="letter-container">'
    for char in phrase:
        if char == " ":
            html_content += '<div class="space-box"></div>'
        elif char in guessed:
            html_content += f'<div class="letter-box" style="background-color: #4CAF50; color: white; border-color: #2e7d32;">{char}</div>'
        else:
            html_content += '<div class="letter-box">_</div>'
    html_content += "</div>"
    return html_content

def check_win(phrase, guessed):
    phrase_no_spaces = phrase.replace(" ", "")
    return all(char in guessed for char in phrase_no_spaces)

def solve_puzzle():
    for char in SECRET_PHRASE:
        if char != " ":
            st.session_state.guessed_letters.add(char)

# --- INTERFAZ ---

if not st.session_state.game_over:
    st.title("🎁 Misión: 28 de Diciembre 🎁")
    st.write("Adivinad el regalo letra a letra o escribid la frase si la sabéis.")

    # 1. PANEL
    st.markdown(display_word(SECRET_PHRASE, st.session_state.guessed_letters), unsafe_allow_html=True)

    # 2. CAJA PARA RESOLVER
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

    # 3. PISTA Y COMODÍN
    with st.expander("🔍 Pista y Comodín"):
        st.info(HINT_TEXT)
        if st.button("🃏 Usar Comodín (Destapar 1 letra)"):
            missing = [c for c in SECRET_PHRASE if c not in st.session_state.guessed_letters and c != " "]
            if missing:
                new_l = random.choice(missing)
                st.session_state.guessed_letters.add(new_l)
                st.toast(f"¡Letra destapada: {new_l}!", icon="🎉")
                st.rerun()
    
    st.write("---")

# --- TECLADO (GRID COMPACTO) ---
if not st.session_state.game_over:
    alphabet = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
    cols = st.columns(6)
    for index, letter in enumerate(alphabet):
        disabled = letter in st.session_state.guessed_letters
        if cols[index % 6].button(letter, key=letter, disabled=disabled):
            st.session_state.guessed_letters.add(letter)
            st.rerun()

# --- PANTALLA FINAL ---
if check_win(SECRET_PHRASE, st.session_state.guessed_letters):
    st.session_state.game_over = True
    
    st.markdown("---")
    time.sleep(0.2)
    st.balloons()
    
    st.markdown(f"<h1 style='color: #4CAF50; text-align:center;'>¡CORRECTO!</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center; margin-top:0;'>{SECRET_PHRASE}</h3>", unsafe_allow_html=True)
    
    # --- INTENTO DE CARGAR IMAGEN ONLINE CON SEGURIDAD ---
    try:
        # Intentamos "tocar" la URL para ver si responde (timeout rápido de 3 seg)
        response = requests.head(IMAGE_URL, timeout=3)
        
        # Si responde OK (código 200), mostramos la imagen
        if response.status_code == 200:
             st.image(IMAGE_URL, caption="Vértigo, paisajes y adrenalina.", use_column_width=True)
        # Si responde con error (ej. 404 not found), no hacemos nada (pass)
        else:
            pass 
    except Exception:
        # Si falla la conexión (ej. no hay internet), no hacemos nada (pass)
        pass
    # -----------------------------------------------------

    st.success("¡Regalo oficial! Preparad las mochilas.")
    st.info("📅 **Fecha:** Sábado, 28 de Diciembre.\n\n👟 **Nota:** Llevad calzado deportivo.")
    
    if st.button("Reiniciar Juego"):
        st.session_state.guessed_letters = set()
        st.session_state.game_over = False
        st.rerun()
