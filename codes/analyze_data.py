import pandas as pd

'''1.Load data'''
df = pd.read_csv('cleaned_data.csv')

'''2.View data'''
df.info()
df.head()
df = df.astype({'posted_year':int})#remove number after digit point of float type
df = df.astype({'posted_year':str})#convert data type in a line

'''3.Compare volumn of posts, mean of km group by brand, carmodel, city, district, posted_month'''
#brand
brand = df.groupby(['brand']).size().sort_values(ascending=False) #find the brand is posted the most
brand.head(10) #top 10 brand

#carmodel
carmodel = df.groupby(['brand', 'carmodel']).size().sort_values(ascending=False) #find the car model is posted the most

#city
df.groupby('city').size().sort_values(ascending= False) #Find the city is posted the most
hcm = df.groupby('city').get_group('Tp Hồ Chí Minh')
hcm.groupby('district').size().sort_values(ascending=False) #Find the district is posted the most in HCM city

#district
df.groupby(['city', 'district']).size().sort_values(ascending=False) #Find the district is posted the most
df.groupby('city').get_group('Lạng Sơn')
df[df['city'] == 'Sơn La'] #get post's info in Sơn La

#posted_month
df.groupby('posted_month').size() #All post on Feb>> scarped value is wrong >> chose wrong element

'''4.Sell Ratio'''
#Create a new dataframe 
top_posts = df.groupby(['brand','carmodel','year']).size().sort_values(ascending=False)
sell_ratio = top_posts.reset_index() #convert series (groupby result) into dataframe
sell_ratio.rename(columns={0:'num_posts'}, inplace=True) #change column name

#Filter manufacture year (2020,2021,2022)
sell_ratio = sell_ratio[sell_ratio['year'].isin(['2020','2021','2022'])]

#Filter brand which have data revenue in VAMA
filter_brand = ['Toyota','Ford','Honda','Mitsubishi','Kia','Mazda','Suzuki','Isuzu']
sell_ratio = sell_ratio[sell_ratio['brand'].isin(filter_brand)]

#Filter number of posts which quite large to analyze, after view unique value of num_posts, I chose 20
sell_ratio = sell_ratio[sell_ratio['num_posts'] > 20]

#Add data from VAMA statements
vama_data = [30251, 15650, 13291, 5485, 11365, 16447, 16844, 8512, 2793, 12033, 16122, 11803, 9745,
            13616, 19931, 4206, 18411, 6075, 1961, 5902, 7653, 3969, 14696, 5589, 3683, 5916, 1948,
            23529, 21473, 14104, 2478, 6352, 11404, 9812, 21983, 3195, 6526, 9775, 2813, 6065, 5406,
            9320, 4725, 5333, 9578, 5423, 2906, 5175, 867, 4471, 10505, 1076, 12700, 9446, 7214, 10230, 
            5854, 12398, 8334, 1710]

vama_report_2020 = 'http://vama.org.vn/Data/upload/files/2020/Thang12-2020/VAMA%20sales%20report%20December%202020%20-%20Detail.pdf'
vama_report_2021 = 'http://vama.org.vn/Data/upload/files/2021/Thang12-2021/VAMA%20sales%20report%20December%202021%20-%20Detail.pdf'
vama_report_2022 = 'http://vama.org.vn/Data/upload/files/2022/T12-2022/VAMA%20sales%20report%20December%202022%20-%20Detail.pdf'

sell_ratio['VAMA'] = vama_data
sell_ratio.info()
#Create a ratio column 
sell_ratio['sell_ratio'] = sell_ratio['num_posts'] / sell_ratio['VAMA'] *100
sell_ratio.to_csv('sell_ratio_chotot.csv', index=False)
'''5.Compare km between brands, car models'''
df.groupby('brand').mean()['km']
df.groupby(['brand', 'carmodel']).mean()['km']

'''6.Extract dataset for generating Visualization on Tableau'''
#num_posts, mean_km group by brand
brand = df.groupby(['brand']).agg({'km':['mean', 'count']}) #get 2 aggregate functions, extract a DataFrame
brand = brand.reset_index() #reset index
brand.columns = ['brand', 'mean_km', 'num_posts'] #change multiple column names
brand.to_csv('posts_km_groupby_brand.csv', index= False)

#num_posts, mean_km group by carmodel
carmodel = df.groupby(['brand', 'carmodel'])['km'].agg(['mean', 'size'])
carmodel = carmodel.reset_index()
carmodel.columns = ['brand', 'carmodel', 'mean_km', 'num_posts']
carmodel.to_csv('posts_km_groupby_carmodel.csv', index= False)

#num_posts group by city
city = df.groupby('city').size()
city = city.reset_index()
city.columns = ['city', 'num_posts']
city.to_csv('posts_groupby_city.csv', index= False)
#num_posts group by disctrict in HCM
hcm = df.groupby('city').get_group('Tp Hồ Chí Minh')
dis_hcm = hcm.groupby('district').size()
dis_hcm = dis_hcm.reset_index()
dis_hcm.columns = ['district', 'num_posts']
dis_hcm['city'] = 'Hồ Chí Minh' #add city column to get hcm's geographic data which used in tableau
dis_hcm.to_csv('posts_groupby_district_hcm.csv', index= False)
