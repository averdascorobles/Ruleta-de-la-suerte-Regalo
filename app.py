import streamlit as st
import time
import random

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="¿Sorpresa o Broma?",
    page_icon="🎁",
    layout="centered" 
)

# --- ESTILOS CSS (Optimizado iPhone 15 Pro Max) ---
st.markdown("""
    <style>
    /* Contenedor flexible de letras */
    .letter-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 6px;
        margin-bottom: 20px;
        padding: 5px;
    }
    
    /* Cuadraditos de letras */
    .letter-box {
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 8px 10px; 
        min-width: 32px; 
        min-height: 42px;
        background-color: #ffffff;
        color: #000000;
        font-size: 20px;
        font-weight: bold;
        border-radius: 6px;
        border: 2px solid #333;
        box-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }

    .space-box {
        width: 12px;
        height: auto;
        display: inline-block;
    }

    /* Botones del teclado */
    div.stButton > button {
        width: 100%;
        border-radius: 10px;
        height: 50px !important;
        font-size: 18px;
        font-weight: 600;
        margin-top: 4px;
        border: 1px solid #ddd;
    }
    
    /* Botón de Comodín especial */
    .wildcard-btn {
        border: 2px solid #FFD700 !important;
        background-color: #fff9c4 !important;
        color: #b7950b !important;
    }

    h1 {
        text-align: center;
        font-size: 1.6rem !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- CONFIGURACIÓN DEL JUEGO ---
SECRET_PHRASE = "NOS VAMOS AL CAMINITO DEL REY"

# Pista criptica
HINT_TEXT = "Se necesitan cascos y valentía. (Y aunque sea 28 de diciembre... ¡esto NO es una inocentada!)."

# Estado del juego
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

def use_wildcard():
    # Buscar letras que faltan
    missing_chars = [char for char in SECRET_PHRASE if char not in st.session_state.guessed_letters and char != " "]
    if missing_chars:
        # Elegir una al azar y añadirla
        new_letter = random.choice(missing_chars)
        st.session_state.guessed_letters.add(new_letter)
        st.toast(f"🃏 ¡Comodín usado! Ha salido la letra: {new_letter}", icon="🎉")

# --- INTERFAZ ---

if not st.session_state.game_over:
    st.title("🎁 Misión: 28 de Diciembre 🎁")
    st.write("Adivinad dónde vamos. ¡Cuidado que hoy es un día peligroso para creerse cosas!")

    # Panel
    st.markdown(display_word(SECRET_PHRASE, st.session_state.guessed_letters), unsafe_allow_html=True)

    # Zona de Ayudas
    col_pista, col_comodin = st.columns([1, 1])
    
    with col_pista:
        with st.expander("🕵️ Ver Pista"):
            st.info(HINT_TEXT)
            
    with col_comodin:
        # Botón Comodín
        if st.button("🃏 Usar Comodín"):
            use_wildcard()
            st.rerun()

    st.write("---")

# --- TECLADO ---
if not st.session_state.game_over:
    alphabet = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
    cols = st.columns(6) # 6 columnas para mejor tamaño en iPhone Max
    
    for index, letter in enumerate(alphabet):
        disabled = letter in st.session_state.guessed_letters
        if cols[index % 6].button(letter, key=letter, disabled=disabled):
            st.session_state.guessed_letters.add(letter)
            st.rerun()

# --- PANTALLA FINAL (VICTORIA) ---
if check_win(SECRET_PHRASE, st.session_state.guessed_letters):
    st.session_state.game_over = True
    
    st.markdown("---")
    time.sleep(0.3)
    st.balloons()
    
    st.markdown(f"<h1 style='color: #4CAF50;'>¡CORRECTO!</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center;'>{SECRET_PHRASE}</h3>", unsafe_allow_html=True)
    
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c2/Caminito_del_Rey_-_Gorge.jpg/1024px-Caminito_del_Rey_-_Gorge.jpg", 
             caption="Vértigo, paisajes y adrenalina.", use_column_width=True)
    
    st.success("¡Regalo oficial! No es una inocentada 😉")
    
    st.info("📅 **Fecha:** Sábado, 28 de Diciembre.\n\n👟 **Nota:** Llevad calzado deportivo bien atado.")


