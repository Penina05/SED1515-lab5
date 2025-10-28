

from machine import Pin, I2C
import time

#  Configuration I2C pour le DS3231 
i2c = I2C(1, sda=Pin(14), scl=Pin(15))
rtc_address = 0x68  # Adresse I2C du DS3231

#  Fonction pour lire les secondes depuis le DS3231 
def bcd_to_int(bcd):
    """Convertit une valeur BCD en entier"""
    return ((bcd >> 4) * 10) + (bcd & 0x0F)

def read_seconds():
    """Lit les secondes depuis le registre 0x00 du DS3231"""
    raw = i2c.readfrom_mem(rtc_address, 0x00, 1)
    return bcd_to_int(raw[0])

#  Bouton pour le jeu 
button = Pin(22, Pin.IN, Pin.PULL_DOWN)

# Ouverture du fichier journal 
log = open("log.txt", "a")

try:
    print("Jeu de perception du temps ")
    print("Appuyez une premiere fois pour demarrer...")

    while True:
        # Attente du premier appui
        while not button.value():
            time.sleep(0.01)
        start = read_seconds()
        pico_start = time.ticks_ms()

        print("Debut ! Comptez environ 15 secondes...")

        # Attente du deuxième appui
        while button.value():  # attendre que le joueur relâche
            time.sleep(0.01)
        time.sleep(0.2)  # anti-rebond

        while not button.value():
            time.sleep(0.01)
        end = read_seconds()
        pico_end = time.ticks_ms()

        # Calcul du temps écoulé
        elapsed = (end - start) % 60
        pico_elapsed = time.ticks_diff(pico_end, pico_start) / 1000

        print("Vous avez compter : {} s (RTC)".format(elapsed))
        print(" Temps interne Pico : {:.2f} s".format(pico_elapsed))

        # Sauvegarde
        log.write("RTC: {} s, Pico: {:.2f} s\n".format(elapsed, pico_elapsed))
        log.flush()
        print("Resultat enregistrer dans log.txt")
        print("\nAppuyez pour rejouer...\n")

        # Attendre que le bouton soit relâché avant de recommencer
        while button.value():
            time.sleep(0.01)

except KeyboardInterrupt:
    print("Fin du jeu.")

finally:
    log.close()
    print("Journal sauvegarder dans log.txt")

