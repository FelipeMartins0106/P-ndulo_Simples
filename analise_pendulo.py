# --- Importação de todas as bibliotecas necessárias ---
import cv2
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# ==============================================================================
# --- PARTE 1: PROCESSAMENTO DE VÍDEO E EXTRAÇÃO DE DADOS ---
# ==============================================================================

print("Iniciando a Parte 1: Processamento do vídeo...")

# --- Configuração ---
video_path = 'Pêndulo.mp4' 

cor_min = np.array([0, 0, 0]) 
cor_max = np.array([179, 80, 80])


# --- Processamento ---
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print(f"Erro: Não foi possível abrir o vídeo '{video_path}'")
    exit()

fps = cap.get(cv2.CAP_PROP_FPS)
dados = []
frame_num = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mascara = cv2.inRange(hsv, cor_min, cor_max)
    
    contornos, _ = cv2.findContours(mascara, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if len(contornos) > 0:
        c = max(contornos, key=cv2.contourArea)
        M = cv2.moments(c)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            
            tempo = frame_num / fps
            dados.append([tempo, cx, cy])
        
    frame_num += 1

cap.release()

# --- Salva os dados em um arquivo .csv ---
df = pd.DataFrame(dados, columns=['tempo_s', 'posicao_x_px', 'posicao_y_px'])
df.to_csv('dados_pendulo.csv', index=False)

print(f"Parte 1 concluída! Processou {frame_num} frames.")
print("Dados salvos em 'dados_pendulo.csv'")
print("\nIniciando a Parte 2: Análise e ajuste da curva...")

# ==============================================================================
# --- PARTE 2: ANÁLISE, AJUSTE DA CURVA E GRÁFICO ---
# ==============================================================================

t = df['tempo_s']
x = df['posicao_x_px']

# Define a função do Oscilador Harmônico Amortecido (OHA) para o ajuste
def oha(t, A, b, omega, phi, C):
    return A * np.exp(-b * t) * np.cos(omega * t + phi) + C

# Tenta estimar os valores a partir dos dados para ajudar o algoritmo
A0 = (x.max() - x.min()) / 2
b0 = 0.05
# Estima a frequência contando picos 
num_oscilacoes = len(df[df['posicao_x_px'] > x.mean()].diff().abs().dropna()) / 2
freq_estimada = num_oscilacoes / t.max() if t.max() > 0 else 1
omega0 = 2 * np.pi * freq_estimada
phi0 = 0
C0 = x.mean()
chutes_iniciais = [A0, b0, omega0, phi0, C0]

# Realiza o ajuste da curva
try:
    params, covariance = curve_fit(oha, t, x, p0=chutes_iniciais, maxfev=5000)

    # Extrai os parâmetros ajustados
    A, b, omega, phi, C = params
    print("\nParâmetros ajustados com sucesso:")
    print(f"  Amplitude (A): {A:.2f} px")
    print(f"  Fator de Amortecimento (b): {b:.4f} 1/s")
    print(f"  Frequência Angular (ω): {omega:.4f} rad/s")
    print(f"  Fase (φ): {phi:.4f} rad")
    print(f"  Centro (C): {C:.2f} px")

    # Calcula o Fator de Qualidade (Q)
    omega0 = omega 
    Q = omega0 / (2 * b)
    print(f"\nFator de Qualidade (Q): {Q:.2f}")

    # Plota os resultados
    plt.figure(figsize=(12, 6))
    plt.plot(t, x, 'b.', label='Dados Experimentais', markersize=4)
    plt.plot(t, oha(t, *params), 'r-', label='Ajuste da Curva OHA')
    plt.title('Posição do Pêndulo vs. Tempo')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Posição Horizontal x (pixels)')
    plt.legend()
    plt.grid(True)
    plt.show()

except RuntimeError:
    print("\nErro no ajuste da curva. O algoritmo não conseguiu convergir.")
    print("Tente ajustar os 'chutes_iniciais' no código ou verifique seus dados.")
    # Mesmo com erro, plota os dados crus para visualização
    plt.figure(figsize=(12, 6))
    plt.plot(t, x, 'b.', label='Dados Experimentais')
    plt.title('Posição do Pêndulo vs. Tempo (Falha no Ajuste)')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Posição Horizontal x (pixels)')
    plt.legend()
    plt.grid(True)
    plt.show()