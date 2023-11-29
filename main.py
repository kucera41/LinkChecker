#hlavní soubor programu, který spouští celý program
#program má následující funkce:

#1. zeptá se uživatele na URL webové stránky, kterou chce prozkoumat
#2. načte a zpracuje soubor robots.txt (robot.txt je soubor, který obsahuje pravidla pro prohledávání webové stránky za pomocí robotů)
#3. vypíše obsah souboru robots.txt
#4. zjistí, zda je v robots.txt zakázaná celá cesta nebo jiná omezení
#5. zeptá se uživatele, zda chce pokračovat v procházení webu (pro případ, že je v robots.txt zakázaná celá cesta nebo jiná omezení)
#6. prochází web a kontroluje odkazy na webové stránce a jejich odezvy
#7. vypíše mrtvé odkazy do konzole
#8. vypíše ignorované odkazy do konzole (dle robots.txt)
#9. vypíše statistiky do konzole (celkový čas odezvy, průměrný čas odezvy, počet odkazů a počet mrtvých odkazů)

#omezení: program zpracovává odkazy do hloubky 1, tj. následuje odkazy na hlavní stránce, ale ne odkazy na dalších stránkách
#použité technologie: Python 3.12, Selenium, ChromeDriver, requests, colorama, webdriver_manager, urllib.parse, time, 
#-----------------------------------------------------


import robots_parser # Import modulu robots_parser
import link_checker # Import modulu link_checker
from colorama import Fore, Style, init # Knihovna pro barevný výstup do konzole

#-----------------------------------------------------
if __name__ == "__main__": #identifikace hlavního souboru programu
    init() # Inicializace barevného výstupu do konzole
    user_input_url = input("Zadejte URL webové stránky pro kontrolu odkazů: ") 
    # ↑↑↑ Uživatel zadá URL webové stránky, kterou chce prozkoumat na přítomnost mrtvých odkazů
    
    # načtení a zpracování souboru robots.txt
    robots_content = robots_parser.get_robots_txt(user_input_url)
    disallowed_paths = robots_parser.parse_robots_txt(robots_content, user_input_url) 
    # ↑↑↑ Zpracovává obsah robots.txt a vytváří seznam zakázaných cest.


    # výpis obsahu robots.txt
    robots_content = robots_parser.get_robots_txt(user_input_url)
    print(Fore.RED + "\n----------------------------------------------------------------------------------")
    print("\nObsah souboru robots.txt:")
    print(robots_content) #print obsahu souboru robots.txt
    print("\n----------------------------------------------------------------------------------\n" + Style.RESET_ALL)


    disallowed_paths = robots_parser.parse_robots_txt(robots_content, user_input_url)

    # Dotaz na pokračování v procházení webu (pro případ, že je v robots.txt zakázaná celá cesta nebo jiná omezení)
    continue_crawl = input("\nChcete pokračovat s procházením webu? ("+Fore.GREEN+ "ano"+Style.RESET_ALL+"/"+Fore.RED+"ne"+Style.RESET_ALL+"): ").lower()
    if continue_crawl != 'ano':
        print("Procházení webu bylo ukončeno.")
        exit()

    # Volání funkce check_links_on_page z modulu link_checker
    dead_links, total_links, response_times, ignored_links = link_checker.check_links_on_page(user_input_url, disallowed_paths)

    # Výpočet průměrného času odezvy
    average_response_time = sum(response_times) / len(response_times) if response_times else 0

    # Výpis mrtvých odkazů do konzole
    if dead_links:
        print(Fore.RED + "\nNalezené mrtvé odkazy:")
        for dead_link in dead_links:
            print(dead_link)

    # Výpis ignorovaných odkazů do konzole
    if ignored_links:
        print(Fore.YELLOW + "\nIgnorované odkazy podle robots.txt:")
        for ignored_link in ignored_links:
            print(ignored_link)

    # Výpis statistik do konzole, měříme celkový čas odezvy, průměrný čas odezvy, počet odkazů a počet mrtvých odkazů
    print(Fore.GREEN + "\n----------------------------------------------------------------------------------" + Style.RESET_ALL)
    print(Fore.BLUE + f"\nCelkem naskenováno: {total_links}", Fore.RED + f", mrtvé odkazy: {len(dead_links)}" + Style.RESET_ALL)
    print(Fore.GREEN + f"\nCelkový čas odezvy: {sum(response_times):.2f} sekund, průměrný čas odezvy: {average_response_time:.2f} sekund")
    print(Fore.GREEN + "\n----------------------------------------------------------------------------------" + Style.RESET_ALL)