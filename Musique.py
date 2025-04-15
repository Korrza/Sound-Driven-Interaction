import numpy as np
import pygame
from pydub import AudioSegment
import matplotlib.pyplot as plt

# === 1. Charger le fichier WAV ===
audio = AudioSegment.from_wav("assets/toxicity.wav")
samples = np.array(audio.get_array_of_samples()).astype(np.float32)

# Initialisation Pygame
pygame.init()
width, height = 800, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Equalizer")
clock = pygame.time.Clock()

# Paramètres des rectangles
bar_width = 20
spacing = 5
num_bars = width // (bar_width + spacing)

# Si stéréo → garder un seul canal
if audio.channels == 2:
    samples = samples[::2]

# Normaliser entre -1 et 1
samples /= np.max(np.abs(samples))

# === 2. Fonction pour calculer l’énergie ===
def get_energy_frames(samples, frame_size=1024, hop_size=512):
    energy = []
    for i in range(0, len(samples) - frame_size, hop_size):
        frame = samples[i:i + frame_size]
        e = np.sum(frame ** 2)
        energy.append(e)
    energy = np.array(energy)
    energy /= np.max(energy)
    return energy

energy = get_energy_frames(samples) #une note pour chaque trame de l'intensité

# === 3. Détection de pics simples ===
# Méthode : si l'énergie dépasse une moyenne locale + un seuil

def detect_peaks(energy, threshold=1.5, window_size=10):
    peaks = []
    for i in range(window_size, len(energy)):
        local_avg = np.mean(energy[i-window_size:i])
        if energy[i] > local_avg * threshold:
            peaks.append(i)
    return peaks

peaks = detect_peaks(energy, threshold=1.5) # les moment ou la musique pete et sa puissance

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((10, 10, 10))  # Fond noir

    pygame.display.flip()
    clock.tick(10)
# === 4. Affichage (optionnel) ===
plt.figure(figsize=(12, 4))
plt.plot(energy, label="Énergie audio")
plt.scatter(peaks, energy[peaks], color='red', label="Pics détectés")
plt.title("Détection de battements/pics")
plt.xlabel("Trame")
plt.ylabel("Énergie")
plt.legend()
plt.show()
