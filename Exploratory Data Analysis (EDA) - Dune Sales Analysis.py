#!/usr/bin/env python
# coding: utf-8

# # Sales Analysis
# 
# Dune is a reputable global retailer offering a diverse selection of products, including accessories, clothing, and phones. With a growing presence in 14 countries and a team of over 70,000 employees, the company prides itself on providing affordable options for everyone. From fashion-forward trendsetters to multi-generational families, Dune strives to offer great quality essentials and standout styles that cater to a wide range of customers. 
# 
# My objective is to analyze the company's sales data from the previous year and provide actionable insights and recommendations. This analysis will help identify areas of opportunity and inform future business decisions aimed at improving performance and increasing profitability. 

# ### Exploratory Data Analysis (EDA) 
# 
# This is the process of analyzing and summarizing data in order to gain insights and understanding of the underlying patterns and relationships. The main objective of EDA is to identify and explore the main characteristics and patterns of the data, and to identify any anomalies or outliers that may impact subsequent analysis. 
# 
# EDA typically involves a number of steps, including 
# 
# 1. __Data cleaning:__ This involves removing or correcting any errors or inconsistencies in the data, such as missing values or incorrect values. 
# 2. **Data visualization:** Data visualization techniques are then used to graphically represent the data and identify any trends or patterns. 
# 3. **statistical analysis:** Statistical analysis is used to identify any relationships between variables and to test hypotheses about the data. This may involve calculating summary statistics such as mean and standard deviation, and performing tests such as correlation analysis and hypothesis testing.
# 
# These are the steps I will employ in this project.

# First, I will import necessary libraries:

# In[42]:


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import missingno as msno
from collections import Counter
import warnings
warnings.filterwarnings('ignore')


# Next, I will load the dataset and print the top 5 rows for assessment

# In[2]:


df = pd.read_csv(R"C:\Users\Mumsie\Downloads\Dune Sales Data.csv")
df.head()


# In[3]:


df.tail(3)


# Next, I will assess the data dimensionality (the number of rows and columns)

# In[4]:


df.shape


# In[5]:


df.columns


# Next, I will investigate the dataset for data types and anomalies

# In[6]:


df.info()


# In[7]:


# Numerical Statistical Analysis
df.describe()


# In[8]:


# Categorical Statistical Analysis
df.describe(include = ['object', 'bool'])


# Next, I will investigate the missing data

# In[9]:


df.isnull().sum()


# In[10]:


# Visualizing the missing data

plt.figure(figsize = (8,4))
sns.heatmap(df.isnull(), cbar=True, cmap='coolwarm');


# In[11]:


msno.bar(df, color='blue');


# In[12]:


# Displaying where the missing data exists

df[df.isnull().any(axis=1)]


# Next, I will drop the missing data

# In[13]:


df.dropna(inplace=True)
df.isnull().sum()


# In[14]:


# Datetime Analysis
df.head(2)


# Next, I will convert the date column into a pandas datetime object

# In[24]:


df['Date'] = pd.to_datetime(df['Date'])
df.info()


# Next, I will extract the Year, Month, and Quarter

# In[25]:


df['year'] = df['Date'].dt.year
df['month'] = df['Date'].dt.month
df['month_name'] = df['Date'].dt.month_name()
df['quarter'] = df['Date'].dt.quarter

df.head(2)


# Next, I will group customer age

# In[26]:


def age_group(age):
    if age <= 25:
        return '<=25 Young Adult'
    elif age <= 40:
        return '26-40 Adult'
    elif age <= 50:
        return '41-50 Old Adult'
    else:
        return '>=51 Elder'

df['age_group'] = df['Customer_Age'].apply(age_group)

df.head(2)


# Next, I will calculate Cost, revenue, and Profit

# In[27]:


df['cost'] = df['Quantity'] * df['Unit_Cost']
df['revenue'] = df['Quantity'] * df['Unit_Price']
df['profit'] = df['revenue'] - df['cost']

df.head(2)


# In[28]:


# Profit/Loss grouping

def porl(x):
    if x >= 0:
        return 'Profit'
    else:
        return 'Loss'
    
df['profit_label'] = df['profit'].apply(porl)
df.head(3)


# ### Univariate Analysis
# 
# First, I will be analyzing the distribution and summary statistics of individual variables/columns.

# #### Categorical Data Vizualization

# In[29]:


df.columns


# In[32]:


