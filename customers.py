import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt

def customer_counts(df, prev_year, curr_year):
	df_prev = df[df['year'] == prev_year]
	df_curr = df[df['year'] == curr_year]

	frames = [df_prev, df_curr]
	result = pd.concat(frames)

	#duplicates are the same customers for both years
	#by removing them, we keep only the new ones
	result = result.drop_duplicates(subset=['customer_email'], keep=False)
	df_curr_new = result[result['year'] == curr_year]
	#the customers of the previous year that are not in the current one (not duplicates), are the lost ones
	df_prev_lost = result[result['year'] == prev_year]

	new_rev = df_curr_new['net_revenue'].sum() 
	new_customers = df_curr_new['customer_email']
	lost_customers = df_prev_lost['customer_email']

	return (new_rev, new_customers, lost_customers)

def existing_customer_revenue(df, prev_year, curr_year):
	index_curr_year = df.loc[df['year'] == curr_year]
	index_prev_year = df.loc[df['year'] == prev_year]

	return (index_curr_year['net_revenue'].values[0] - index_prev_year['net_revenue'].values[0])

def main():
	#load csv file
	df = pd.read_csv('casestudy.csv')

	#1: Total revenue for current year (Same for #5 & 6: Existing Customer Revenue?)
	df_years = df.groupby(["year"]).net_revenue.sum().reset_index()
	print ('Total revenue for each year:')
	print(df_years)
	df_years.plot(x='year', y='net_revenue', kind='bar')
	plt.title('Total Revenue')	
	plt.show()

	#7 & 8: Total Customers Each Year
	df_cust = df.groupby(["year"]).net_revenue.count().reset_index()
	print ('\nTotal customers for each year:')
	print(df_cust)
	df_cust.plot(x='year', y='net_revenue', kind='bar')
	plt.title('Total Customers')	
	plt.show()

	df_tmp = df_years.iloc[:-1 , :]
	nc, lc, yr = [],[],[]
	for ind in df_tmp.index:
		prev_year = df_years['year'][ind]
		curr_year = df_years['year'][ind+1]

		#2 & 9: New Customers & New Customers Revenue
		new_rev, new_customers, lost_customers = customer_counts(df, prev_year, curr_year)
		print ('\nNew customer revenue for ', curr_year, ': ',new_rev)
		print ('\nNew customers for ', curr_year, ':')
		print (new_customers)
		nc.append(new_customers.size)
		print ('\nLost customers for ', curr_year, ':')
		print (lost_customers)
		lc.append(lost_customers.size)
		yr.append(curr_year)

		#3: Existing Customer Growth
		existing = existing_customer_revenue(df_years, prev_year, curr_year)
		print ('\nExisting customer growth for ', curr_year, ':', existing)

		#4: Revenue lost from attrition
		# (revenue previous year - revenue current year) / revenue previous year
		rev_attr = (df_years['net_revenue'][ind] - df_years['net_revenue'][ind+1]) / df_years['net_revenue'][ind]
		print ('\nRevenue attrition rate for ', curr_year, ': ',rev_attr)

	plt.plot(yr, nc, label='new_customers')
	plt.plot(yr, lc, label='lost_customers')
	plt.legend()
	plt.title('New vs Lost Customers')
	plt.show()

if __name__ == '__main__':
	main()