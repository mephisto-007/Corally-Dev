from calculator_core import Rechner

rechner = Rechner()

while True:
    print("1: Addition")
    print("2: Subtraktion")
    print("3: Multiplikation")
    print("4: Division")
    print("5: Beenden")
    
    choice = int(input("Bitte eine Auswahl treffen: "))
    
    if choice == 5:
        print("Programm wird beendet...")
        break
    
    a = float(input("Zahl 1: "))
    b = float(input("Zahl 2: "))
        
    match choice:
        case 1:
            result = rechner.add(a, b)
        case 2:
            result = rechner.subtract(a, b)
        case 3:
            result = rechner.multiply(a, b)
        case 4:
            result = rechner.divide(a, b)
        case _:
            print("Ungültige Auswahl!")
            continue

    if result is not None:
        print("Ergebnis:", result)