# investigating the customer column
sns.countplot(x='Customer', data=df);


# > It can be seen from the countplot that there is an erroneous category called "Hign".
# >
# > I will investigate the affected column(s)

# In[33]:


df[df['Customer'] == "Hign"].head(3)


# Next, I will correct the spelling of "HIGN"

# In[34]:


df.loc[df['Customer'] == 'Hign', 'Customer'] = 'High'

sns.countplot(x=df['Customer'])
plt.title('Customer Frequency per Customer category');

df['Customer'].value_counts()


# >The countplot displays the distribution of customers across three categories: 'Low', 'Medium', and 'High'. 'Low category' has the highest frequency(13,041 customers), followed by 'Medium'(12,926 customers), and 'High' has the lowest frequency(8,899 customers).
# >
# >This provides a clear visual representation of the distribution of customers across different categories, which can be useful for understanding the customer base and making business decisions based on customer segmentation.

# Next, I will investigate number of transactions by sales person

# In[35]:


plt.figure(figsize = (8,5))
ax = sns.countplot(x=df['Sales Person'], order=df['Sales Person'].value_counts(ascending=False).index)
values = df['Sales Person'].value_counts(ascending=False).values
ax.bar_label(container=ax.containers[0], labels=values)
plt.title('Count of transactions by salesperson');


# > The countplot represents the number of transactions carried out by each salesperson.
# >
# > From the countplot, we can observe that: 'Remota' had the highest number of transactions, with 6,667 transactions. 'Chinazam' follows closely with 6,556 transactions. 'Feyisola' and 'Suleman' had 6,129 and 4,618 transactions, respectively. There are also salespersons with lower transaction counts, including 'Segun', 'Derick', and 'Kenny'.
# >
# > This analysis provides insights into the distribution of transactions among different salespersons, which can be valuable for evaluating individual sales performance and making informed decisions about sales strategies or resource allocation.

# Next, I will investigate Total transactions by Customer Age group

# In[41]:


plt.figure(figsize = (15,5))

ax = sns.countplot(y=df['age_group'], order=df['age_group'].value_counts(ascending=False).index)
values = df['age_group'].value_counts(ascending=False).values
ax.bar_label(container=ax.containers[0], labels=values)
plt.title('Count of transactions by Customer Age Group');


# > The countplot titled "Count of transactions by Customer Age Group" visually represents the distribution of transactions among different age groups of customers. The age groups are divided into four categories:
# > - "26-40 Adult": This age group had the highest number of transactions, with a count of 17,015 transactions.
# > - "41-50 Old Adult": This age category had the second-highest number of transactions, totaling 7,507.
# > - "<=25 Young Adult": This age group had 6,076 transactions.
# > - ">=51 Elder": The ">=51 Elder" category had the fewest transactions, with a count of 4,268.
# >
# > This analysis provides insights into the distribution of transactions among different age groups of customers. It indicates that the "26-40 Adult" age group had the highest engagement in terms of transactions, followed by the "41-50 Old Adult" group, while the ">=51 Elder" group had the lowest transaction count. Understanding transaction distribution by age groups can be useful for tailoring marketing and sales strategies to specific customer segments.

# Next, I will investigate Total transactions by Customer Gender

# In[45]:


fig,ax = plt.subplots(figsize = (5,5))
count = Counter(df['Customer_Gender'])
ax.pie(count.values(), labels=count.keys(), autopct=lambda p:f'{p:.2f}%')
ax.set_title('Percentage of Transactions by Gender')
plt.show();


# > The pie chart provides a visual representation of the distribution of transactions between different customer genders. In this case, there are two categories: "F" for Female and "M" for Male. The pie chart indicates the percentage of transactions attributed to each gender category.
# > - "F" (Female) represents approximately 50.02% of the total transactions.
# > - "M" (Male) represents nearly 49.98% of the total transactions.
# >
# > This analysis demonstrates that the dataset has a nearly equal distribution of transactions between the two genders, with females accounting for a slightly higher percentage. Understanding the gender distribution of transactions can be valuable for marketing and product targeting strategies, as it helps in tailoring approaches to specific customer segments.

# Next, I will investigate Total transactions by State

# In[48]:


plt.figure(figsize=(12,5))
top10 = df['State'].value_counts().head(10)
sns.countplot(x=df['State'], order=top10.index)
plt.title('Top 10 transactions by State');

print(top10)


