import streamlit as st
import pandas as pd
import random
import time
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="Encontro Pharmic", 
    page_icon="🎉", 
    layout="centered",
    initial_sidebar_state="expanded"
)

# Sessões de controle
if "nomes_restantes" not in st.session_state:
    st.session_state.nomes_restantes = []
if "sorteados" not in st.session_state:
    st.session_state.sorteados = []
if "lista_carregada" not in st.session_state:
    st.session_state.lista_carregada = False
if "historico_sorteios" not in st.session_state:
    st.session_state.historico_sorteios = []
if "ultimo_sorteado" not in st.session_state:
    st.session_state.ultimo_sorteado = None
if "mostrar_resultado" not in st.session_state:
    st.session_state.mostrar_resultado = False

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #36B227;
        margin-bottom: 2rem;
    }
    .winner-animation {
        animation: fadeIn 1.2s ease-in-out;
        text-align: center;
        font-size: 72px;
        color: #28a745;
        font-weight: bold;
        padding: 20px;
        border-radius: 15px;
        background: linear-gradient(135deg, #f5f5f5, #e8f5e8);
        margin: 20px 0;
    }
    .countdown {
        text-align: center;
        color: #ff6600;
        font-size: 36px;
        font-weight: bold;
        padding: 20px;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: scale(0.8) rotate(-2deg); }
        to { opacity: 1; transform: scale(1) rotate(0deg); }
    }
</style>
""", unsafe_allow_html=True)

# Cabeçalho
st.markdown("<h1 class='main-header' style='color: #FF5733;'>🎉 SORTEIO ENCONTRO PHARMIC</h1>", unsafe_allow_html=True)

# Sidebar para controles
with st.sidebar:
    st.header("⚙️ Controles")
    
    # Reiniciar sorteio
    if st.button("🔄 Reiniciar Sorteio", use_container_width=True):
        st.session_state.nomes_restantes = st.session_state.nomes_restantes + st.session_state.sorteados
        st.session_state.sorteados = []
        st.session_state.historico_sorteios = []
        st.session_state.ultimo_sorteado = None
        st.session_state.mostrar_resultado = False
        st.rerun()

# Upload do CSV
if not st.session_state.lista_carregada:
    st.header("📁 Carregar Lista de Participantes")
    arquivo = st.file_uploader("Enviar arquivo CSV", type=["csv"], help="Arquivo CSV com um nome por linha")

    if arquivo is not None:
        try:
            df = pd.read_csv(arquivo, header=None, encoding="utf-8")
            nomes = df[0].dropna().astype(str).str.strip().tolist()
            
            if nomes:
                # Remove duplicatas mantendo a ordem
                nomes_unicos = []
                for nome in nomes:
                    if nome not in nomes_unicos:
                        nomes_unicos.append(nome)
                
                st.session_state.nomes_restantes = nomes_unicos.copy()
                st.session_state.sorteados = []
                st.session_state.lista_carregada = True
                st.session_state.historico_sorteios = []
                
                st.rerun()
                
            else:
                st.warning("⚠️ Nenhum nome válido encontrado no arquivo.")
                
        except Exception as e:
            st.error(f"❌ Erro ao ler o arquivo CSV: {e}")

# Função de sorteio
if st.session_state.lista_carregada:
    
    # Se não está mostrando resultado, mostra apenas o botão de sorteio
    if not st.session_state.mostrar_resultado:
        st.header("🎯 Realizar Sorteio")
        
        # Botão de sorteio centralizado
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            sortear_btn = st.button(
                "🎯 SORTEAR NOME", 
                use_container_width=True, 
                type="primary",
                disabled=not st.session_state.nomes_restantes
            )
        
        if not st.session_state.nomes_restantes:
            st.warning("⚠️ Todos os nomes já foram sorteados!")
            st.balloons()
        
        if sortear_btn and st.session_state.nomes_restantes:
            # Contagem regressiva
            countdown_placeholder = st.empty()
            for i in range(3, 0, -1):
                countdown_placeholder.markdown(
                    f"<div class='countdown'>⏳ Sorteando em {i}...</div>",
                    unsafe_allow_html=True
                )
                time.sleep(1)
            countdown_placeholder.empty()

            # Sorteio
            sorteado = random.choice(st.session_state.nomes_restantes)
            st.session_state.nomes_restantes.remove(sorteado)
            st.session_state.sorteados.append(sorteado)
            st.session_state.ultimo_sorteado = sorteado
            st.session_state.mostrar_resultado = True
            
            # Registrar no histórico com timestamp
            timestamp = datetime.now().strftime("%H:%M:%S")
            st.session_state.historico_sorteios.append((sorteado, timestamp))
            
            st.rerun()
    
    # Se está mostrando resultado, mostra apenas o botão e o nome sorteado
    else:
        # Container principal centralizado
        main_container = st.container()
        
        with main_container:
            # Botão para novo sorteio
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                novo_sorteio_btn = st.button(
                    "🎯 NOVO SORTEIO", 
                    use_container_width=True, 
                    type="primary",
                    disabled=not st.session_state.nomes_restantes
                )
            
            # Mostrar resultado com animação
            st.markdown(f'<div class="winner-animation">🎉 {st.session_state.ultimo_sorteado} 🎉</div>', unsafe_allow_html=True)
            
            # Efeitos visuais
            st.balloons()
        
        if novo_sorteio_btn:
            st.session_state.mostrar_resultado = False
            st.rerun()