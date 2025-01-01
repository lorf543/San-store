from bs4 import BeautifulSoup
import requests

website = 'https://www.rockauto.com/'
result = requests.get(website)
content = result.text

soup = BeautifulSoup(content, 'lxml')

# Encuentra todas las cajas con la clase 'ranavouter'
boxes_brand = soup.find_all('div', class_='ranavouter')

# Itera sobre cada caja y encuentra los enlaces dentro de ella
for box in boxes_brand:
    links = box.find_all('a')
    for link in links:
        # Obtén el texto de cada enlace (marca)
        brand = link.get_text()
        
        # Obtén el enlace de la marca
        brand_link = link.get('href')
        
        # Realiza una solicitud GET a la página de la marca
        brand_result = requests.get(website + brand_link)
        brand_content = brand_result.text
        
        # Crea un objeto BeautifulSoup para la página de la marca
        brand_soup = BeautifulSoup(brand_content, 'lxml')
        
        # Encuentra las cajas con los años disponibles
        years_boxes = brand_soup.find_all('div', class_='year')
        
        # Itera sobre cada caja y encuentra los años disponibles
        for year_box in years_boxes:
            years = year_box.find_all('a')
            for year in years:
                # Imprime la marca y el año disponible
                print(f"{brand}: {year.get_text()}")