# > The bar chart provides a visual representation of the distribution of transactions across different states. It focuses on the top 10 states with the highest number of transactions. Among the top 10 states with the highest transaction counts, "Lagos" leads with approximately 10,332 transactions. "Abuja" and "Abia" follow closely with 6,421 and 5,206 transactions, respectively.
# The remaining states in the top 10 also contribute significantly to the transaction count, with varying numbers of transactions.
# >
# > This analysis provides insights into the geographic distribution of transactions, highlighting which states have the highest transaction volumes. This information can be valuable for the business to allocate resources effectively, target marketing efforts, and identify regions with potential for growth or improvement in sales and customer engagement.

# Next, I will investigate Total transactions by Sub Category

# In[51]:


plt.figure(figsize = (13,5))

ax = sns.countplot(y=df['Sub_Category'], order=df['Sub_Category'].value_counts(ascending=False).index)
values = df['Sub_Category'].value_counts(ascending=False).values
ax.bar_label(container=ax.containers[0], labels=values)
plt.title('Count of transactions by Sub Category');


# > The bar chart provides a visual representation of the distribution of transactions across different sub-categories of products. It focuses on identifying which sub-categories are the most popular among customers. The sub-category "Keyboard" stands out as the most popular among customers, with approximately 11,112 transactions. "Ear Piece" and "Wrist Watch" follow, with 5,295 and 4,176 transactions, respectively. Other sub-categories like "Samsung," "IPhone," and "Jerseys" also have a significant number of transactions.
# >
# > This analysis is valuable for understanding customer preferences and which product sub-categories are in high demand. The business can use this information to optimize their inventory, marketing strategies, and product offerings to cater to customer preferences effectively.

# Next, I will investigate Total transactions by Product Category

# In[59]:


pc = df['Product_Category'].value_counts()
plt.pie(pc, labels=pc.index, autopct='%1.1f%%', wedgeprops={'width': 0.6});


# > The pie chart provides a clear breakdown of the total transactions based on product categories. There are three primary product categories which include:
# > - Accessories: This category represents the largest share of transactions, accounting for approximately 64.6% of the total transactions. Customers seem to have a significant preference for purchasing accessories.
# > - Phones: The second-largest category is "Phones," which makes up about 20.3% of the total transactions. 
# > - Clothing: Clothing transactions contribute the remaining portion, constituting around 15.0% of the total transactions. This category has a smaller share compared to accessories and phones but still represents a notable segment of customer purchases.
# >
# > This pie chart effectively illustrates the distribution of transactions across different product categories, helping the business understand which categories are the most popular among customers.

# Next, I will investigate Total transactions by Payment Option

# In[63]:


po = df['Payment Option'].value_counts()
plt.pie(po, labels=po.index, autopct='%1.1f%%', wedgeprops={'width': 0.6});

print(po)


# > The pie chart visually represents the distribution of transactions across different payment options. There are three primary payment options including:
# > - Cash: Cash transactions appear to be the most common payment method, accounting for the majority of transactions at approximately 45.6%. This suggests that a significant portion of customers prefers to make payments in cash.
# > - POS (Point of Sale): The POS payment option represents the second-largest segment, comprising about 31.6% of the total transactions. It indicates that a substantial number of customers opt for electronic payments using POS terminals.
# > - Online: Online payments, likely made through digital platforms or internet banking, make up the remaining portion, approximately 22.8% of the total transactions. While the smallest segment, it still represents a noteworthy share of the payment methods chosen by customers.
# >
# >This pie chart provides valuable insights into the distribution of transactions across different payment options, allowing you to understand the preferred methods of payment among your customers.

# Next, I will investigate Total transactions by Month (month name)

# In[69]:


plt.figure(figsize = (12,5))
ax = sns.countplot(x=df['month_name'], order=df['month_name'].value_counts(ascending=False).index)
values = df['month_name'].value_counts(ascending=False).values
ax.bar_label(container=ax.containers[0], labels=values)
plt.title('Count of Transactions by Month');

df['month_name'].value_counts()


