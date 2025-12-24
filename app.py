import streamlit as st
import time
import random

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="¿Sorpresa o Broma?",
    page_icon="🎁",
    layout="centered"
)

# --- ESTILOS CSS (Mejorados para teclado QWERTY y iPhone) ---
st.markdown("""
    <style>
    /* Contenedor de la frase */
    .letter-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 5px;
        margin-bottom: 20px;
        padding: 5px;
    }
    
    /* Cuadraditos de letras del panel */
    .letter-box {
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 5px; 
        width: 30px; /* Un poco más pequeño para asegurar que quepa la frase */
        height: 40px;
        background-color: #ffffff;
        color: #000000;
        font-size: 18px;
        font-weight: bold;
        border-radius: 5px;
        border: 2px solid #333;
        box-shadow: 1px 1px 3px rgba(0,0,0,0.1);
    }
    
    .space-box { width: 10px; display: inline-block; }

    /* ESTILO DEL TECLADO (Botones más compactos y cuadrados) */
    div.stButton > button {
        width: 100%;
        min-width: 0px !important; /* Importante para móviles */
        padding: 0px !important;
        height: 45px !important;
        font-size: 16px !important;
        font-weight: 600;
        margin: 2px 0px;
        border-radius: 8px;
        border: 1px solid #ccc;
    }
    
    /* Estilo para el botón de resolver */
    .solve-btn { border: 2px solid #4CAF50 !important; color: #4CAF50 !important; }
    
    /* Títulos */
    h1 { text-align: center; font-size: 1.5rem !important; }
    </style>
""", unsafe_allow_html=True)

# --- CONFIGURACIÓN DEL JUEGO ---
SECRET_PHRASE = "NOS VAMOS AL CAMINITO DEL REY"
HINT_TEXT = "Se necesitan cascos y valentía. (Aunque sea 28 de diciembre... ¡NO es broma!)."

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

def solve_puzzle():
    # Rellena todas las letras
    for char in SECRET_PHRASE:
        if char != " ":
            st.session_state.guessed_letters.add(char)

# --- INTERFAZ DEL JUEGO ---

if not st.session_state.game_over:
    st.title("🎁 Misión: 28 de Diciembre 🎁")
    st.write("Adivinad el regalo letra a letra o escribid la frase si la sabéis.")

    # 1. EL PANEL
    st.markdown(display_word(SECRET_PHRASE, st.session_state.guessed_letters), unsafe_allow_html=True)

    # 2. CAJA PARA RESOLVER DIRECTAMENTE
    st.write("---")
    col_input, col_btn = st.columns([3, 1])
    with col_input:
        guess_attempt = st.text_input("¿Te la sabes?", placeholder="Escribe aquí la frase completa...", label_visibility="collapsed")
    with col_btn:
        if st.button("Resolver"):
            if guess_attempt and guess_attempt.upper().strip() == SECRET_PHRASE:
                solve_puzzle()
                st.rerun()
            else:
                st.toast("❌ ¡Incorrecto! Sigue intentando.", icon="🚫")

    # 3. PISTA Y COMODÍN
    with st.expander("🔍 Opciones de ayuda (Pista / Comodín)"):
        st.info(HINT_TEXT)
        if st.button("🃏 Usar Comodín (Destapar 1 letra)"):
            missing = [c for c in SECRET_PHRASE if c not in st.session_state.guessed_letters and c != " "]
            if missing:
                new_l = random.choice(missing)
                st.session_state.guessed_letters.add(new_l)
                st.toast(f"¡Salió la {new_l}!", icon="🎉")
                st.rerun()

    st.write("---")
    st.caption("Teclado:")

# --- TECLADO TIPO QWERTY (MEJORADO) ---
if not st.session_state.game_over:
    # Definimos las filas del teclado
    row1 = "QWERTYUIOP"
    row2 = "ASDFGHJKLÑ"
    row3 = "ZXCVBNM"
    
    # Función para renderizar una fila
    def render_row(keys_string):
        # Creamos tantas columnas como letras tenga la fila
        cols = st.columns(len(keys_string), gap="small")
        for i, letter in enumerate(keys_string):
            disabled = letter in st.session_state.guessed_letters
            if cols[i].button(letter, key=letter, disabled=disabled):
                st.session_state.guessed_letters.add(letter)
                st.rerun()

    # Renderizamos las 3 filas
    render_row(row1)
    render_row(row2)
    
    # Para la última fila, usamos columnas vacías a los lados para centrarla visualmente
    c_left, c_center, c_right = st.columns([1.5, 7, 1.5]) 
    with c_center:
        # Renderizamos la fila Z-M dentro de la columna central
        cols_r3 = st.columns(len(row3), gap="small")
        for i, letter in enumerate(row3):
            disabled = letter in st.session_state.guessed_letters
            if cols_r3[i].button(letter, key=letter, disabled=disabled):
                st.session_state.guessed_letters.add(letter)
                st.rerun()

# --- PANTALLA FINAL (VICTORIA) ---
if check_win(SECRET_PHRASE, st.session_state.guessed_letters):
    st.session_state.game_over = True
    
    st.markdown("---")
    time.sleep(0.2)
    st.balloons()
    
    st.markdown(f"<h1 style='color: #4CAF50; text-align:center;'>¡CORRECTO!</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center; margin-top:0;'>{SECRET_PHRASE}</h3>", unsafe_allow_html=True)
    
    # IMAGEN ARREGLADA (URL fiable de Unsplash)
    # Esta imagen es de un desfiladero similar (típico para representar Caminito del Rey en webs gratuitas)
    st.image("https://images.unsplash.com/photo-1597920787680-7b2498263721?q=80&w=1000&auto=format&fit=crop", 
             caption="Vértigo, paisajes y adrenalina.", use_column_width=True)
    
    st.success("¡Regalo oficial! Preparad las mochilas.")
    st.info("📅 **Fecha:** Sábado, 28 de Diciembre.\n\n👟 **Nota:** Llevad calzado deportivo.")
    
    if st.button("Reiniciar Juego"):
        st.session_state.guessed_letters = set()
        st.session_state.game_over = False
        st.rerun()
