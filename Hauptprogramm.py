import subprocess
while True:
    print("1: Rechner")
    print("2: Währungsumrechner")
    print("3: Zinsrechner")
    print("4: Beenden")
    choice = int(input("Bitte wählen Sie eine Option: "))
    
    if choice == 4:
        print("Programm wird beendet.")
        break
    match choice:
        case 1:
            subprocess.run(["python", "Rechner.py"])

        case 2:
            uvicorn_process = subprocess.Popen(["uvicorn", "api_free:app"])

        case 3:
            subprocess.run(["python", "Zinsrechner.py"])
        
        case _:
            print("Ungültige Auswahl. Bitte erneut versuchen.")
            continue