# > This bar chart provides insights into the distribution of transactions across different months.
# > - **June and May:** These two months reflect the periods with the highest transaction counts. June recorded the highest, with approximately 3,680 transactions, closely followed by May, with 3,676 transactions. This suggests that the middle of the year experiences a peak in sales or activities, possibly due to seasonal factors or promotional events.
# > - **December:** December ranks third in terms of transaction volume, with around 3,414 transactions. It's common for December to be a busy month for many businesses due to holiday shopping and year-end festivities.
# > - **April and March:** These months also show notable transaction counts, with around 3,283 and 3,155 transactions, respectively. It's possible that these months have specific events or promotions driving customer activity.
# > - **January and February:** The beginning of the year sees somewhat lower transaction counts, with January having around 2,907 transactions and February with 2,887. This could be due to a post-holiday slowdown or customers recovering from holiday spending.
# > - **October, November, September, August, and July**: These months have progressively fewer transactions, with July having the lowest count at 2,215. This pattern may indicate a seasonal trend or variations in customer behavior throughout the year.
# >
# > Overall, this analysis provides valuable insights into the seasonality of transactions, helping the business understand the fluctuations in sales or activities over the course of a year. It can be instrumental in planning marketing strategies and inventory management to align with these trends.

# Next, I will investigate Total transactions by Profit or Loss

# In[70]:


fig,ax = plt.subplots(figsize = (5,5))
count = Counter(df['profit_label'])
ax.pie(count.values(), labels=count.keys(), autopct=lambda p:f'{p:.2f}%')
ax.set_title('Percentage of Transactions by Profit or Loss')
plt.show();


# > This pie chart visually represents the distribution of transactions based on whether they resulted in a profit or a loss. 
# >
# > - The majority of transactions, accounting for approximately 86.08%, resulted in a profit. This indicates that the business is generally successful in generating revenue exceeding its costs for the majority of its transactions.
# >
# > - About 13.92% of transactions led to a loss. While this percentage is significantly smaller than the profitable transactions, it is still essential to pay attention to these cases. Analyzing the transactions that resulted in losses can help identify areas where cost management or revenue generation strategies may need improvement.
# >
# >This analysis provides a clear overview of the distribution of profitable and unprofitable transactions, which is valuable for assessing the overall financial health of the business. It suggests that the business is predominantly profitable, but further investigation into the characteristics of transactions leading to losses may offer insights for optimization and growth.

# #### Numerical Data Visualization
# 
# - Quantity
# - Cost
# - Revenue
# - Profit

# I will use subplots to visualize all 4 variables

# In[72]:


fig, axs = plt.subplots(2,2, figsize=(15,10))

sns.boxplot(x=df['Quantity'], ax=axs[0,0])
axs[0,0].set_title('Boxplot of Quantity Sold')

sns.boxplot(y=df['cost'], ax = axs[0,1])
axs[0,1].set_title('Boxplot of Cost')

sns.boxplot(y=df['revenue'], ax = axs[1,0])
axs[1,0].set_title('Boxplot of Revenue')

sns.histplot(x=df['profit'], ax = axs[1,1])
axs[1,1].set_title('Histogram of Profit');


# > **Boxplot of Quantity Sold (Top Left):** 
# This boxplot visualizes the distribution of the "Quantity" feature.
# The box represents the interquartile range (IQR), which contains the middle 50% of the data.
# The line inside the box indicates the median (50th percentile) of the data.
# The whiskers extend to the minimum and maximum values within a defined range (usually 1.5 times the IQR) or to the actual data points.
# Any points beyond the whiskers are considered outliers. In this case, there are no outliers.
# >
# > **Boxplot of Cost (Top Right):** 
# This boxplot visualizes the distribution of the "cost" feature.
# Similar to the previous boxplot, it shows the IQR, median, and outliers.
# There are a few outliers on the higher side of the distribution.
# >
# > **Boxplot of Revenue (Bottom Left):** 
# This boxplot visualizes the distribution of the "revenue" feature.
# Like the previous plots, it displays the IQR, median, and outliers.
# There are outliers on present on the higher side of the distribution.
# > 
# > **Histogram of Profit (Bottom Right):**
# This histogram shows the distribution of the "profit" feature.
# The x-axis represents the profit values, while the y-axis shows the frequency (how many data points fall into each bin).
# It appears that most of the profit values are concentrated around a certain range, creating a peak in the histogram. 
# >
# > These visualizations help to understand the spread and central tendency of the respective features, as well as identify potential outliers.

# # Bivariate Analysis
# Involves analysing relationship between two variables
# 
# - I will focus on Profit for this analysis

# In[74]:


df.columns


# In[76]:


# Categorical columns

fig, axs = plt.subplots(2,3, figsize = (27,10))

