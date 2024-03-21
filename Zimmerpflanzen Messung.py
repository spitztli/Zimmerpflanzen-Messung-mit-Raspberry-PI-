from gpiozero import MCP3008
import time
import Adafruit_DHT
from Connection import verbindungDB

# Schwellenwerte für die Bodenfeuchtigkeit
BODENFEUCHTIGKEIT_NIEDRIG = 0.3880  # Passen Sie diese Werte entsprechend an
BODENFEUCHTIGKEIT_HOCH = 0.7760

# Kanal für den MCP3008 ADC (an Ihre Verkabelung anpassen)
ADC_CHANNEL = 0

# GPIO-Pin an dem der DHT11-Sensor angeschlossen ist
DHT_PIN = 4

def berechne_prozent(bodenfeuchtigkeit):
    return max(0, min(100, int((bodenfeuchtigkeit - BODENFEUCHTIGKEIT_HOCH) / (
                BODENFEUCHTIGKEIT_NIEDRIG - BODENFEUCHTIGKEIT_HOCH) * 100)))

def main():
    adc = MCP3008(channel=ADC_CHANNEL)

    while True:
        # Bodenfeuchtigkeit messen
        bodenfeuchtigkeit = adc.value
        print(bodenfeuchtigkeit)
        prozent_bodenfeuchtigkeit = berechne_prozent(bodenfeuchtigkeit)

        # Temperatur Luftfeuchtigkeit messen
        humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, DHT_PIN)
        Temperatur = temperature
        Luftfeuchtigkeit = humidity

        db = verbindungDB()
        if db is not None:
            cursor = db.cursor()
        else:
            print("Datenbankverbindung konnte nicht hergestellt werden")

        query = "INSERT INTO zimmerpflanzen (name, bodenfeuchtigkeit, temperatur, luftfeuchtigkeit) VALUES (%s, %s, %s, %s)"
        werte = ("Goldene Efeutute", prozent_bodenfeuchtigkeit, Temperatur, Luftfeuchtigkeit)

        cursor.execute(query, werte)
        db.commit()

        print(f"\t{prozent_bodenfeuchtigkeit}%", f"Temperatur: {temperature}°C, Luftfeuchtigkeit: {humidity}%")
        print("Daten erfolgreich gesendet!")

        # 1 Stunde warten (3600 Sekunden)
        time.sleep(3600)

    cursor.close()
    db.close()

if __name__ == "__main__":
    main()