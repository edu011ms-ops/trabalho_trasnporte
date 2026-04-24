import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("Calculadora de Transporte Mais Vantajoso")

# Distância
distancia = st.number_input("Distância até o destino (km)", min_value=1.0, value=5.0)

# Dados base (velocidade km/h e custo por km)
transportes = {
    "ônibus": {"velocidade": 40, "custo_km": 0.5},
    "carro": {"velocidade": 60, "custo_km": 1.2},
    "bicicleta": {"velocidade": 15, "custo_km": 0},
    "uber": {"velocidade": 50, "custo_km": 2.0}
}

nomes = list(transportes.keys())

tempos = []
custos = []

for t in nomes:
    vel = transportes[t]["velocidade"]
    custo_km = transportes[t]["custo_km"]

    tempo = (distancia / vel) * 60  # minutos
    custo = distancia * custo_km

    tempos.append(tempo)
    custos.append(custo)

tempos = np.array(tempos)
custos = np.array(custos)

# Preferência do usuário
peso_custo = st.slider("Importância do custo", 0.0, 1.0, 0.6)
peso_tempo = 1 - peso_custo

vantagens = custos * peso_custo + tempos * peso_tempo

melhor_idx = np.argmin(vantagens)

st.success(f"Melhor opção: {nomes[melhor_idx]}")

# Gráfico
fig, ax = plt.subplots()
ax.scatter(tempos, custos)

# destacar melhor opção
ax.scatter(tempos[melhor_idx], custos[melhor_idx], s=200)

for i in range(len(nomes)):
    ax.text(tempos[i], custos[i], nomes[i])

ax.set_xlabel("Tempo (min)")
ax.set_ylabel("Custo (R$)")
ax.set_title("Comparação de Transporte")

st.pyplot(fig)
