import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

# f = open('country.csv','w')
# headers = "Country,Capital,Population,Currency \n"
# f.write(headers)
# f.close()

while True:
    name = input("Enter Country or 0 to exit: ").replace(' ','_').strip().title()
    if name=='0':
        break
    my_url = 'https://en.wikipedia.org/wiki/' + name
    uClient = uReq(my_url)
    page_HTML = uClient.read()
    uClient.close()

    page_soup = soup(page_HTML,'html.parser')
    containers = page_soup.findAll("th", {"class": "infobox-label"})

    # initialize
    # country_text, capital_text, population_text, currency_text = '-','-','-','-'

    # country name
    country = page_soup.find('span',{'class':'mw-page-title-main'})
    country_text = country.text.upper()

    # population
    population = page_soup.findAll('th',{'class':'infobox-header'})
    for p in population:
        if 'Population' in p.text:
            population_text = p.parent.next_sibling.td.text.split('[')[0].replace(',',' ').strip()

    # capital and currency
    for container in containers:
        if 'Capital' in container.text:
            capital_text = container.next_sibling.a.text
        
        if 'Currency' in container.text:
            currency_text = container.next_sibling.text

    with open('country.csv','a',encoding='utf-8') as file:
        file.write(country_text + ',' + capital_text + ',' + population_text + ',' + currency_text + '\n')

    del page_HTML
    
