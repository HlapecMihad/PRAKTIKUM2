import requests
from bs4 import BeautifulSoup
import json

def LinkiProdaja():
    base_url = "https://nepremicnine.siol.net/iskanje/prodaja?price_0=min&price_1=max"

    response = requests.get(base_url)
    if response.status_code != 200:
        print("Error accessing page. Exiting...")
        exit()

    html_content = response.content

    soup = BeautifulSoup(html_content, 'html.parser')

    pagination_links = soup.find_all('li', class_='pagination-link')
    if pagination_links:
        last_page_link = pagination_links[-2]
        last_page_number = last_page_link.a.text.strip()
        print("The last page number is:", last_page_number)
    else:
        print("No pagination links found.")

    all_links = []

    for page_number in range(1, int(last_page_number) + 1):
        print("Scraping page:", page_number)
        
        url = f"{base_url}&page={page_number}"
        
        response = requests.get(url)
        if response.status_code != 200:
            print("Error accessing page. Skipping...")
            continue  

        html_content = response.content

        soup = BeautifulSoup(html_content, 'html.parser')

        items = soup.find_all('div', class_='item')

        for item in items:
            link_tag = item.find('a', class_='list-thumb')
            if link_tag:
                link = link_tag.get('href')
                full_link = "https://nepremicnine.siol.net" + link
                all_links.append(full_link)

    with open('real_estate_links_prodaja.txt', 'w') as file:
        for link in all_links:
            file.write(f"{link}\n")

    print("Links have been saved to real_estate_links.txt")


