import random
import csv
import pandas as pd
import json
import mysql.connector
from faker import Faker
from faker.providers import address, person
import random
import pymysql

#  bảng TRUONG

# Đường dẫn tới tệp Excel nguồn dữ liệu
excel_file = "C:\\Users\\buivu\\OneDrive\\Desktop\\đồ án 2\\danh-sach-truong-thpt-o-tphcm.xlsx"



# Đọc dữ liệu từ tệp Excel
df = pd.read_excel(excel_file)



# Lấy dữ liệu từ cột MATR trong tệp Excel
matr_data = df['MATR'].tolist()
tentr_data= df['TENTR'].tolist()
dchitr_data= df['DCHITR'].tolist()



# Tạo dữ liệu cho bảng TRUONG
truong_data = []
for matr, tentr, dchitr in zip(matr_data, tentr_data, dchitr_data):
    truong_data.append([matr, tentr, dchitr])



# Ghi dữ liệu vào tệp CSV
with open('truong.csv', 'w', newline='', encoding='utf-8') as truong_file:
    writer = csv.writer(truong_file)
    writer.writerow(['MATR', 'TENTR', 'DCHITR'])
    writer.writerows(truong_data)



# bảng HS



# Tạo dữ liệu cho bảng HS
fake = Faker('vi_VN')
fake.add_provider(address)
fake.add_provider(person)
hs_data = []
cccd_numbers_male = list(range(1, 500001))  # Số căn cước công dân cho giới tính nam
cccd_numbers_female = list(range(1, 500001))  # Số căn cước công dân cho giới tính nữ
random.shuffle(cccd_numbers_male)  # Sắp xếp ngẫu nhiên
random.shuffle(cccd_numbers_female)  # Sắp xếp ngẫu nhiên
for i in range(1, 1000001):
    mahs = f"HS{i:07}"
    ho = fake.last_name()
    ten = fake.first_name()
    
    if i <= 500000:
        gioi_tinh = "M"
        cccd = f"M{cccd_numbers[i-1]:06}"
    else:
        gioi_tinh = "F"
        cccd = f"F{cccd_numbers[i-500001]:06}"

    ntns = fake.date_of_birth(minimum_age=17, maximum_age=19).strftime("%d/%m/%Y")
    city_prefix = fake.city_prefix()
    dia_chi = fake.street_address_in_city(city_name='Hồ Chí Minh') + ', ' + fake.district_name_in_city(city_name='Hồ Chí Minh') + ', '  + 'Thành phố Hồ Chí Minh'
    data.append((mahs, ho, ten, cccd, ntns, dia_chi))



# Ghi dữ liệu vào tệp CSV
with open('hs.csv', 'w', newline='') as hs_file:
    writer = csv.writer(hs_file)
    writer.writerow(['MAHS', 'HO','TEN','CCCD','NTNS','DCHI_HS'])
    writer.writerows(hs_data)



# bảng hoc



# Tạo dữ liệu cho bảng HOC
hoc_data = []
for hs_row in hs_data:
    for _ in range(random.randint(1, 3)):
        hoc_data.append([hs_row[0], f'Mon hoc {random.randint(1, 10)}'])



# Ghi dữ liệu vào tệp CSV
with open('hoc.csv', 'w', newline='') as hoc_file:
    writer = csv.writer(hoc_file)
    writer.writerow(['MATR', 'MAHS','NAMHOC','DIEMTB','XEPLOAI','KQUA'])
    writer.writerows(hoc_data)



# PHẦN NÀY QUAN TRỌNG !!!



# Đọc thông tin xác thực từ file cấu hình
with open('config.json') as config_file:
    config = json.load(config_file)



# Ở đây vì em muốn nó mang 1 chút tính bảo mật, nên đã sử dụng 1 file cấu hình mạng để phòng khi mã nguồn có bị lộ ra thì các hacker vẫn không thể thực hiện sql injection được database gây mất mát dữ liệu
# Ý tưởng em học được qua những ngày chơi CTF và học pentest trên mạng, và vì muốn bám sát thực tế nhất có thể nên em đã thêm vào
# File cấu hình chính là file config.json, trong đó chứa thông tin như này:
#{
#  "host": "localhost",
#  "user": "root",
#  "password": "211031",
#  "database": "truonghoc1",
#}



# Thiết lập kết nối với cơ sở dữ liệu MySQL
conn = mysql.connector.connect(
    host=config['host'], 
    user=config['user'],
    password=config['password'],
    database=config['database']
)



# ĐÃ HẾT PHẦN QUAN TRỌNG



# Tạo con trỏ để thực hiện các truy vấn
cursor = conn.cursor()



# Chuyển dữ liệu từ tệp CSV vào bảng TRUONG
with open('truong.csv', 'r') as truong_file:
    truong_data = csv.reader(truong_file)
    next(truong_data)  # Bỏ qua dòng tiêu đề
    cursor.executemany('INSERT INTO TRUONG (matr, tentr, dchitr) VALUES (%s, %s, %s)', truong_data)



# Chuyển dữ liệu từ tệp CSV vào bảng HS
with open('hs.csv', 'r') as hs_file:
    hs_data = csv.reader(hs_file)
    next(hs_data)  # Bỏ qua dòng tiêu đề
    cursor.executemany('INSERT INTO HS (mahs, ho, ten, cccd, ntns, dchi_hs) VALUES (%s, %s ,%s ,%s ,%s , %s)', hs_data)



# Chuyển dữ liệu từ tệp CSV vào bảng HOC
with open('hoc.csv', 'r') as hoc_file:
    hoc_data = csv.reader(hoc_file)
    next(hoc_data)  # Bỏ qua dòng tiêu đề
    cursor.executemany('INSERT INTO HOC (matr, mahs, namhoc, diemtb, xeploai, ketqua) VALUES (%s, %s ,%s ,%s ,%s , %s)', hoc_data)



# Lưu các thay đổi vào cơ sở dữ liệu
conn.commit()



# Đóng kết nối và con trỏ
cursor.close()
conn.close()