cust_prof = df.groupby('Customer')['profit'].sum().reset_index()
sns.barplot(x='Customer', data=cust_prof, y='profit', ax=axs[0,0])
axs[0,0].set_title('Profit by Customer Type')

sp_prof = df.groupby('Sales Person')['profit'].sum().reset_index()
sns.barplot(x='Sales Person', data = sp_prof, y='profit', ax=axs[0,1])
axs[0,1].set_title('Profit by Sales Person')

ag_prof = df.groupby('age_group')['profit'].sum().reset_index()
sns.barplot(x='age_group', data = ag_prof, y='profit', ax=axs[0,2])
axs[0,2].set_title('Profit by Age Group')

pc_prof = df.groupby('Product_Category')['profit'].sum().reset_index()
sns.barplot(y='Product_Category', data=pc_prof, x='profit', ax=axs[1,0])
axs[1,0].set_title('Profit by Product Category')

po_prof = df.groupby('Payment Option')['profit'].sum().reset_index()
sns.barplot(y='Payment Option', data=po_prof, x='profit', ax=axs[1,1])
axs[1,1].set_title('Profit by Payment Option')

sc_prof = df.groupby('Sub_Category')['profit'].sum().reset_index()
sns.barplot(y='Sub_Category', data=sc_prof, x='profit', ax=axs[1,2])
axs[1,2].set_title('Profit by Sub-Category');


# > **Profit by Customer Type (Top Left):**
# This bar chart compares the total profits generated by different customer types: Low, Medium, and High.
# It can be seen that the "Low" category of customers has generated the highest profit, followed closely by the "Medium" customers, while "High" customers have the lowest profit contribution.
# >
# > **Profit by Sales Person (Top Center):**
# This bar chart illustrates the total profits earned by each salesperson.
# Among the salespersons, "Feyisola" has generated the highest profit, followed by "Remota," and "Chinazam." "Derick" has the lowest profit contribution.
# >
# > **Profit by Age Group (Top Right):**
# This bar chart displays the total profits generated by customers grouped into different age categories.
# The "26-40 Adult" age group has contributed the highest profit, followed by "41-50 Old Adult" and "<=25 Young Adult" age groups. ">=51 Elder" customers have the lowest profit contribution.
# >
# > **Profit by Product Category (Bottom Left):** 
# This bar chart compares the total profits generated by different product categories: Accessories, Phones, and Clothing.
# "Accessories" have generated the highest profit, followed by "Clothing," while "Phones" have the lowest profit contribution.
# >
# > **Profit by Payment Option (Bottom Center):**
# This bar chart shows the total profits based on payment options: Cash, POS (Point of Sale), and Online.
# "Cash" transactions have generated the highest profit, followed by "POS," while "Online" transactions have generated the least profit.
# > 
# > **Profit by Sub-Category (Bottom Right):** 
# This bar chart compares the total profits earned from different sub-categories of products.
# "Keyboard" sub-category has generated the highest profit, followed by "Wrist Watch," and "Jerseys." "Socks" and "Memory Card" have the lowest profit contribution among sub-categories.
# > 
# > - These visualizations provide insights into how profits are distributed across various categorical columns. They can help identify trends and areas that might need further investigation or optimization.

# In[77]:


df.columns


# In[78]:


# Numerical Columns

fig, axs = plt.subplots(2,2, figsize = (25,10))

sns.boxplot(x=df['Quantity'], y=df['profit'], ax=axs[0,0])
axs[0,0].set_title('Quantity and Profit')

sns.boxplot(x='Product_Category', data=df, y='profit', ax=axs[0,1])
axs[0,1].set_title('Profit by Product Category')

sns.boxplot(x='age_group', data=df, y='profit', ax=axs[1,0])
axs[1,0].set_title('Profit by Age Group')

sns.scatterplot(x=df['Customer_Age'], y=df['profit'], ax=axs[1,1])
axs[1,1].set_title('Relationship between Customer Age and Profit');


