''' 
robots_parser.py obsahuje funkce pro načtení a zpracování souboru robots.txt z Webové stránky 
robots.txt je soubor, který obsahuje pravidla pro prohledávání webové stránky za pomocí robotů
robots.txt je umístěn v kořenovém adresáři webové stránky
příklad souboru robots.txt na stránce https://www.zsrosi.cz/robots.txt

User-Agent: *           <----- pravidla platí pro všechny roboty
Allow: /                <----- povolené cesty      
Disallow: /admin/       <----- tato cesta je zakázaná
Sitemap: /sitemap.xml   

funkce umožňuje respektovat pravidla pro prohledávání webové stránky
'''

# requests je knihovna pro práci s HTTP požadavky
# urljoin je funkce pro spojení dvou URL 
import requests
from urllib.parse import urljoin

#-----------------------------------------------------
# Funkce pro načtení obsahu souboru robots.txt
def get_robots_txt(url): # Funkce dostane URL webové stránky  
    #Funkce používá blok try-except pro zachycení a zpracování výjimek
    try: 
        robots_url = urljoin(url, '/robots.txt') # Sestavení URL pro robots.txt
        response = requests.get(robots_url) # HTTP požadavek na robots.txt
        if response.status_code == 200: # Pokud je odpověď OK 
            return response.text # Vrátíme obsah souboru robots.txt
        else: 
            return "Nelze načíst robots.txt" # Jinak vrátíme chybovou hlášku
    except requests.RequestException as e: # Zachytává všechny výjimky, které mohou nastat při HTTP požadavku
        return f"Chyba při načítání robots.txt: {e}" # Vrátíme chybovou hlášku


#-----------------------------------------------------
# Funkce pro zpracování obsahu souboru robots.txt
# Analyzuje obsah a extrahuje z něj cesty, které jsou zakázané
def parse_robots_txt(robots_txt, base_url): # Funkce dostane obsah souboru robots.txt a URL webové stránky
    disallowed_paths = [] # Seznam zakázaných cest
    for line in robots_txt.splitlines(): #splitlines() vezme obsah souboru robots.txt jako dlouhý řetězec a rozdělí ho na seznam řetězců
        #takto: ["User-Agent: *", "Allow: /", "Disallow: /admin/", "Sitemap: /sitemap.xml"]
        if line.startswith('Disallow:'):  # Najdeme řádky s Disallow
            path = line.split(':', 1)[1].strip()  # Rozdělíme řádek na dvě části a vezmeme druhou část za ':', odstraníme bílé znaky strip()
            if path: # Pokud je druhá část neprázdná
                full_url = urljoin(base_url, path) # Sestavíme úplnou URL
                disallowed_paths.append(full_url) # Přidáme do seznamu zakázaných cest
    return disallowed_paths # Vrátíme seznam zakázaných cest