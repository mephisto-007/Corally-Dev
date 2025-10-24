from calculator_core import Waerungsrechner

rechner=Waerungsrechner()

while True:
    print("1: Eur/USD")
    print("2: USD/Eur")
    print("3: EUR/BP")
    print("4: BP/EUR")
    print("5: EUR/YEN")
    print("6: YEN/EUR")
    print("7: Beenden")
    
    
    choice = int(input("Bitte eine Auswahl treffen: "))
    if choice == 7:
        break
        
    match choice:
        case 1:
            eur = float(input("Bitte einen € Betrag eingeben:"))
            usd=rechner.eur_to_usd(eur)
            print(f"{eur}€ sind {usd}$")
        case 2:
            usd = float(input("Bitte einen $ Betrag eingeben:"))
            eur=rechner.usd_to_eur(usd)
            print(f"{usd}$ sind {eur}€")
        case 3:
            eur = float(input("Bitte einen € Betrag eingeben: "))
            bp= rechner.eur_to_gbp(eur)
            print(f"{eur}€ sind {bp}£")
        case 4:
            bp = float(input("Bitte einen £ Betrag eingeben: "))
            eur = rechner.gbp_to_eur(bp)
            print(f"{bp}£ sind {eur}€")
        case 5:
            eur = float(input("Bitte einen € Betrag eingeben: "))
            yen = rechner.eur_to_jpy(eur)
            print(f"{eur}€ sind {yen}¥")
        case 6:
            yen = float(input("Bitte einen ¥ Betrag eingeben: "))
            eur = rechner.jpy_to_eur(yen)
            print(f"{yen}¥ sind {eur}€")
            
        case _:
            print("Ungültige Auswahl!")
            continue
        
