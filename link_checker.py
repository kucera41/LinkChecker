#link_checker.py obsahuje funkce pro kontrolu odkazů na webové stránce a jejich odezvy


import requests # Knihovna pro práci s HTTP požadavky
import time # Knihovna pro práci s časem
from selenium import webdriver # Knihovna pro práci s webovým prohlížečem
from selenium.webdriver.common.by import By 
from selenium.webdriver.chrome.service import Service # Knihovna pro práci s ChromeDriverem
from webdriver_manager.chrome import ChromeDriverManager #Driver manager umožňuje automatické stažení a aktualizaci driveru
from colorama import Fore, Style, init # Knihovna pro barevný výstup do konzole

#-----------------------------------------------------
# Funkce pro kontrolu odkazů na webové stránce
def check_links_on_page(url, disallowed_paths): # dostane URL webové stránky a seznam zakázaných cest
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install())) # Spuštění ChromeDriveru a zajištění jeho aktualizace
    driver.get(url) # Otevření webové stránky v prohlížeči

    links = driver.find_elements(By.TAG_NAME, "a") # Najdeme všechny odkazy na stránce pomocí tagu <a>
    all_hrefs = [link.get_attribute('href') for link in links if link.get_attribute('href') and link.get_attribute('href').startswith("http")] 
    # ↑↑↑ Vytvoříme seznam odkazů, které začínají na http a mají atribut href, 
    
    dead_links = [] # Seznam pro mrtvé odkazy
    ignored_links = []  # Seznam pro ignorované odkazy (viz robots_parser.py)
    response_times = [] # Seznam pro časové odezvy


    # for loop pro kontrolu odkazů
    for href in all_hrefs: # Pro každý odkaz v seznamu odkazů
        if any(href.startswith(disallowed) for disallowed in disallowed_paths): # Pokud odkaz začíná na některou z cest v seznamu zakázaných cest
            ignored_links.append(href)  # Přidáme odkaz do seznamu ignorovaných odkazů
            continue
        # Jinak pokračujeme v kontrole odkazu
        print(f"Testuji odkaz: {href}") # Výpis aktuálního testovaného odkazu do konzole
        try: # Blok try-except pro zachycení a zpracování výjimek
            start_time = time.time()  # Začátek měření času pro tento odkaz
            response = requests.head(href, allow_redirects=True) # HTTP požadavek na odkaz s následným přesměrováním
            end_time = time.time()  # Konec měření času
            response_times.append(end_time - start_time)  # Přidání času odezvy do seznamu
            # Výpis do konzole podle stavového kódu
            if response.status_code == 404: # Pokud je stavový kód 404
                print(Fore.RED + f"Mrtvý odkaz (404): {href}" + Style.RESET_ALL) # Výpis do konzole
                dead_links.append(href) # Přidání odkazu do seznamu mrtvých odkazů
        except requests.RequestException as e: # Zachytává všechny výjimky, které mohou nastat při HTTP požadavku
            print(Fore.RED + f"Chyba při načítání odkazu {href}: {e}" + Style.RESET_ALL) # Výpis do konzole
            dead_links.append(href) # Přidání odkazu do seznamu mrtvých odkazů
    
    driver.quit() # Ukončení prohlížeče
    return dead_links, len(all_hrefs), response_times, ignored_links 
    # ↑↑↑ Vrátíme seznam mrtvých odkazů, počet odkazů, seznam časů odezvy a seznam ignorovaných odkazů

