import pandas as pd
import numpy as np

#chuyển địa chỉ thành số
def district_to_number(address, districts):
    for district, value in districts.items():
        if district in address:
            return value
    return 0


#chuyển nội thất thành số
def furniture_to_number(furniture, dict_furniture):
    for fur, value in dict_furniture.items():
        if fur.lower() in furniture.lower():
            return value
    return 2


raw_df = pd.read_csv('./Data/DSPhongTro.csv', sep='\t')

raw_df = raw_df.dropna(subset=['ID', 'Địa chỉ', 'Diện tích', 'Mức giá', 'Ngày đăng tin', 'Số phòng ngủ', 'Số toilet'])

#Loại bỏ dòng trùng lắp
raw_df.drop_duplicates(inplace=True)

raw_df = raw_df[raw_df['Mức giá'] != 'Thỏa thuận'].reset_index(drop=True) #bỏ những dòng nào có giá là 'thỏa thuận'

#Chuẩn hóa cột địa chỉ và nội thất
districts = pd.read_csv('./Data/address.txt', sep=':', header=None)
districts = districts.set_index(0)[1].to_dict()
dict_furniture = pd.read_csv('./Data/furniture.txt', sep=':', header=None).set_index(0)[1].to_dict()

raw_df['Địa chỉ'] = raw_df['Địa chỉ'].apply(lambda x: district_to_number(x, districts))
raw_df['Nội thất'] = raw_df['Nội thất'].apply(lambda x: furniture_to_number(x, dict_furniture))

#Chỉnh sửa kiểu dữ liệu cho từng cột
raw_df['ID'] = raw_df['ID'].astype('category')
raw_df['Mức giá'] = raw_df['Mức giá'].astype(np.float64)
raw_df['Ngày đăng tin'] = pd.to_datetime(raw_df['Ngày đăng tin'], format='%d/%m/%Y')
raw_df['Địa chỉ'] = raw_df['Địa chỉ'].astype('category')
raw_df['Nội thất'] = raw_df['Nội thất'].astype('category')

start_date = pd.to_datetime('01/10/2024', format='%d/%m/%Y')
end_date = pd.to_datetime('31/10/2024', format='%d/%m/%Y')
raw_df = raw_df[(raw_df['Ngày đăng tin'] >= '1/10/2024') & (raw_df['Ngày đăng tin'] <= '31/10/2024')]

#Lưu dữ liệu đã xử lý vào file csv
raw_df.to_csv('./Data/DSPhongTro_DaXuLy.csv', encoding='utf-8-sig', header=True, sep='\t')