
#precisa intall requests - !pip install requests
import requests as r  

url = 'https://api.covid19api.com/dayone/country/brazil'
resp = r.get(url)

#resp.status_code - se printar 200 é pq ta certo
raw_data = resp.json()
#raw_data[0] - só para visualizar

final_data = []
for obs in raw_data:
  final_data.append([obs['Date'], obs['Confirmed'], obs['Deaths'], obs['Active'], obs['Recovered']])
#final_data

final_data.insert(0, ['Data', 'Confirmados', 'Mortos', 'Ativos', 'Recuperados']) #header
#para referenciar >>>
data = 0
confirmados = 1
mortos = 2 
ativos = 3 
recuperados = 4

for i in range(1, len(final_data)):
  final_data[i][data] = final_data[i][data][:10]
#final_data - só para visualizar

import datetime as dt #biblioteca de datas
import csv

with open('brasil-covid.csv', 'w') as file: 
  writer = csv.writer(file)
  writer.writerows(final_data)

for i in range(1, len(final_data)):
  final_data[i][data] = dt.datetime.strptime(final_data[i][data], '%Y-%m-%d')

final_data

def get_datasets(y, labels): #função para datas
  if type(y[0]) == list:
    datasets = []
    for i in range(len(y)):
      datasets.append({
          'label': labels[i],
          'data': y[i] 
      })
    return datasets
  else:
    return [
            {
                'label' : labels[0],
                'data': y              
            }
    ]

def set_title(title= ''): #função pra titulo
   if title != '':
     display = 'true'
   else:
     display = 'false'
   return {
       'title' : title,
       'display' : display
   }

def create_chart(x, y, labels, kind='bar', title=''): #função pra criar o grafico
  
  datasets = get_datasets(y, labels)
  options = set_title(title)

  chart = {
      'type' : kind,
      'data':{
          'labels': x,
          'datasets': datasets
      },
      'options': options 

  }
  return chart

def get_api_chart(chart):
  url_base = 'https://quickchart.io/chart'
  resp = r.get(f'{url_base}?c={str(chart)}')
  return resp.content

def save_image(path, content):
  with open(path, 'wb') as image:
    image.write(content)

from PIL import Image
from IPython.display import display

def display_image(path):
  img_pil = Image.open(path)
  display(img_pil)

y_data_1 = []
for obs in final_data[1::15]:
  y_data_1.append(obs[confirmados])

y_data_2 = []
for obs in final_data[1::15]:
  y_data_2.append(obs[recuperados])

labels = ['Confirmados', 'Recuperados']

x = []
for obs in final_data[1::15]:
  x.append(obs[data].strftime('%d/%m/%Y'))

chart = create_chart(x, [y_data_1, y_data_2], labels, title= 'Gráfico Confirmados X Recuperados')
chart_content = get_api_chart(chart)
save_image('meu-primeiro-grafico.png', chart_content)
display_image('meu-primeiro-grafico.png')

from urllib.parse import quote
def get_api_qrcode(link):
  text = quote(link) 
  url_base = 'https://quickchart.io/qr'
  resp = r.get(f'{url_base}?text={text}')
  return resp.content

url_base = 'https://quickchart.io/chart'
link = f'{url_base}?c={str(chart)}'
save_image('qr-code.png', get_api_qrcode(link))
display_image('qr-code.png')
