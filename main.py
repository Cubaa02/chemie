import csv
import json

# Cesty k souborům
csv_file_path = "elements.csv"  # Nahraďte správnou cestou
json_file_path = "groups.json"  # Nahraďte správnou cestou

# Funkce pro načtení dat z CSV souboru
def load_elements_from_csv(file_path):
    elements = []
    with open(file_path, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            elements.append(row)
    return elements

# Funkce pro načtení dat ze souboru JSON
def load_groups_from_json(file_path):
    with open(file_path, mode='r', encoding='utf-8') as jsonfile:
        groups = json.load(jsonfile)
    return groups

# Vyhledání prvku podle kritéria
def find_element(elements, criterion, value):
    results = []
    for el in elements:
        if criterion == "AtomicNumber":
            # Odstranění mezer a kontrola čísla
            if el.get(criterion) and el[criterion].strip().isdigit() and int(el[criterion].strip()) == int(value):
                results.append(el)
        else:
            if el.get(criterion, "").strip().lower() == value.strip().lower():
                results.append(el)
    return results

# Výpočet průměrné relativní atomové hmotnosti
def calculate_average_mass(elements, criterion, value):
    # Filtrování prvků podle kritéria a hodnoty, ověřujeme, zda klíč existuje a hodnota není prázdná
    filtered = [el for el in elements if el.get(criterion) == value and el.get('AtomicMass')]
    if not filtered:
        return None  # Pokud nejsou nalezeny žádné prvky
    
    # Výpočet průměrné atomové hmotnosti
    masses = []
    for el in filtered:
        mass = el.get('AtomicMass', '').strip()  # Odstranění mezer kolem hodnoty
        if mass.replace('.', '', 1).isdigit():  # Kontrola, zda je hmotnost platné číslo
            masses.append(float(mass))  # Převod na float a přidání do seznamu

    if not masses:
        return None  # Pokud nejsou žádné platné hmotnosti
    return sum(masses) / len(masses)

# Export do HTML
def export_to_html(elements, file_name="elements_table.html"):
    html_content = "<!DOCTYPE html>\n<html>\n<head>\n<title>Periodic Table</title>\n</head>\n<body>\n"
    html_content += "<table border='1'>\n<tr>"
    headers = elements[0].keys()
    html_content += "".join(f"<th>{header}</th>" for header in headers)
    html_content += "</tr>\n"
    
    for element in elements:
        html_content += "<tr>"
        html_content += "".join(f"<td>{element[header]}</td>" for header in headers)
        html_content += "</tr>\n"
    
    html_content += "</table>\n</body>\n</html>"
    
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(html_content)
    return file_name

# Export do JSON
def export_to_json(elements, file_name="selected_elements.json"):
    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(elements, file, indent=4, ensure_ascii=False)
    return file_name

# Export do Markdown
def export_to_markdown(elements, group_name=None, file_name="elements_overview.md"):
    markdown_content = f"# Přehled prvků\n\n"
    if group_name:
        markdown_content += f"## Skupina: {group_name}\n\n"
    markdown_content += "| Symbol | Název | Atomová hmotnost | Skupina | Perioda |\n"
    markdown_content += "|--------|-------|------------------|---------|---------|\n"
    for element in elements:
        markdown_content += f"| {element['Symbol']} | {element['Element']} | {element['AtomicMass']} | {element['Group']} | {element['Period']} |\n"
    
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(markdown_content)
    return file_name

# Základní struktura menu
def main_menu():
    elements_data = load_elements_from_csv(csv_file_path)
    groups_data = load_groups_from_json(json_file_path)

    while True:
        print("\nChemické Prvky - Hlavní Menu")
        print("1. Vyhledat prvek")
        print("2. Zobrazit vlastnosti prvku")
        print("3. Výpočet průměrné relativní atomové hmotnosti")
        print("4. Export dat")
        print("5. Ukončit program")
        
        choice = input("Vyberte možnost: ")
        
        if choice == "1":
            criterion = input("Hledat podle (Symbol/Element/AtomicNumber): ").capitalize()
            value = input("Zadejte hodnotu: ")
            results = find_element(elements_data, criterion, value)
            if results:
                print("Nalezené prvky:")
                for res in results:
                    print(res)
            else:
                print("Žádný prvek nebyl nalezen.")
        
        elif choice == "2":
            symbol = input("Zadejte symbol prvku: ")
            results = find_element(elements_data, "Symbol", symbol)
            if results:
                print("Vlastnosti prvku:")
                for key, val in results[0].items():
                    print(f"{key}: {val}")
            else:
                print("Prvek nebyl nalezen.")
        
        elif choice == "3":
            group_or_period = input("Chcete průměr počítat pro (Skupina/Perioda): ").capitalize()
            value = input("Zadejte číslo: ")
            avg_mass = calculate_average_mass(elements_data, group_or_period, value)
            if avg_mass is not None:
                print(f"Průměrná atomová hmotnost: {avg_mass:.2f}")
            else:
                print("Žádné prvky odpovídající kritériu nebyly nalezeny nebo neobsahují platné hmotnosti.")
        
        elif choice == "4":
            print("\nExport dat")
            print("1. Export do HTML")
            print("2. Export do JSON")
            print("3. Export do Markdown")
            export_choice = input("Vyberte možnost: ")
            
            if export_choice == "1":
                file_name = export_to_html(elements_data)
                print(f"Data byla exportována do souboru {file_name}.")
            
            elif export_choice == "2":
                file_name = export_to_json(elements_data)
                print(f"Data byla exportována do souboru {file_name}.")
            
            elif export_choice == "3":
                group_name = input("Chcete exportovat konkrétní skupinu? (nechte prázdné pro všechny): ")
                selected_elements = elements_data
                if group_name:
                    group = next((g for g in groups_data if g["cs"].lower() == group_name.lower()), None)
                    if group:
                        selected_elements = [el for el in elements_data if el['Symbol'] in group['elements']]
                    else:
                        print("Skupina nebyla nalezena.")
                        continue
                file_name = export_to_markdown(selected_elements, group_name)
                print(f"Data byla exportována do souboru {file_name}.")
        
        elif choice == "5":
            print("Ukončuji program. Nashledanou!")
            break
        
        else:
            print("Neplatná volba, zkuste to znovu.")

# Spuštění programu
main_menu()
