from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import json

BASIS_URL = "https://aip.dfs.de/BasicIFR/"

IGNORIEREN = {
    'AIP', 'AD', 'Impressum', 'Disclamer', 'Datenschutz',
    'AD 0', 'AD 1 Flugplätze/Hubschrauberflugplätze – Einführung',
    'AD 2 Flugplätze', 'AD 3 Hubschrauberflugplätze',
    'MIL-AD 1', 'MIL-AD 2'
}


def warte(browser):
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, 'a'))
    )
    time.sleep(1.5)


def alle_links(browser):
    return [(l.text.strip(), l.get_attribute('href'))
            for l in browser.find_elements(By.TAG_NAME, 'a')]


def ist_karte(text, href, fh_url):
    if not text or not href:
        return False
    if "aip.dfs.de" not in href:
        return False
    if href == fh_url:
        return False
    if any(x in href for x in ['#popupSearch', '#popupPermalink', 'javascript:']):
        return False
    if text in IGNORIEREN:
        return False
    if '»' in text:
        return False
    if len(text) < 3:
        return False
    return True


def durchlauf():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    service = Service(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=service, options=options)
    katalog = {}

    try:
        # 1. Startseite → AD Flugplätze
        browser.get(BASIS_URL)
        warte(browser)

        ad_url = next((href for text, href in alle_links(browser)
                       if "AD Flugplätze" in text and href), None)
        if not ad_url:
            print("Fehler: AD Flugplätze nicht gefunden.")
            return

        # 2. AD Flugplätze → AD 2 Flugplätze
        browser.get(ad_url)
        warte(browser)

        ad2_url = next((href for text, href in alle_links(browser)
                        if "AD 2 Flugplätze" in text and href), None)
        if not ad2_url:
            print("Fehler: AD 2 Flugplätze nicht gefunden.")
            return

        # 3. Alle Flughafen-URLs direkt einsammeln (keine Alphabet-Ordner)
        browser.get(ad2_url)
        warte(browser)

        flughafen_urls = {}
        for text, href in alle_links(browser):
            if (href and "aip.dfs.de" in href and "»" in text
                    and text not in IGNORIEREN and len(text) > 3):
                name = text.replace('»', '').strip()
                flughafen_urls[name] = href

        print(f"{len(flughafen_urls)} Flughäfen gefunden.")

        # 4. Jeden Flughafen aufrufen und Karten sammeln
        for fh_name, fh_url in flughafen_urls.items():
            print(f"  {fh_name} ...", end=" ", flush=True)
            browser.get(fh_url)
            warte(browser)

            karten = {}
            for text, href in alle_links(browser):
                if ist_karte(text, href, fh_url):
                    karten[text] = href

            print(f"({len(karten)} Karten)")
            katalog[fh_name] = {
                "_url": fh_url,
                "karten": karten
            }

        with open("ifr_katalog_export.json", "w", encoding="utf-8") as f:
            json.dump(katalog, f, indent=4, ensure_ascii=False)

        print(f"\nFertig! {len(katalog)} Flughäfen gespeichert.")

    except Exception as e:
        import traceback
        print(f"Fehler: {e}")
        traceback.print_exc()

    finally:
        browser.quit()


def main():
    import sys
    if '--loop' in sys.argv:
        while True:
            print("Starte Durchlauf...")
            durchlauf()
            print("Nächster Durchlauf in 6 Stunden.\n")
            time.sleep(6 * 60 * 60)
    else:
        durchlauf()


if __name__ == '__main__':
    main()
