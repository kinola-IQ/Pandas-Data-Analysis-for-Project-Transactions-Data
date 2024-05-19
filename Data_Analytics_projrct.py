# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 12:48:27 2023

@author: Akin
"""


'''
    KEY OBJECTTIVES
    1.) READ IN DATA FROM MULTIPLE CSV FILES
    2.) EXPLORE THE DATA(MILLIONS OF ROWS!)
    3.) CREATE NEW COLUMNS TO AID IN ANALYSIS
    4.) FILTER , SORT AND AGGREGATE THE DATA TO PINPOINT AND SUMMARIZE IMPORTANT INFORMATION
    5.) BUILD PLOTS TO COMMUNICATE KEY INSIGHTS

    COLUMNS TO WORK WITH:
    PROJECT_TANSACTIONS.CSV AND PRODUCT.CSV(BRIEFLY)
'''

import pandas as pd
import seaborn as sns
sns.set_style('darkgrid')


''' 
    FIRST READ IN TRANSACIONS DATA AND EXPLORE IT
    * TAKE A LOOK AS THE RAW DATA,THE DATATYPES AND CAST DAY,QUANTITY,STORE_ID AND WEEK_NO COLUMNS
    TO THE SMALLEST APPROPRIATE DATATYPE,CHECK THE MEMORY REDUCTION BY DOING SO
'''
project_transactions= pd.read_csv('C:/Users/akinola/Documents/python DATA ANALYTICS files/Pandas Course Resources/project_data/project_transactions.csv',
                                  )
                      
                      
this sections is to check the dtype and downcast accordingly to reduce memory usage
print(project_transactions['WEEK_NO'].max())

project_transactions =(project_transactions
                        .astype(
                            {
                            
                            'DAY':'int16',
                           
                            'QUANTITY':'int32',
                            
                            'STORE_ID':'int32',
                            
                            'WEEK_NO':'int8'
                            })
                        )
print(project_transactions.info(memory_usage='deep'))
# ORIGINAL memory usage: 180.1 MB
# NEW memory usage: 137.1 MB

'''    
    IS THERE ANY MISSING DATA?
'''
print(project_transactions.isna().sum())
#there appears to be no missing data
'''
    
    * HOW MANY UNIQUE HOUSEHOLDS AND PRODUCTS ARE THERE IN THE DATA?,
    THE FIELDS HOUSEHOLD_KEY AND PRODUCT_ID WILL HELP HERE
'''
print(project_transactions[['household_key','PRODUCT_ID']].nunique())
#   THE NUMBER OF UNIQUE HOUSEHOLDS AND PRODUCTS ARE:
#household_key     2099
#PRODUCT_ID       84138



                      

 '''
         COLUMN CREATION
create two columns
A column thatcaptures the total_discount by row(sum of [retail_disc],[coupon_disc])
The percentage discount([total_discount]/[sales_value]),Make sure this is positive (try '.abs()')
If the percentage discount is greater than 1,set it equalto 1, if it is less than 0, set it to 0.
Drop the individualdiscount columns(retail_disc, coupon_disc , coupon_match_disc)
feel free to overwrite the existing transaction dataframe after making the modifications above
'''

#-A column thatcaptures the total_discount by row(sum of [retail_disc]/[coupon_disc])
#--The percentage discount([total_discount]/[sales_value]),Make sure this is positive
#---(try '.abs()')
#---using the .assign() method i will proceede to create two columns satisfying the above
project_transactions=(project_transactions
                      .assign(
                          TOTAL_DISC = lambda x:x['RETAIL_DISC'] + x['COUPON_DISC'],
                          PERC_DISC = lambda x:(x['TOTAL_DISC']/x['SALES_VALUE']).abs().round()
                          ).drop(['RETAIL_DISC','COUPON_DISC','COUPON_MATCH_DISC'],axis=1)
                      )
print(project_transactions.query("PERC_DISC in [1.0]"))
print(project_transactions.info(memory_usage='deep'))


'''
        OVERALL STATISTICS
CALCULATE:
    -THE TOTAL SALES (SUM OF SALES_VALUE)
    -TOTAL DISCOUNT (SUM OF TOTAL_DISCOUNT)
    -OVERALL PERCENTAGE DISCOUNT(SUM OF TOTAL_DISCOUNT/SUM OF SALES VALUE)
    -TOTAL QUANTITY SOLD (SUM OF QUANTITY)
    -MAX QUANTITY SOLD IN A SINGLE ROW . INSPECT THE ROW AS WELL , DOES THIS HAVE A HIGH DISCOUNT
    PERCENTAGE?
    -TOTAL SALES VALUE PER BASKET(SUM OF SALES_VALUE/NUNIQUE BASKET_ID)
    -TOTAL SALES VALUE PER HOUSEHOLD(SUM OF SALES VALUE/NUNIQUE HOUSE HOLD KEY)
'''

TOTAL_SALES = project_transactions['SALES_VALUE'].sum()
TOTAL_DISCOUNT = project_transactions['TOTAL_DISC'].sum()
OVERALL_PERC_DISC = TOTAL_DISCOUNT / TOTAL_SALES
TOTAL_Q = project_transactions['QUANTITY'].sum()

MAX_Q = project_transactions['QUANTITY'].max()

print(project_transactions.query("QUANTITY == @MAX_Q"))
#max value does not have a high percentage discount, its per_disc == 0.0

TOTAL_SALES_PER_BASKET = TOTAL_SALES / project_transactions['BASKET_ID'].nunique()

TOTAL_SALES_PER_HOUSEHOLD = TOTAL_SALES / project_transactions['household_key'].nunique()

print(
      'OVERALL_PERC_DISC =',          OVERALL_PERC_DISC,           '\n',#-0.1768099350106248
      'TOTAL_SALES =',                TOTAL_SALES,                 '\n',#6666243.499999999
      'TOTAL_DISCOUNT =',             TOTAL_DISCOUNT,              '\n',#1178658.0799999998 
      'TOTAL_QUANTITY =',             TOTAL_Q,                     '\n',#216713611 
      'MAX_QUANTITY =',               MAX_Q,                       '\n',#89638 
      'TOTAL_SALES_PER_BASKET =',     TOTAL_SALES_PER_BASKET,      '\n',#28.61797938516092
      'TOTAL_SALES_PER_HOUSEHOLD =',  TOTAL_SALES_PER_HOUSEHOLD         #3175.9140066698424
      )


 '''
        HOUSEHOLD ANALYSIS


'''
# -plot the distribution of total sales value purchased at the household level
sales_dist = (project_transactions
              
              .pivot_table(
                index = 'WEEK_NO',
                columns= 'household_key',
                values = 'SALES_VALUE',
                aggfunc =  sum).head(52)
             
              )

print(sales_dist.plot.hist(legend=False,alpha=0.4).figure.savefig('hist.png',bbox_inches='tight'))
print(sales_dist.tail())

# -what were the top 10 households by quantity purchased?
top_by_q =(
    project_transactions
    .sort_values('QUANTITY',ascending=False)
    .groupby('household_key',as_index=False)[['QUANTITY']]
    .sum()
    .sort_values('QUANTITY',ascending=False)
    )

print(top_by_q.head(10))

# -what were th etop 10 households by sales value?
top_by_SV =(
    project_transactions
    .sort_values('SALES_VALUE',ascending=False)
    .groupby('household_key',as_index=True)[['SALES_VALUE']]
    .sum()
    .sort_values('SALES_VALUE',ascending=False)
    .head(10)
    )
print(top_by_SV)


# -plot the total sales value for our top 10 house holds by value, order from highest to lowest
print(top_by_SV.plot.bar())




'''
                product analysis
-which product had the most sales by value?plot a horizintal bar chart
-did the top 10 seling items have a higher than average discount rate?
-what was the most common [product_id]among rows with the households in our top
    10 households by sales value
-look up the names of the top 10 products by sales in the [product.csv]dataset
-look up the product name of  the item that had the highest quantity sold in a single row
'''
product = pd.read_csv('C:/Users/akinola/Documents/python DATA ANALYTICS files/Pandas Course Resources/project_data/product.csv')


print(project_transactions.info())
product =(product
          .assign( sales_value = project_transactions['SALES_VALUE'],
                  discount_rate = project_transactions['RETAIL_DISC']))
# n0.1
print(product[['COMMODITY_DESC','sales_value']]
      .nlargest(10,'sales_value')
      .sort_values(by='sales_value', ascending=False)
      .set_index('COMMODITY_DESC')
      .plot.barh(y='sales_value', 
                  xlabel = 'commodity',
                  ylabel = 'sales value'))
# no.2
print(product.info())
top_10 = product[['sales_value','discount_rate']].nlargest(10,'sales_value').agg({'discount_rate':"mean",'sales_value':'mean'})
print(top_10,'\n',
      product.describe(),'\n',
      'the top 10 had a below average discount of -7.530 '
      )

# no.3 
print(project_transactions.info())
#most common product id
top_10_house =(project_transactions[['household_key','SALES_VALUE','PRODUCT_ID']].nlargest(10,'SALES_VALUE')
                .agg({'PRODUCT_ID':'mode'}))

print(top_10_house,'\n',"most common product_id is 1089093")

# no.4
print(product.info())
top_10_prod_names =  (product[['COMMODITY_DESC','sales_value']]
                      .nlargest(10,'sales_value')
                      .reset_index())
print(top_10_prod_names)

# no.5

product = product.assign(quantity = project_transactions['QUANTITY'])
top_by_q = product.groupby("COMMODITY_DESC")[['quantity']].agg({'quantity':'sum'})
top_by_qor = product[['COMMODITY_DESC','quantity']].nlargest(1,'quantity')
print(top_by_qor)