# > **Quantity and Profit (Top Left):** 
# This boxplot compares the distribution of profits concerning the quantity of items sold.
# It does show very slight variations in profit across different quantities. Outliers are present across all boxplots.
# >
# > **Profit by Product Category (Top Right):**
# This boxplot visualizes the distribution of profits within different product categories: Accessories, Phones, and Clothing.
# It provides insights into the profit distribution among product categories. "Phones" have a wider profit range compared to "Clothing" and "Accessories".
# >
# > **Profit by Age Group (Bottom Left):** 
# This boxplot illustrates the distribution of profits among different customer age groups.
# It indicates variations in profit among different age groups. "<=25 Young Adult" customers seem to have the smallest range of profit compared to other age groups.
# >
# > **Relationship between Customer Age and Profit (Bottom Right):** 
# This scatterplot explores the relationship between customer age and profit.
# It does not reveal a linear correlation between customer age and profit. However, it does show that profits are distributed across a wide range of customer ages.
# 
# > - These visualizations provide insights into the relationships and distributions involving numerical columns in the Dune dataset. They can help identify potential patterns or outliers and guide further analysis. 

# # Multivariate Analysis
# ...involves analyzing the relationship between three or more variables

# In[79]:


df.columns


# In[80]:


# Product Category against cost, revenue, and profit

procat = df.groupby('Product_Category')[['cost', 'revenue', 'profit']].sum().reset_index()
procat = pd.melt(procat, id_vars = 'Product_Category', var_name = 'Metric', value_name = 'Total')
sns.barplot(data=procat, x='Product_Category', y='Total', hue='Metric')
plt.title('Product Category by Cost, Revenue, and Profit');


# > The barplot visualizes the total cost, revenue, and profit associated with different product categories: Accessories, Clothing, and Phones. 
# >
# > Accessories generate a relatively low cost compared to their revenue, resulting in a reasonable profit margin.
# >
# > Clothing products also maintain a favorable profit margin, with costs lower than the revenue generated.
# >
# > Phones have a higher cost compared to the revenue they generate, resulting in a lower profit margin.
# >
# > - It can be seen that although the "Phones" category has high cost and revenue, its profit is relatively lower than "Accesories" and "Clothing" categories. Accesories bring in the most profit to the Dune business.
# >
# > - This visualization demonstrates the financial performance of different product categories in terms of cost, revenue, and profit. It's clear that Accessories and Clothing are more cost-effective, yielding higher profit margins compared to Phones, which have higher costs relative to their revenue. These insights can guide business decisions, such as resource allocation and marketing strategies, to maximize profitability.

# In[83]:


plt.figure(figsize = (15,5))
sns.lineplot(x='month', y='profit', data=df, hue='year');


# > In 2015, the line chart shows a period of recorded loss that occurs between February and June. During this period, the data points dip below zero, indicating that the company experienced a loss. However, starting from July, there is a notable shift, and the company transitions into a profit-making phase.
# >
# > The transition to profit in 2015 continues, and the year ends with significant profits. However, there is a slight dip in profits observed between month 6 (June) and month 7 (July).
# 
# Next, I will create a pivot table to observe the progression:

# In[84]:


df.pivot_table(values='profit', index='year', columns='month', aggfunc='sum')


# > The line chart and pivot table provide valuable insights into the profitability trends over two years, 2015 and 2016:
# >
# > The pivot table presents a more detailed breakdown of the profit/loss figures for each month in the years 2015 and 2016.
# >
# >In 2015, the company started the year with losses in the first half (months 1 to 6), with the lowest point occurring in March (month 3). However, the second half of the year (from July onwards) shows a remarkable turnaround, with substantial profits recorded as seen in the line chart. The highest profit occurs in December (month 12).
# >
# >In 2016, the company starts the year on a positive note, with profits in the first six months (months 1 to 6). However, the data for the remaining months of the year is not captured, so it's unclear yet how the year concluded.
# >
# > >Overall, these visualizations suggest that the company faced challenges and losses in the first half of 2015 but managed to turn things around, ending the year with substantial profits. The profitability trend in 2016 appears positive in the available data, but additional data for the remaining half of the year would provide a more complete picture of that year's performance.

# Next, I will explore the Customer Gender, Age group, and Profit

# In[87]:


plt.figure(figsize = (10,5))
sns.barplot(x='Customer_Gender', y='profit', data=df, hue='age_group');


# Next, I will create a pivot table to observe the numbers:

# In[90]:


df.pivot_table(values='profit', index='age_group', columns='Customer_Gender', aggfunc='sum')


