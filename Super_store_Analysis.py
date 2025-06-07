import pandas as pd ;
import numpy as np;
import matplotlib.pyplot as plt;


# importing the csv file 


df = pd.read_csv("train.csv")
print(df.head())

#general overview of the data 

print(df.info())


# calculating number of null values 

null_count = df["Postal Code"] .isnull().sum()
print(null_count)


#filling 0 with empty coloumn 

df["Postal Code"].fillna(0,inplace=True)

#changing from float to integers 

df["Postal Code"] = df["Postal Code"].astype(int)

print(df.info())



#Data DEscriptiion 

print(df.describe())



#data Cleaning 

#Chechk I =f duplicates are avaliabel ":


if df.duplicated().sum()>0:
    print("Duplicates are present ")
else :
    print("No duplicates are present ") 
print(df.duplicated())


df.duplicated(keep = False).sum()


# EDA (EXPLORATORYY DATA ANALYSIS )

#Customer Analysis 

#type of Customers

type_Of_customers  =df["Segment"].unique()

print(type_Of_customers)



#no.of customer in each segment 

number_of_customers = df['Segment'].value_counts().reset_index()
number_of_customers.columns = ['Customer Type', 'Total Customers']
print(number_of_customers)

plt.pie(
    number_of_customers['Total Customers'],   # numeric sizes
    labels=number_of_customers['Customer Type'],  # slice labels
    autopct='%1.1f%%',
    startangle=90
)
plt.title('Distribution of Customers by Segment')
plt.show()


# sales target

sales_per_category = df.groupby('Segment')['Sales'].sum().reset_index()
#sales_per_category = sales_per_category.columns.str.strip()
#sales_per_category.columns = ['Customer Type ', 'Total Sales']
print(sales_per_category)


plt.pie(
    sales_per_category['Sales'],           # use 'Sales', not 'Total Sales '
    labels=sales_per_category['Segment'],  # use 'Segment', not 'Customer Type'
    autopct='%1.1f%%',
    startangle=90
)
plt.title("Distribution of Sales")
plt.show()


#Bar GRaph

plt.bar(sales_per_category['Segment'], sales_per_category['Sales'])

#title
plt.title('Sales per customer Category')
plt.xlabel('Segment')
plt.ylabel('Sales')

plt.show()


#Customer Loyalty Repeated Purchased Customer 

print(df.head())

cutomer_order_freq = df.groupby(['Customer ID','Customer Name','Segment'])['Order ID'].count().reset_index()
#rename column order id with total orders 
customer_order_freq = cutomer_order_freq.rename(columns={'Order ID':'Total orders'})
#Identify repeated customer 
repeat_customer = customer_order_freq[customer_order_freq['Total orders']>=1]
#sorted repeated customer
sorted_repeat_customer = repeat_customer.sort_values(by = 'Total orders',ascending = False)

print(sorted_repeat_customer.head(10).reset_index(drop =True))

# Ranking Customer in terms of sales 

customer_sales = df.groupby(['Customer ID' , 'Customer Name','Segment'])['Sales'].sum().reset_index()

#Sort in descending order 

top_spenders = customer_sales.sort_values(by ='Sales',ascending=False)

print(top_spenders.head(10).reset_index(drop=True))



#Mode Of shipping used to deleviery by Super Store 


ship_mode = df['Ship Mode'].unique()
print(ship_mode)


#Frequency used by Shipping Methods 

shipping_mode = df['Ship Mode'].value_counts().reset_index()
shipping_mode = shipping_mode.rename(columns={'count':'use Frequency','Ship Mode':'Mode Of Shipment'})
print(shipping_mode)

plt.pie(
    shipping_mode['use Frequency'],
    labels = shipping_mode['Mode Of Shipment'],
    autopct= '%1.1f%%',
    startangle = 90 

)

plt.title("Frquency plot By Shipping ")
plt.show()


# Geographical Analysis By City 

