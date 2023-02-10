import pandas as pd

'''Load data'''
df = pd.read_csv('data.csv')

'''Get briefly of dataset'''
df.head()
df.info() 
df.describe()
df.columns

'''Cleaning empty value'''
#View the empty value
df[df.isnull().any(axis=1)] 
km_mode = df['km'].mode() #find mode value and ignore NaN value
km_mode = float(km_mode) #mode() function create object so have to change data type before use on fillna method
df['km'].fillna(km_mode, inplace=True) 

#View again include brand, carmodel so drop the rest of na
df.dropna(inplace=True) 

'''Cleaning wrong format'''
df.info()
convert_dict = {'km':int, 'price':int, 'posted_year':str}
df = df.astype(convert_dict)

'''Check wrong data in city'''
#view unique in city column
set(df['city']) #do not have misspelling and obey the standard

'''Remove duplicates'''
df.duplicated() #All is False >> no duplicates

'''#Save dataset after cleaning'''
df.to_csv('cleaned_data.csv', index=False) #remove index number

