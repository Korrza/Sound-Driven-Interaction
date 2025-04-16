import pygame
import numpy as np
from scipy.io import wavfile
import random

# === CONFIG ===
AUDIO_PATH = "assets/enemy.wav"
FRAME_SIZE = 2048
HOP_SIZE = 512
HIGH_FREQ_MIN = 3000  # Hz
SKIP_SECONDS = 0

rate, samples = wavfile.read(AUDIO_PATH)

if len(samples.shape) == 2:
    samples = samples[:, 0]

samples = samples.astype(np.float32)
samples /= np.max(np.abs(samples))

start_sample = rate * SKIP_SECONDS
samples = samples[start_sample:]

print("Nombre d’échantillons :", len(samples))
print("Extrait (début) :", samples[:10])
print("Raw Pydub samples :")
print(samples[:100])
print("Max sample:", np.max(samples))
print("Min sample:", np.min(samples))


pygame.init()
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Visualiseur Haute Fréquence")
clock = pygame.time.Clock()

pygame.mixer.init(frequency=rate)
pygame.mixer.music.load(AUDIO_PATH)
pygame.mixer.music.play(start=SKIP_SECONDS)

def get_fft_spectrum(frame, sample_rate):
    windowed = frame * np.hanning(len(frame))
    fft_result = np.fft.fft(windowed)
    freqs = np.fft.fftfreq(len(frame), d=1/sample_rate)
    magnitude = np.abs(fft_result)
    return freqs[:len(freqs)//2], magnitude[:len(magnitude)//2]

running = True
current_sample = 0
num_bars = 64
min_freq = 20
max_freq = rate // 3

freq_bins = np.logspace(np.log10(min_freq), np.log10(max_freq), num_bars + 1)
size_bar_before = np.zeros(num_bars)
smooth_size = 0.4
while running and current_sample + FRAME_SIZE < len(samples):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    elapsed_ms = pygame.mixer.music.get_pos()
    elapsed_sec = elapsed_ms / 1000
    current_sample = int(elapsed_sec * rate)

    if current_sample + FRAME_SIZE >= len(samples):
        break

    frame = samples[current_sample:current_sample + FRAME_SIZE]
    freqs, mag = get_fft_spectrum(frame, rate)

    screen.fill((15, 15, 40))

    bar_width = screen_width / (num_bars - 14)
    avoid_bar = 0
    for i in range(num_bars):
        f_min = freq_bins[i]
        f_max = freq_bins[i + 1]

        band = (freqs >= f_min) & (freqs < f_max)
        if not np.any(band):
            avoid_bar += 1
            continue

        band_energy = np.mean(mag[band])
        size_bar_before[i] = (1 - smooth_size) * size_bar_before[i] + smooth_size * band_energy
        band_energy_norm = min(size_bar_before[i] / 250, 1.0)

        x = (i - avoid_bar) * bar_width
        h = band_energy_norm * screen_height * 1.2
        y = screen_height - h
        color = (155 + int(band_energy_norm * 100), int(band_energy_norm * 255), i * (255/num_bars))
        pygame.draw.rect(screen, color, (x, y, bar_width - 2, h))

    pygame.display.flip()
    clock.tick(60)
    current_sample += HOP_SIZE

pygame.quit()