state = df['State'].value_counts().reset_index()
state = state.rename(columns={'count':'State','State':'No. of Customer'})
print(state.head(10))

#CUstomer By City 


city = df['City'].value_counts().reset_index()
city = city.rename(columns={'count':'City','City':'No. of Customer'})
print(city.head(10))



#sales Per State and Grouping State and sales 

state_sales = df.groupby(['State'])['Sales'].sum().reset_index()

top_state_sales =state_sales.sort_values(by='Sales',ascending =False)
print(top_state_sales.head(10))

#sales Per State and Grouping city and sales

city_sales = df.groupby(['City'])['Sales'].sum().reset_index()

top_city_sales =city_sales.sort_values(by='Sales',ascending =False)
print(top_city_sales.head(10))

# Product Analysis 

Product_Analysis = df['Category'].unique()
print(Product_Analysis)


# group by Sub Category 

subcategory = df.groupby(['Category','Sub-Category']).nunique().reset_index()
subcategory =subcategory.sort_values(by ='Sub-Category',ascending=False)
print(subcategory.reset_index(drop=True))

# Sales Per Category Product 

category_sales = df.groupby(['Category'])['Sales'].sum().reset_index()

category_sales= category_sales.sort_values(by = 'Sales',ascending=False)
print(category_sales.reset_index(drop=True))


#Plotting a pie chart 

plt.pie(category_sales['Sales'],
        labels = category_sales['Category'],
        autopct= '%1.1f%%',
        startangle= 90
        )
plt.title("Top Product Based on sales ")

plt.show()

#Group data by product Subcategry and sales

pdt_Sub = df.groupby(['Sub-Category'])['Sales'].sum().reset_index()

#Sorting in descending 

top_pdt_Sub = pdt_Sub.sort_values(by= 'Sales',ascending = False)
print(top_pdt_Sub.reset_index(drop = True))


plt.barh(top_pdt_Sub['Sub-Category'],top_pdt_Sub['Sales'])
#Label
plt.title("Total Producty Sub Category")
plt.xlabel("Product Sub Category")
plt.ylabel("Total Sales ")

plt.show()


# Sales Trend Analysis 


df['Order Date'] = pd.to_datetime(df['Order Date'],dayfirst=True)

#grouping hear by year and summing the sales per yeatr 

yearly_sales = df.groupby(df['Order Date'].dt.year)['Sales'].sum()

#setting new index and renaming the columns 
yearly_sales =yearly_sales.reset_index()
yearly_sales = yearly_sales.rename(columns={'Order Date':'Year','Sales':'Total Sales'})

print(yearly_sales)


#plotting bar graph 

plt.bar(yearly_sales['Year'],yearly_sales['Total Sales'])
#Label
plt.title("Yearly Sales ")
plt.xlabel("Total Sales")
plt.ylabel("Year ")
plt.xticks(rotation = 65 )

plt.show()

#Plotting line graph 

plt.plot(yearly_sales['Year'],yearly_sales['Total Sales'],marker = 'o',linestyle = '--')
#label
plt.title("Yearly Sales ")
plt.xlabel("Total Sales")
plt.ylabel("Year ")
plt.xticks(rotation = 65 )

plt.show()
 

 #Quaterly Sales 
df['Order Date']=pd.to_datetime(df['Order Date'],dayfirst=True)
year_sales = df[df['Order Date'].dt.year == 2018]
quaterly_sales =year_sales.resample('Q',on='Order Date')['Sales'].sum()
quaterly_sales= quaterly_sales.reset_index()
quaterly_sales=quaterly_sales.rename(columns={'Order date':'Quater','Sales':'Total Sales'})
print("this are quaterly sales  for 2018 ")

print(quaterly_sales)


plt.plot(quaterly_sales['Order Date'],quaterly_sales['Total Sales'],marker='o',linestyle='--')
plt.title("Quaterly sales for 2018 ")

plt.xlabel("Total Sales")
plt.ylabel("Quaterly Year ")
plt.xticks(rotation = 65 )

plt.show()






