'''
    COLUMNS TO WORK WITH:
    PROJECT_TANSACTIONS.CSV AND PRODUCT.CSV(BRIEFLY)
'''

import pandas as pd
import seaborn as sns
sns.set_style('darkgrid')


#____________________________________________reading in neccessary data___________________________________________________________
project_transactions= pd.read_csv('C:/Users/akinola/Documents/python DATA ANALYTICS files/Pandas Course Resources/project_data/project_transactions.csv',
                                  )
                      
                      
#sections to check the dtype and downcast accordingly to reduce memory usage
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

#checking for missing data
print(project_transactions.isna().sum())
#there appears to be no missing data

#Checking for unique household and product values
print(project_transactions[['household_key','PRODUCT_ID']].nunique())
#   THE NUMBER OF UNIQUE HOUSEHOLDS AND PRODUCTS ARE:
#household_key     2099
#PRODUCT_ID       84138

#_____________________________________________________________________________________________________________________

                      

#______________________________________________COLUMN CREATION___________________________________________________________
project_transactions=(project_transactions
                      .assign(
                          TOTAL_DISC = lambda x:x['RETAIL_DISC'] + x['COUPON_DISC'],
                          PERC_DISC = lambda x:(x['TOTAL_DISC']/x['SALES_VALUE']).abs().round()
                          ).drop(['RETAIL_DISC','COUPON_DISC','COUPON_MATCH_DISC'],axis=1)
                      )
print(project_transactions.query("PERC_DISC in [1.0]"))
print(project_transactions.info(memory_usage='deep'))
#_________________________________________________________________________________________________________________________


#____________________________________________OVERALL STATISTICS______________________________________________________

#THE TOTAL SALES (SUM OF SALES_VALUE)
TOTAL_SALES = project_transactions['SALES_VALUE'].sum()

#TOTAL DISCOUNT (SUM OF TOTAL_DISCOUNT)
TOTAL_DISCOUNT = project_transactions['TOTAL_DISC'].sum()

#OVERALL PERCENTAGE DISCOUNT(SUM OF TOTAL_DISCOUNT/SUM OF SALES VALUE)
OVERALL_PERC_DISC = TOTAL_DISCOUNT / TOTAL_SALES

#TOTAL QUANTITY SOLD (SUM OF QUANTITY)
TOTAL_Q = project_transactions['QUANTITY'].sum()

#MAX QUANTITY SOLD IN A SINGLE ROW
MAX_Q = project_transactions['QUANTITY'].max()

#checking for A HIGH DISCOUNT PERCENTAGE
print(project_transactions.query("QUANTITY == @MAX_Q"))
#max value does not have a high percentage discount, its per_disc == 0.0

#TOTAL SALES VALUE PER BASKET(SUM OF SALES_VALUE/NUNIQUE BASKET_ID)
TOTAL_SALES_PER_BASKET = TOTAL_SALES / project_transactions['BASKET_ID'].nunique()

#TOTAL SALES VALUE PER HOUSEHOLD(SUM OF SALES VALUE/NUNIQUE HOUSE HOLD KEY)
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
#__________________________________________________________________________________________________________________


 #________________________________________________________HOUSEHOLD ANALYSIS________________________________________________

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
#_______________________________________________________________________________________________________________________



#____________________________________________product analysis___________________________________________________________________

product = pd.read_csv('C:/Users/akinola/Documents/python DATA ANALYTICS files/Pandas Course Resources/project_data/product.csv')

print(project_transactions.info())
product =(product
          .assign( sales_value = project_transactions['SALES_VALUE'],
                  discount_rate = project_transactions['RETAIL_DISC']))
                  
# which product had the most sales by value?plot a horizintal bar chart
print(product[['COMMODITY_DESC','sales_value']]
      .nlargest(10,'sales_value')
      .sort_values(by='sales_value', ascending=False)
      .set_index('COMMODITY_DESC')
      .plot.barh(y='sales_value', 
                  xlabel = 'commodity',
                  ylabel = 'sales value'))
# did the top 10 seling items have a higher than average discount rate?
print(product.info())
top_10 = product[['sales_value','discount_rate']].nlargest(10,'sales_value').agg({'discount_rate':"mean",'sales_value':'mean'})
print(top_10,'\n',
      product.describe(),'\n',
      'the top 10 had a below average discount of -7.530 '
      )

# what was the most common [product_id]among rows with the households in our top 10 households by sales value
print(project_transactions.info())
#most common product id
top_10_house =(project_transactions[['household_key','SALES_VALUE','PRODUCT_ID']].nlargest(10,'SALES_VALUE')
                .agg({'PRODUCT_ID':'mode'}))

print(top_10_house,'\n',"most common product_id is 1089093")

# look up the names of the top 10 products by sales in the [product.csv]dataset
print(product.info())
top_10_prod_names =  (product[['COMMODITY_DESC','sales_value']]
                      .nlargest(10,'sales_value')
                      .reset_index())
print(top_10_prod_names)

# look up the product name of  the item that had the highest quantity sold in a single row
product = product.assign(quantity = project_transactions['QUANTITY'])
top_by_q = product.groupby("COMMODITY_DESC")[['quantity']].agg({'quantity':'sum'})
top_by_qor = product[['COMMODITY_DESC','quantity']].nlargest(1,'quantity')
print(top_by_qor)
#______________________________________________________________________________________________________________