# > The barplot visualization presents a multivariate analysis of customer gender, age group, and their respective contributions to profit. 
# >
# >Among female customers, the age group that contributes the most to profit is 41-50 Old Adults. The second-highest profit contribution among female customers comes from the 26-40 Adult age group. Both the <=25 Young Adult and >=51 Elder age groups also contribute to profits, with around 58 and 63, respectively.
# >
# >For male customers, the age groups 26-40 Adult and 41-50 Old Adults are the most significant contributors to profit. 
# > >Overall, it can be observed that both male and female customers in the 26-40 Adult and 41-50 Old Adult age groups are the primary contributors to profits, generating the highest profit figures.
# >
# > **Pivot Table Insights:** 
# >
# >The pivot table provides a summarized view of profit figures for each combination of age group and customer gender.
# >Among 26-40 Adults, male customers generate a profit of approximately 593,853.62, while female customers contribute around 509,089.54 in profit. Male customers in this age group appear to be slightly more profitable.
# >
# > In the 41-50 Old Adult category, both male and female customers contribute almost equally, with profits of around 261,019.12 and 259,447.64, respectively.
# >
# > For the <=25 Young Adult age group, female customers contribute more profit (approximately 194,125.09) compared to male customers (approximately 169,959.46).
# >
# > In the >=51 Elder age group, male customers generate slightly higher profits (approximately 140,191.10) compared to female customers (approximately 133,923.11).
# > > These insights suggest that the 26-40 and 41-50 age groups are key contributors to profits, with some variations based on gender within these groups. Additionally, the <=25 Young Adult age group shows a notable profit contribution among female customers.

# Next, I will check for significant relationships using correlation

# In[96]:


a = df.corr(numeric_only = True)
a


# In[99]:


f, ax = plt.subplots(figsize = (15,8))
sns.heatmap(a, vmax=.8, square=True, annot=True);


# > The correlation matrix shows the pairwise correlation coefficients between different numeric variables. Each number in the matrix represents how strongly two variables are related to each other.
# 
# 1. Profit vs. Customer Age (0.014): There is a very weak positive correlation (0.014) between customer age and profit. This suggests that as customer age increases, profit tends to increase slightly, but the relationship is not significant.
# 
# 2. Profit vs. Quantity (0.0031): The correlation between profit and quantity is also very weak (0.0031). There's almost no discernible relationship between the quantity of products sold and profit.
# 
# 3. Profit vs. Unit Cost (0.17): There is a modest positive correlation (0.17) between profit and unit cost. This implies that as unit cost increases, profit tends to increase as well, indicating a positive association.
# 
# 4. Profit vs. Unit Price (0.34): Profit has a stronger positive correlation (0.34) with unit price. This suggests that as the unit price of products increases, profit tends to increase, indicating a more significant positive relationship.
# 
# 5. Profit vs. Year (0.26): Profit has a moderate positive correlation (0.26) with the year. This indicates that over the years, there has been a positive trend in profit, with profit generally increasing as the years go by.
# 
# 6. Profit vs. Month (-0.19): There is a moderate negative correlation (-0.19) between profit and the month. This suggests that there may be some seasonality in profit, with profit decreasing slightly in certain months.
# 
# 7. Profit vs. Quarter (-0.2): Similarly, there is a moderate negative correlation (-0.2) between profit and the quarter. This implies that profit may vary throughout the year, with lower profits in certain quarters.
# 
# 8. Profit vs. Cost (0.2): Profit has a moderate positive correlation (0.2) with cost. This indicates that as the cost of producing or acquiring products increases, profit tends to increase as well.
# 
# 9. Profit vs. Revenue (0.4): Profit has a strong positive correlation (0.4) with revenue. This suggests that as revenue increases, profit tends to increase substantially, indicating a strong positive relationship between these two variables.
# 
# 10. Profit vs. Profit (1): The correlation of profit with itself is, of course, 1, as it represents the perfect correlation between a variable and itself.
# 
# > > In summary, the analysis shows that profit is most strongly positively correlated with variables like unit price and revenue, indicating that increasing unit prices and revenue tend to boost profit. On the other hand, profit is moderately negatively correlated with month and quarter, suggesting some seasonal variations. Customer age and quantity have very weak correlations with profit, indicating they have little influence on profit in your dataset. Additionally, profit is moderately positively correlated with variables like unit cost and cost, implying that as these costs increase, profit tends to increase as well.

# In[108]:


# Vizualisation using pairplot

sns.pairplot(df, height=2.5);