# Function to scrape data from a given URL
def scrape_data(url):
    print(url)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    naziv = soup.find('h2', class_='sp-lg-title').get_text(strip=True) if soup.find('h2', class_='sp-lg-title') else 'N/A'
    transaction_type = soup.select_one('.pd-meta a.ff-heading').get_text(strip=True) if soup.select_one('.pd-meta a.ff-heading') else 'N/A'
    region = soup.find('p', class_="col-6 fw600 mb10 ff-heading dark-color", string="Regija").find_next('p').get_text(strip=True) if soup.find('p', class_="col-6 fw600 mb10 ff-heading dark-color", string="Regija") else 'N/A'
    city = soup.find('p', class_="col-6 fw600 mb10 ff-heading dark-color", string="Naselje").find_next('p').get_text(strip=True) if soup.find('p', class_="col-6 fw600 mb10 ff-heading dark-color", string="Naselje") else 'N/A'
    price = soup.find('h3', class_='price mb-0').get_text(strip=True) if soup.find('h3', class_='price mb-0') else 'N/A'
    property_type = soup.find('h6', class_='mb-0', string='Tip').find_next('p', class_='text mb-0 fz15').get_text(strip=True).split(',')[0] if soup.find('h6', class_='mb-0', string='Tip') else 'N/A'
    kopalnice = soup.find('h6', string="Število kopalnic").find_next('p').get_text(strip=True) if soup.find('h6', string="Število kopalnic") else 'N/A'
    spalnice = soup.find('h6', string="Število spalnic").find_next('p').get_text(strip=True) if soup.find('h6', string="Število spalnic") else 'N/A'
    #rooms = soup.find('h6', class_='mb-0', string='Tip').find_next('p', class_='text mb-0 fz15').get_text(strip=True).split(',', 1)[1].strip() if soup.find('h6', class_='mb-0', string='Tip') and 'Stanovanje' in soup.find('h6', class_='mb-0', string='Tip').find_next('p', class_='text mb-0 fz15').get_text(strip=True).split(',', 1)[0].strip() else 'N/A'
    tip_element = soup.find('h6', class_='mb-0', string='Tip')
    try:
        if tip_element:
            tip_text = tip_element.find_next('p', class_='text mb-0 fz15').get_text(strip=True)
            tip_parts = tip_text.split(',', 1)
            if len(tip_parts) > 1 and 'Stanovanje' in tip_parts[0].strip():
                second_part = tip_parts[1].strip()
                rooms = '1' if second_part == 'Garsonjera' else second_part
            else:
                rooms = 'N/A'
        else:
            rooms = 'N/A'
    except IndexError:
        rooms = 'N/A'
    id_nepremicnine = soup.find(title='Šifra oglasa').get_text(strip=True) if soup.find(title='Šifra oglasa') else 'N/A'
    year_built = soup.find('p', string="Leto izgradnje").find_next('p').get_text(strip=True) if soup.find('p', string="Leto izgradnje") else 'N/A'
    size = soup.find('h6', string='Velikost').find_next('p').get_text(strip=True) if soup.find('h6', string='Velikost') else 'N/A'
    if 'Bruto:' in size: size = size.split('Bruto:')[1].split('|')[0].strip() 
    description = soup.find('div', class_='ps-widget bgc-white bdrs12 default-box-shadow2 mb30 p30 overflow-hidden position-relative').text.split('Podrobnosti')[0].strip() if soup.find('div', class_='ps-widget bgc-white bdrs12 default-box-shadow2 mb30 p30 overflow-hidden position-relative') else 'N/A'
    land_size = soup.find('h6', string="Velikost zemljišča").find_next('p').get_text(strip=True) if soup.find('h6', string="Velikost zemljišča") else 'N/A'
    rebuild_year = soup.find('p', string="Obnove").find_next('p').get_text(strip=True) if soup.find('p', string="Obnove") else 'N/A'
    #agency_name = soup.find('div', class_='agent-meta mb10 d-md-flex flex-column').find('h6', class_='title mb-1').text.strip() if soup.find('div', class_='agent-meta mb10 d-md-flex flex-column') else 'N/A'
    agent_meta = (soup.find('div', class_='agent-meta mb10 d-md-flex flex-column') or 
                  soup.find('div', class_='single-contant my10 overflow-hidden'))
    agency_name = (agent_meta.find('h6', class_='title mb-1').text.strip() 
                   if agent_meta and agent_meta.find('h6', class_='title mb-1') 
                   else 'N/A')
    oprema_div = soup.find('h4', string="Oprema in ostalo").find_next('div') if soup.find('h4', string="Oprema in ostalo") else 'N/A'
    if(oprema_div != 'N/A'): lastnosti = [p.text.strip() for p in oprema_div.find_all('p', class_='text mb10')] 
    else: lastnosti = 'N/A'

    if(property_type == 'Turistični objekt'): property_type = 'Počitniški objekt'
    elif(property_type == 'Garaža' or property_type == 'Parkirišče'): property_type = 'Garaža/Parkirni mesto'

    # Extract all image URLs
    image_urls = [a['href'] for a in soup.select('.gallery-image-video .sp-img-content a') if a.get('href')]
    # Create the dictionary
    data = {
        'naziv': naziv,
        'posredovanje': transaction_type,
        'link': url,
        'tip_nepremicnine': property_type,
        'lokacija': region + ', ' + city,
        'cena': float(price.replace('.', '').replace(',', '.').replace(' €', '').replace('/mesec','').replace('/dan','')) if price not in ['N/A', 'Po dogovoru'] else 'N/A',
        'st_sob': float(rooms.split('-')[0].replace(',', '.').replace('+', '')) if rooms not in ['N/A', 'Drugo'] else 'N/A',
        'st_spalnic': int(spalnice) if spalnice != 'N/A' else 'N/A',
        'st_kopalnic': int(kopalnice) if kopalnice != 'N/A' else 'N/A',
        'leto_izgradnje': int(year_built) if year_built != 'N/A' else 'N/A',
        'st_nadstopij': 'N/A',  
        'velikost_zemljisca': land_size,  
        'velikost_skupaj': size,  
        'id_nepremicnine': id_nepremicnine if id_nepremicnine != 'N/A' else url.split('/')[4],
        'image_urls': image_urls,
        'opis': description,
        'leto_obnove': rebuild_year,
        'agencija': agency_name,
        'lastnosti': [lastnosti],
    }
    return data

def NepremicnineProdaja():
    # Read links from the text file
    with open('real_estate_links_prodaja.txt', 'r') as file:
        links = file.readlines()

    # Strip newline characters from each link
    links = [link.strip() for link in links]

    # Scrape data from each link and store it in a list
    scraped_data = []
    counter = 0
    for link in links:
        if(counter < 100):
            data = scrape_data(link)
            scraped_data.append(data)
            print(counter)
        counter += 1

    # Save the scraped data to a JSON file with proper formatting
    with open('scraped_real_estate_data_oddaja.json', 'w', encoding='utf-8') as outfile:
        json.dump(scraped_data, outfile, ensure_ascii=False, indent=4)

    print("Scraping and saving completed.")

if __name__ == "__main__":
    LinkiProdaja()
    NepremicnineProdaja()