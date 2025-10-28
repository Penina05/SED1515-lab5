import matplotlib.pyplot as plt

# ----- Lire le fichier log.txt -----
temps = []

with open("log.txt", "r") as f:
    for line in f:
        line = line.strip()
        if line.startswith("RTC:"):
            # Exemple de ligne : "RTC: 14 s, Pico: 15.23 s"
            parts = line.split(',')
            rtc_part = parts[0]  # "RTC: 14 s"
            value = int(rtc_part.split()[1])  # récupère le nombre 14
            temps.append(value)

# ----- Créer un histogramme -----
plt.hist(temps, bins=range(min(temps), max(temps)+2), edgecolor='black', align='left')
plt.xlabel("Temps compté par le joueur (secondes)")
plt.ylabel("Nombre d'essais")
plt.title("Précision de la perception du temps")
plt.xticks(range(min(temps), max(temps)+1))
plt.show()
