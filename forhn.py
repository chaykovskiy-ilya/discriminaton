import requests
from bs4 import BeautifulSoup
from datetime import datetime

def parse_first_page(text, variant=0):

    info_data = {}
    soup = BeautifulSoup(text, 'html.parser')   
    tables = soup.findAll('table')
    #
    table_rows =  tables[3+variant].findAll('tr')
    info_data['type'] = table_rows[0].text.strip().lower()
    info_data['name'] = table_rows[1].text.strip().lower()
    
    #Info 
    table_rows =  tables[5+variant].findAll('tr')
    print('Row in info:', len(table_rows))
    td = table_rows[0].find('td')
    str_date = td.text.split(':')[1].strip()
    info_data['date_of_vote'] = datetime.strptime(str_date, '%d.%m.%Y')
    
    td = table_rows[1].find('td')    
    info_data['total_records'] = int(td.text.split(':')[1].strip())

    #Columns
    temp = []
    table_rows =  tables[7+variant].findAll('tr')
    
    td = table_rows[0].findAll('td')
    for row in td:
        temp.append(row.text.strip().lower())
    
    #remove Статус кандидата. it is next 3 columns
    temp = temp[:-1]
    
    td = table_rows[1].findAll('td')
    for row in td:
        temp.append(row.text.strip().lower())
    
    print('Columns:', len(temp))

    info_data['columns'] = temp

    #links to pages
    a_href = tables[6+variant].findAll("a", href=lambda href: href and "number=" in href)
    links = [link['href'].strip() for link in a_href]

    info_data['links'] = links 

    return info_data

def parse_page(text, variant=0):
    """
    tables = soup.findAll('table')
    parser for tables[7]
    """
    rows = []
    soup = BeautifulSoup(text, 'html.parser')
    tables = soup.findAll('table')
    main_table = tables[7+variant]
    table_rows =  main_table.findAll('tr')

    for row in table_rows[2:]: #first 2 rows - columns name
        person = []
        tds = row.findAll('td')

        #
        temp = tds[0].text.strip().lower()
        person.append(temp)

        temp = tds[1].find('a', href=True)['href']
 
        person.append(temp)

        for column in tds[2:]:
            temp = column.text.strip().lower()
            person.append(temp)

        rows.append(person)
    return rows

        
def parse_person_page(text, variant=0):
    """

    """
    person = {}
    soup = BeautifulSoup(text, 'html.parser')
    tables = soup.findAll('table')
    main_table = tables[4+variant]
    table_rows =  main_table.findAll('tr')

    for row in table_rows[1:]: #first style
        tds = row.findAll('td')
        key = tds[1].text.strip() #key
        value = tds[2].text.strip().lower() #value
        person.update({key:value})

    return person

def parse_name_and_sex(str_fio):
    """
    """
    member = {}
    name = []
  
    temp = str_fio.strip().lower().split()

    if len(temp)>2:
        #determine sex by otchestvo
        if temp[-1][-2:] in ['на','зы']:#кызы
            member['sex']= 'f'
        else:
            if temp[-1][-2:] in ['ич', 'лы']:#оглы
                member['sex'] = 'm'

    if len(temp)==4 and (temp[-1][-2:] in ['зы', 'лы']):
        name = temp[0:2]
        name.append(temp[2] + ' ' + temp[3])
    if len(temp)==3:
        name = temp
    if len(temp)==2:
        name = temp

    if len(name)==0:
        None
    else:
        member['name'] = name
    
    return member
