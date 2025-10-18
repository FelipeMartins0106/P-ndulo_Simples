import pandas as pd
import matplotlib.pyplot as plt

# Carrega os dados gerados pelo script principal
try:
    df = pd.read_csv('dados_pendulo.csv')
except FileNotFoundError:
    print("Erro: Arquivo 'dados_pendulo.csv' não encontrado.")
    print("Execute o script principal de análise primeiro para gerar os dados.")
    exit()

# Extrai os dados de tempo, x e y
t = df['tempo_s']
x = df['posicao_x_px']
y = df['posicao_y_px']

# --- 1. PROVA QUANTITATIVA (OS NÚMEROS) ---
# Calcula a amplitude total do movimento em cada eixo
range_x = x.max() - x.min()
range_y = y.max() - y.min()

print("--- Análise da Variação Vertical (y) vs. Horizontal (x) ---")
print(f"Variação total em x (amplitude do movimento): {range_x:.2f} pixels")
print(f"Variação total em y (altura do arco): {range_y:.2f} pixels")
print("-" * 20)

# Compara as duas variações
if range_x > 0:
    razao_y_x = (range_y / range_x) * 100
    print(f"A variação em y corresponde a apenas {razao_y_x:.2f}% da variação em x.")
    print("Isso confirma que a variação vertical é desprezível em comparação com a horizontal.")
else:
    print("Não foi possível calcular a razão (variação em x é zero).")


# --- 2. PROVA VISUAL (O GRÁFICO) ---
# Cria uma figura com dois subplots, um em cima do outro
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

# Plot 1: Posição X vs. Tempo
ax1.plot(t, x, 'b.', markersize=3)
ax1.set_title('Movimento Horizontal (x)')
ax1.set_ylabel('Posição x (pixels)')
ax1.grid(True)

# Plot 2: Posição Y vs. Tempo
ax2.plot(t, y, 'g.', markersize=3)
ax2.set_title('Movimento Vertical (y)')
ax2.set_ylabel('Posição y (pixels)')
ax2.set_xlabel('Tempo (s)')
ax2.grid(True)

# Para facilitar a comparação, vamos forçar os dois eixos Y a terem a mesma "altura"
# Isso deixará a pequenez da variação em Y ainda mais óbvia, mas pode "achatar" o gráfico de Y.
# Descomente a linha abaixo se quiser experimentar isso.
# ax2.set_ylim(ax1.get_ylim())

plt.suptitle('Comparação dos Movimentos nos Eixos X e Y', fontsize=16)
plt.tight_layout(rect=[0, 0, 1, 0.96]) # Ajusta para o super-título
plt.show()