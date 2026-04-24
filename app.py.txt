app.py + requirements.txt

# transport_app
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("Calculadora de Transporte Mais Vantajoso")

# Entrada do usuario
transportes = ["onibus", "carro", "bicicleta", "uber"]

dados = {}

st.subheader("Insira os dados:")

for t in transportes:
    st.write(f"### {t}")
    tempo = st.number_input(f"Tempo (min) - {t}", min_value=0, key=t+"tempo")
    custo = st.number_input(f"Custo (R$) - {t}", min_value=0.0, key=t+"custo")
    dados[t] = {"tempo": tempo, "custo": custo}

# Peso personalizado
st.subheader("Preferencia do usuário")
peso_custo = st.slider("Importancia do custo", 0.0, 1.0, 0.6)
peso_tempo = 1 - peso_custo

if st.button("Calcular melhor opcao"):
    nomes = list(dados.keys())
    custos = np.array([dados[n]["custo"] for n in nomes])
    tempos = np.array([dados[n]["tempo"] for n in nomes])

    vantagens = custos * peso_custo + tempos * peso_tempo

    melhor_idx = np.argmin(vantagens)

    st.success(f"Melhor opcao: {nomes[melhor_idx]}")

    # Grafico
    fig, ax = plt.subplots()
    ax.scatter(tempos, custos)

    for i in range(len(nomes)):
        ax.text(tempos[i], custos[i], nomes[i])

    ax.set_xlabel("Tempo")
    ax.set_ylabel("Custo")

    st.pyplot(fig)