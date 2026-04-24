import streamlit as st 
import numpy as np
import matplotlib.pyplot as plt

st.title("🚗 Calculadora de Transporte Mais Vantajoso")

# Distância
distancia = st.number_input("Distância até o destino (km)", min_value=1.0, value=5.0)

# Lista de transportes
transportes = ["ônibus", "carro", "bicicleta", "uber"]

dados = {}

st.subheader("Selecione e insira os dados:")

for t in transportes:
    usar = st.checkbox(f"Usar {t}", value=True)
    
    if usar:
        st.write(f"### {t}")
        tempo = st.number_input(f"Tempo (min) - {t}", min_value=0, key=t+"tempo")
        custo = st.number_input(f"Custo base (R$) - {t}", min_value=0.0, key=t+"custo")
        
        custo_total = custo * distancia
        
        dados[t] = {"tempo": tempo, "custo": custo_total}

# Preferência do usuário
st.subheader("Preferência do usuário")
peso_custo = st.slider("Importância do custo", 0.0, 1.0, 0.6)
peso_tempo = 1 - peso_custo

if st.button("Calcular melhor opção"):
    
    if len(dados) == 0:
        st.warning("Selecione pelo menos um meio de transporte!")
    else:
        nomes = list(dados.keys())
        custos = np.array([dados[n]["custo"] for n in nomes])
        tempos = np.array([dados[n]["tempo"] for n in nomes])

        vantagens = custos * peso_custo + tempos * peso_tempo

        melhor_idx = np.argmin(vantagens)

        st.success(f"Melhor opção: {nomes[melhor_idx]}")

        # Gráfico
        fig, ax = plt.subplots()
        ax.scatter(tempos, custos)

        # destacar melhor
        ax.scatter(tempos[melhor_idx], custos[melhor_idx], s=200)

        for i in range(len(nomes)):
            ax.text(tempos[i], custos[i], nomes[i])

        ax.set_xlabel("Tempo")
        ax.set_ylabel("Custo")

        st.pyplot(fig)