# > The pairplot allows for exploration of the relationships between multiple (numeric variables) in the dataset by displaying scatterplots for pairs of variables and histograms for individual variables along the diagonal. 
# >
# > - **Histogram Distributions:** The histograms along the diagonal of the pairplot reveal the distribution of each variable. It's notable that unit cost, unit price, cost, and revenue are all skewed to the right, indicating that these variables have a right-skewed distribution. In contrast, profit and customer age appear to be normally distributed with no outliers.
# >
# > - **Unit Cost and Unit Price:** There is a strong positive correlation between unit cost and unit price. This finding is intuitive since an increase in unit cost typically leads to a higher unit price, aligning with your expectations.
# >
# > - **Cost, Unit Cost, Unit Price, and Revenue:** Cost is positively correlated with unit cost, unit price, and revenue. This suggests that as unit cost increases, these variables also tend to increase. This observation could be due to the fact that higher unit costs lead to higher overall costs and, subsequently, higher prices and revenues.
# >
# > - **Revenue and Profit:** Revenue is positively correlated with profit, indicating that as revenue increases, profit tends to increase as well. This positive relationship is a common business expectation.
# >
# > - **Profit and Customer Age:** There appears to be no significant correlation between profit and customer age. This suggests that customer age does not strongly influence profit in your dataset.
# >
# > - **Profit and Cost:** Similarly, there seems to be no strong correlation between profit and cost. This implies that variations in cost are not strongly associated with changes in profit.
# > > Overall, the pairplot analysis provides a clear understanding of the relationships between these numeric variables. It confirms some intuitive expectations, such as the positive correlation between unit cost and unit price, while also highlighting the absence of strong correlations in certain areas, such as profit and customer age or profit and cost. These insights can guide further exploration and analysis of the Dune Business sales data, helping to make informed decisions based on the data's underlying patterns and relationships.

# ### Summary of Sales Data Analysis for Dune Company
# 
# > The analysis of Dune company's sales data from the previous year has yielded valuable insights and actionable recommendations aimed at improving performance and increasing profitability. The key findings and recommendations are as follows:
# >
# > **1. Profitability Trends:**
# > - Yearly Profit Growth: There is a positive trend in yearly profits, indicating that the company's financial performance is improving over time. This suggests that the company is moving in the right direction.
# > - Seasonal Variations: Seasonal variations were observed, with profits being lower in certain months and quarters. It's important for the company to investigate the factors contributing to these fluctuations and plan accordingly.
# >
# > **2. Customer Segmentation:** 
# > - Age and Gender Segmentation: Customers in the 26-40 and 41-50 age groups, regardless of gender, contribute significantly to profits. This suggests the importance of targeted marketing and product offerings for these segments.
# > - Unit Price Influence: Profit is positively correlated with unit price, indicating that adjusting pricing strategies for certain customer segments may lead to increased profitability.
# >
# > **3. Product and Cost Analysis:**
# > - Unit Cost and Unit Price Relationship: There is a strong positive correlation between unit cost and unit price. The company should carefully manage unit costs to maintain profitability while setting competitive unit prices.
# > - Cost and Revenue: Cost is positively correlated with revenue, suggesting that increased investments in product development and marketing may lead to higher revenues. However, cost management remains critical.
# >
# ### Actionable Recommendations: 
# > 1. Seasonal Planning: Develop seasonal marketing and inventory strategies to address fluctuations in profits. This could include targeted promotions, inventory adjustments, or product launches during peak seasons.
# > 2. Customer Targeting: Focus marketing efforts on the 26-40 and 41-50 age groups, as they are the primary contributors to profits. Tailor product offerings and promotions to align with their preferences.
# > 3. Pricing Optimization: Continuously assess and adjust pricing strategies to maximize profitability without alienating customers. Monitor the impact of price changes on profit closely.
# > 4. Cost Control: Implement cost control measures to ensure that increasing costs do not erode profit margins. Regularly review and optimize the supply chain and operational processes.
# >
# ### Future Business Decisions: 
# > 1. Data-Driven Decision-Making: Promote a data-driven culture within the company. Regularly analyze sales data to inform strategic decisions and stay agile in responding to market changes.
# > 2. Customer Experience Enhancement: Invest in improving the overall customer experience, which can lead to increased customer loyalty and potentially higher profits in the long term.
# > 3. Innovation and Product Development: Explore opportunities for innovation in product offerings to attract new customers and diversify revenue streams.
# > > In conclusion, the analysis of Dune company's sales data provides a comprehensive view of its performance and opportunities for growth. By addressing seasonal variations, targeting key customer segments, optimizing pricing and costs, and making data-driven decisions, the company can enhance profitability and position itself for long-term success in the market.
# 
