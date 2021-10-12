import requests
from bs4 import BeautifulSoup
import csv
import concurrent.futures

def csv_saver():
    with open("results.csv","w",newline="",encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(['ID',"ID intern","Tip proprietate","Valabilitate","Status palnie","Tip apartament","Tip vila","Compartimentare","Stadiu constructie",'Orientare','Pret vanzare','TVA Vanzare','Pret inchiriere','TVA Inchiriere','Inchiriat pana la','Nr. camere','An constr.',"S. construita",'S. utila','S. balcoane','S. terasa','S. totala','S. teren','Deschidere','Strada','Nr. strada','Bloc','Scara','Nr. apartament','Etaj','Nr. et. Cladire','Reper','Judet','Localitate','Zona','Agent','Ansamblu rezidential','Model apartament','Titlu','Descriere','Contact','Dotari: Dotari','Dotari: Sistem incalzire','Dotari: Bucatarie','Dotari: (nume grup dotari)','POZE PROPRIETATI'])
        writer.writerows([x for x in records])

def url_generator(url_pat,pages):
    for x in range(1,pages+1):
        page_link = url_pat.format(str(x))
        page_links.append(page_link)

def item_links_extractor(url,object_type,deal_type):
    r = requests.get(url)
    soup = BeautifulSoup(r.text,'html.parser')

    items = soup.find_all('div',class_="col-xs-6 col-md-4 col-grid-post io-property")

    for item in items: 
        adress = item.find('p',class_='property-address').text   
        link_parrent = item.find('div',class_='property-thumbnail')
        links = link_parrent.find_all('a')  
        img_link = item.find('img')   
        img_link = img_link['src'] 
        link = links[1]  
        link_adress = (link['href'],adress,img_link,object_type,deal_type)  
        item_links.append(link_adress) 

def main_extractor(link):
    url = link[0]
    r = requests.get(url)
    soup = BeautifulSoup(r.text,'html.parser')
    area_name  = link[1]
    object_type = link[3]
    deal_type = link[4]
    title = soup.find('h1',class_="entry-title single-property-title").text
    description_parrent = soup.find('div',class_='property-content')
    description = description_parrent.find('p').text
    description = description.replace(',',';')
    
    sell_price = None
    rent_price = None

    if deal_type == "sell":
        price_parrent = soup.find('span',class_='single-property-price price').text
        price_parrent = price_parrent.split('€')
        sell_price = price_parrent[0]
        sell_price = sell_price.replace(".",'')
    elif deal_type == "rent":
        price_parrent = soup.find('span',class_='single-property-price price').text     
        if ("(" in price_parrent):
            price_parrent3 = price_parrent.split("€")
            rent_price = price_parrent3[1]
            rent_price = rent_price.replace("(",'').replace(" ",'').replace(".",'')

        else:
            price_parrent1 = price_parrent.split('€')
            rent_price = price_parrent1[0]
            rent_price = rent_price.replace(".",'')
        
    object_id_parrent = soup.find('a',class_='printer-icon idul').text
    object_id_parrent = object_id_parrent.split(' ')
    object_id = object_id_parrent[1]


    whole_area = None
    usable_area = None
    teresse_area = None
    rooms = None
    bathrooms = None
    floor = None
    floors_in_building = None
    construction_year = None

    other_parrent = soup.find('div',class_='property-meta entry-meta clearfix')
    other_parrent = other_parrent.find_all("div",class_='meta-item')

    for meta_item in other_parrent:
        label = meta_item.find('span',class_='meta-item-label').text
        if ('Suprafata Construita' in label):
            whole_area_parrent = meta_item.find('span',class_='meta-item-value').text
            whole_area_parrent = whole_area_parrent.split('m')
            whole_area = whole_area_parrent[0]

        elif ('Suprafata Utila' in label):
            usable_area_parrent = meta_item.find('span',class_='meta-item-value').text
            usable_area_parrent = usable_area_parrent.split('m')
            usable_area = usable_area_parrent[0]

        elif ('Suprafata terasa' in label):
            teresse_area_parrent = meta_item.find('span',class_='meta-item-value').text
            teresse_area_parrent = teresse_area_parrent.split('m')
            teresse_area = teresse_area_parrent[0]

        elif ('Camere' in label):
            rooms = meta_item.find('span',class_='meta-item-value').text

        elif ('Bai' in label):
            bathrooms = meta_item.find('span',class_='meta-item-value').text

        elif ('Etaj' in label):
            floors_parrent = meta_item.find('span',class_='meta-item-value').text
            floors_parrent = floors_parrent.split(' ')
            floor = floors_parrent[0]
            floors_in_building = floors_parrent[2]

        elif ('Anul constructiei' in label):
            construction_year = meta_item.find('span',class_='meta-item-value').text
        

    agent_data = soup.find('div',class_='agent-content-wrapper agent-common-styles')
    agent_name = agent_data.find('h3').text
    agent_ddata = agent_name.split('            ')
    agent_name = agent_ddata[1]
    agent_phone = agent_data.find('div',id='agent-phone-fix')
    agent_numb = agent_phone.find('a').text
    balcony_area = None
    sell_tax = None
    for_none = None

    img_links_list_parrent = soup.find('div',class_='single-property-slider gallery-slider flexslider')
    img_links_list_parrent = img_links_list_parrent.find('ul',class_='slides')
    img_links_list = img_links_list_parrent.find_all("img")
    img_links = ''
    for x in img_links_list:
        link_string = x['src']
        img_links = img_links + link_string
        img_links = img_links + "; "




    record = (for_none,object_id,"apartament","activa",for_none,object_type,for_none,for_none,"finalizata",for_none,sell_price,sell_tax,rent_price,for_none,for_none,rooms,construction_year,whole_area,usable_area,teresse_area,for_none,for_none,for_none,for_none,area_name,"1",for_none,for_none,'1',floor,floors_in_building,for_none,"bucuresti",for_none,area_name,agent_name,for_none,for_none,title,description,agent_numb,for_none,for_none,for_none,for_none,img_links)
    records.append(record)

def main(url_pat,pages):
    url_generator(url_pat,pages)

    if ('de-vanzare' in url_pat):
        deal_type = 'sell'
    elif ('de-inchiriat' in url_pat):
        deal_type = 'rent'
    if ('apartament' in url_pat):
        object_type = "apartament"
    elif ('duplex' in url_pat):
        object_type = "duplex"
    elif ('penthouse' in url_pat):
        object_type = "penthouse"

    for x in page_links:
        item_links_extractor(x,object_type,deal_type)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(main_extractor,item_links)
    print("Complete")

page_links = []
item_links = []
records = []


#Sell
url_pat_sell_apart = 'https://imobiliare-herastrau.ro/properties-search/page/{}/?status=de-vanzare&type%5B0%5D=apartament&min-price=0&max-price=99999999&min-area=0&max-area=999999999&property-id#038;type%5B0%5D=apartament&min-price=0&max-price=99999999&min-area=0&max-area=2&property-id'
url_pat_sell_dupl = 'https://imobiliare-herastrau.ro/properties-search/page/{}/?status=de-vanzare&type%5B0%5D=duplex&min-price=0&max-price=99999999&min-area=0&max-area=999999999&property-id#038;type%5B0%5D=duplex&min-price=0&max-price=99999999&min-area=0&max-area=2&property-id'
url_pat_sell_pent ='https://imobiliare-herastrau.ro/properties-search/page/{}/?status=de-vanzare&type%5B0%5D=penthouse&min-price=0&max-price=99999999&min-area=0&max-area=999999999&property-id#038;type%5B0%5D=penthouse&min-price=0&max-price=99999999&min-area=0&max-area=5&property-id'
#Rent
url_pat_rent_apart = 'https://imobiliare-herastrau.ro/properties-search/page/{}/?status=de-inchiriat&type%5B0%5D=apartament&min-price=0&max-price=99999999&min-area=0&max-area=999999999&property-id#038;type%5B0%5D=apartament&min-price=0&max-price=99999999&min-area=0&max-area=2&property-id'
url_pat_rent_dupl = 'https://imobiliare-herastrau.ro/properties-search/page/{}/?status=de-inchiriat&type%5B%5D=duplex&min-price=0&max-price=99999999&min-area=0&max-area=999999999&property-id='
url_pat_rent_pent ='https://imobiliare-herastrau.ro/properties-search/page/{}/?status=de-inchiriat&type%5B%5D=penthouse&min-price=0&max-price=99999999&min-area=0&max-area=999999999&property-id='

#20,2,5,8




main(url_pat_sell_apart,20)
page_links = []
item_links = []
main(url_pat_sell_dupl,2)
page_links = []
item_links = []
main(url_pat_sell_pent,5)
page_links = []
item_links = []
main(url_pat_rent_apart,8)
page_links = []
item_links = []
main(url_pat_rent_dupl,1)
page_links = []
item_links = []
main(url_pat_rent_pent,1)


csv_saver()
