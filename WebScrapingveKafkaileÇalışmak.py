import requests
from bs4 import BeautifulSoup
import json
import time
from kafka import KafkaProducer

# Sayfayı çekme
adres = 'https://scrapeme.live/shop/'
yanıt = requests.get(adres)
soup = BeautifulSoup(yanıt.text, 'html.parser')

# Veriyi çıkarma
urunler = []
for urun in soup.find_all('li', class_='product'):
    title = urun.select_one('h2.woocommerce-loop-product__title').get_text(strip=True)
    price = urun.select_one('span.price').get_text(strip=True)
    urunler.append({'title': title, 'price': price})

# Elde edilen ürün bilgilerini yazdırma
print(urunler)

# Kafka'ya veri gönderme
producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda v: json.dumps(v,ensure_ascii=False).encode('utf-8'))
for product in urunler:
    producer.send('datasets', product)
    time.sleep(1)  # 1 saniyelik aralıki

# Verileri datasets.json dosyasına yazma
with open("datasets.json", "w", encoding='utf-8') as file:
    for data in urunler:
        file.write(json.dumps(data, ensure_ascii=False) + "\n")

print("Veri başarıyla datasets.json dosyasına yazıldı.")

