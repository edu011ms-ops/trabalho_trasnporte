import streamlit as st 
import numpy as np
import matplotlib.pyplot as plt

st.title("Calculadora de Transporte Mais Vantajoso")

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

peso_custo = st.slider("Importância do custo", 0.0, 10.0, 6.0)
peso_tempo = st.slider("Importância do tempo", 0.0, 10.0, 4.0)

#normalização (garante que somam 1)
total = peso_custo + peso_tempo

if total == 0:
    st.warning("Escolaha pelo menos uma prefêrencia")
else:
    peso_custo /= total
    peso_tempo /= total

if st.button("Calcular melhor opção"):
    
    if len(dados) == 0:
        st.warning("Selecione pelo menos um meio de transporte!")
    else:
        nomes = list(dados.keys())
        custos = np.array([dados[n]["custo"] for n in nomes])
        tempos = np.array([dados[n]["tempo"] for n in nomes])

        # normalizar valores (esla comparavel)
        
        custos_norm =(custos - np.min(custos)) / (np.max(custos) if np.min(custos)) != np.min(custos) else custos
        tempos_norm =(tempos - np.min(tempos)) / (np.max(tmepos) if np.min(tempos)) != np.min(tempos) else tempos

        #inverter (quanto menor melhor)
        custos_norm = 1 - custos_norm
        tempos_norm = 1 - tempos_norm

        #calculo final
        vantagens = custos_norm * peso_custo + tempos_norm * peso_tempo

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
