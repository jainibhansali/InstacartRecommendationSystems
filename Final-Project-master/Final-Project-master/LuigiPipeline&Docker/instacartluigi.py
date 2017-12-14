import urllib
import requests
from bs4 import BeautifulSoup
from pandas import DataFrame
import zipfile,io,os
import pandas as pd
import csv
import numpy as np
import luigi
import tarfile
import os,zipfile,io
import tarfile
import boto3
import botocore
import argparse
import sys
import datetime
from luigi.parameter import MissingParameterException



class fetchinstacartdata(luigi.Task):

		
	def run(self):		
		url='https://www.instacart.com/datasets/grocery-shopping-2017'
		r=requests.get(url,headers = {'User-Agent': 'Mozilla/5.0'})
		html_content=r.text
		soup=BeautifulSoup(html_content,'html.parser')
		l=soup.find_all('a')
		downloadlink=None
		for item in l:
			if "dataset" in str(item):
				downloadlink=item['href']

		if not os.path.exists('Instacartdata'):
			os.makedirs('Instacartdata')

		datafile = urllib.request.URLopener()
		datafile.retrieve(downloadlink,os.path.join('Instacartdata',"instacartdata.tar.gz"))

		tar=tarfile.open(os.path.join('Instacartdata',"instacartdata.tar.gz"),'r:gz')
		filelist=tar.getnames()
		tar.extractall(os.path.join('Instacartdata'))

		file=pd.DataFrame(columns=["csvname"])
		for i in filelist:
			s=i.split("/")
			if len(s) > 1:
				if "._" in s[1]:
					continue
				else:
					file=file.append({'csvname':str(s[0]+"/"+s[1])},ignore_index=True)
		tar.close()			
		file.to_csv(self.output().path,index=False)
	def output(self):
		return luigi.LocalTarget('filenames.csv')
		

class readandmerge(luigi.Task):

	def requires(self):
		yield fetchinstacartdata()
	def run(self):
	
		filenames=pd.read_csv(fetchinstacartdata().output().path)
		filelist=list(filenames['csvname'])
		aisles=pd.read_csv(str('Instacartdata'+"/"+filelist[0]))
		departments=pd.read_csv(str('Instacartdata'+"/"+filelist[1]))
		orderprior=pd.read_csv(str('Instacartdata'+"/"+filelist[2]))
		ordertrain=pd.read_csv(str('Instacartdata'+"/"+filelist[3]))
		orders=pd.read_csv(str('Instacartdata'+"/"+filelist[4]))
		products=pd.read_csv(str('Instacartdata'+"/"+filelist[5]))
		aisles['aisle_id']=aisles['aisle_id'].astype('int16')
		orderprior['order_id']=orderprior['order_id'].astype('int32')
		orderprior['product_id']=orderprior['product_id'].astype('int32')
		orderprior['add_to_cart_order']=orderprior['add_to_cart_order'].astype('int16')
		orderprior['reordered']=orderprior['reordered'].astype('int8')
		ordertrain['order_id']=ordertrain['order_id'].astype('int32')
		ordertrain['product_id']=ordertrain['product_id'].astype('int32')
		ordertrain['add_to_cart_order']=ordertrain['add_to_cart_order'].astype('int16')
		ordertrain['reordered']=ordertrain['reordered'].astype('int8')		
		departments['department_id']=departments['department_id'].astype('int8')
		products['product_id']=products['product_id'].astype('int32')
		products['department_id']=products['department_id'].astype('int8')
		products['aisle_id']=products['aisle_id'].astype('int16')
		orders['order_id']=orders['order_id'].astype('int32')
		orders['user_id']=orders['user_id'].astype('int32')
		orders['order_number']=orders['order_number'].astype('int8')
		orders['order_dow']=orders['order_dow'].astype('int8')
		orders['order_hour_of_day']=orders['order_hour_of_day'].astype('int8')
		orders['days_since_prior_order'].fillna(-1,inplace=True)
		orders['days_since_prior_order']=orders['days_since_prior_order'].astype('int8')
		products['product_id']=products['product_id'].astype('int32')
		products['aisle_id']=products['aisle_id'].astype('int16')
		products['department_id']=products['department_id'].astype('int8')
		#merging orderprior ordertrain and orders for making some basic recommendation systems
		frames=[orderprior,ordertrain]
		mergedorderprod=pd.concat(frames)
		mergeforprodanduser=orders.merge(mergedorderprod,how='inner',on='order_id')
		mergeforproduserdeptaisle=mergeforprodanduser.merge(products,how='inner',on='product_id')
		mergeforproduserdeptaisle.to_csv(self.output().path,index=False)
	def output(self):
		return luigi.LocalTarget('instacartdata.csv')


class userbasedheuristic(luigi.Task):
	def requires(self):
		yield readandmerge()
	def run(self):
		mergeforprodanduser=pd.read_csv(readandmerge().output().path,encoding="ISO-8859-1")
		userandprod=mergeforprodanduser[['product_id','user_id']].copy()
		recommend=pd.DataFrame(userandprod['product_id'].groupby(userandprod['user_id']).value_counts())
		recommend['userprod']=recommend.index
		recommend.columns=['count','userprod']
		recommend.reset_index(inplace=True)
		recommend.drop('userprod',axis=1,inplace=True)
		recommend['user_id']=recommend['user_id'].astype('int32')
		recommend['product_id']=recommend['product_id'].astype('int32')
		recommend['count']=recommend['count'].astype('int32')
		mxboughtbyuser=pd.DataFrame(recommend.groupby(recommend['user_id']).head())
		prod=pd.read_csv('Instacartdata/instacart_2017_05_01/products.csv')
		mxboughtbyuser=mxboughtbyuser.merge(prod,how='inner',on='product_id')
		mxboughtbyuser.to_csv(self.output().path,index=False)
	def output(self):
		return luigi.LocalTarget('topuserbought.csv')

class producthour(luigi.Task):
	def requires(self):
		yield readandmerge()
	def run(self):
		mergeforprodanduser=pd.read_csv(readandmerge().output().path,encoding="ISO-8859-1")
		hourandprod=mergeforprodanduser[['order_hour_of_day','product_id']].copy()
		recommendhour=pd.DataFrame(hourandprod['product_id'].groupby(hourandprod['order_hour_of_day']).value_counts())
		recommendhour['hourprod']=recommendhour.index
		recommendhour.columns=['count','hourprod']
		recommendhour.reset_index(inplace=True)
		recommendhour.drop('hourprod',axis=1,inplace=True)
		ph=recommendhour.copy()
		ph['order_hour_of_day']=ph['order_hour_of_day'].astype('int32')
		ph['product_id']=ph['product_id'].astype('int32')
		ph['count']=ph['count'].astype('int32')
		maximumboughtprohour=pd.DataFrame(ph[['count','product_id']].groupby(ph['order_hour_of_day']).max(),columns=['count','product_id'])
		maximumboughtprohour.reset_index(inplace=True)
		prod=pd.read_csv('Instacartdata/instacart_2017_05_01/products.csv')
		maximumboughtprohour=maximumboughtprohour.merge(prod,how='inner',on='product_id')
		maximumboughtprohour.to_csv(self.output().path,index=False)
	def output(self):
		return luigi.LocalTarget('topproducthour.csv')
		
class topproductfordepartment(luigi.Task):
	def requires(self):
		yield readandmerge()
	def run(self):
		mergeforprodanduser=pd.read_csv(readandmerge().output().path,encoding="ISO-8859-1")
		products=pd.read_csv('Instacartdata/instacart_2017_05_01/products.csv')
		prodfordept=products[['department_id','product_id','product_name']].copy()
		recommendproddep=mergeforprodanduser.merge(prodfordept,how='inner',on='product_id')
		recommendproddep=recommendproddep[['department_id','product_id']]
		recommendproddept=pd.DataFrame(recommendproddep['product_id'].groupby(recommendproddep['department_id']).value_counts())
		recommendproddept['deptprod']=recommendproddept.index
		recommendproddept.columns=['count','deptprod']
		recommendproddept.reset_index(inplace=True)
		recommendproddept.drop('deptprod',axis=1,inplace=True)
		dp=recommendproddept.copy()
		dp['department_id']=dp['department_id'].astype('int32')
		dp['product_id']=dp['product_id'].astype('int32')
		dp['count']=dp['count'].astype('int32')
		maxprodperdept=pd.DataFrame(dp[['product_id','department_id']].groupby(dp['department_id']).head(4))
		prod=pd.read_csv('Instacartdata/instacart_2017_05_01/products.csv')
		prod=prod[['product_id','product_name']]
		maxprodperdept=maxprodperdept.merge(prod,how='inner',on='product_id')
		dept=pd.read_csv('Instacartdata/instacart_2017_05_01/departments.csv')
		maxprodperdept=maxprodperdept.merge(dept,how='inner',on='department_id')
		maxprodperdept.to_csv(self.output().path,index=False)
	def output(self):
		return luigi.LocalTarget('topproductfordepartment.csv')
	
	

class mostboughproduct(luigi.Task):
	def requires(self):
		yield readandmerge()
	def run(self):
		mergeforprodanduser=pd.read_csv(readandmerge().output().path,encoding="ISO-8859-1")
		mostbought=pd.DataFrame(mergeforprodanduser['product_id'].value_counts().head(5))
		mostbought.rename(columns={'product_id':'count'},inplace=True)
		mostbought.reset_index(inplace=True)
		mostbought.rename(columns={'index':'product_id'},inplace=True)
		mostbought=mostbought.merge(products,how='inner',on='product_id')
		mostbought.to_csv(self.output().path,index=False)
	def output(self):
		return luigi.LocalTarget('mostboughtproduct.csv')

class mostboughtitemforday(luigi.Task):
	def requires(self):
		yield readandmerge()
	def run(self):
		mergeforprodanduser=pd.read_csv(readandmerge().output().path,encoding="ISO-8859-1")
		recommenddow=pd.DataFrame(mergeforprodanduser['product_id'].groupby(mergeforprodanduser['order_dow']).value_counts())
		recommenddow.rename(columns={'product_id':'count'},inplace=True)
		recommenddow.reset_index(inplace=True)
		recommenddow=recommenddow.merge(products,how='inner',on='product_id')
		rdow=recommenddow.copy()
		rdow['order_dow']=rdow['order_dow'].astype('int32')
		rdow['count']=rdow['count'].astype('int32')
		rdow['product_id']=rdow['product_id'].astype('int32')
		maxproddow=pd.DataFrame(rdow[['product_id','order_dow','product_name']].groupby(rdow['order_dow']).head(4))
		maxproddow.to_csv(self.output().path,index=False)
	def output(self):
		return luigi.LocalTarget('mostboughtitemforday.csv')

class famousdepartment(luigi.Task):
	def requires(self):
		yield readandmerge()
	def run(self):
		products=pd.read_csv('Instacartdata/instacart_2017_05_01/products.csv')
		mergeforprodanduser=pd.read_csv(readandmerge().output().path,encoding="ISO-8859-1")
		mergeprodwithall=mergeforprodanduser.merge(products,how='inner',on='product_id')
		maxdept=pd.DataFrame(mergeprodwithall['department_id'].value_counts().head())
		maxdept.rename(columns={'department_id':'count'},inplace=True)
		maxdept.reset_index(inplace=True)
		maxdept.rename(columns={'index':'department_id'},inplace=True)
		dept=pd.read_csv('departments.csv')
		maxdept=maxdept.merge(dept,how='inner',on='department_id')
		maxdept.to_csv(self.output().path,index=False)
	def output(self):
		return luigi.LocalTarget('famousdepartment.csv')

class topsellersforproductfordayhour(luigi.Task):
	def requires(self):
		yield readandmerge()
	def run(self):
		mergeforprodanduser=pd.read_csv(readandmerge().output().path,encoding="ISO-8859-1")
		prodhourdow=mergeforprodanduser[['product_id','order_dow','order_hour_of_day']].copy()
		p=pd.DataFrame(prodhourdow.groupby(['order_dow','order_hour_of_day'])['product_id'].value_counts())
		p.rename(columns={'product_id':'count'},inplace=True)
		p.reset_index(inplace=True)
		findowhourprod=pd.DataFrame(p.groupby(['order_dow','order_hour_of_day']).head(3))
		findowhourprod=findowhourprod.merge(products,how='inner',on='product_id')
		findowhourprod.to_csv(self.output().path,index=False)
	def output(self):
		return luigi.LocalTarget('dayhourtop.csv')

class createzip(luigi.Task):
	def requires(self):
		yield readandmerge()
		yield topsellersforproductfordayhour()
		yield famousdepartment()
		yield mostboughtitemforday()
		yield mostboughproduct()
		yield userbasedheuristic()
		yield producthour()
		yield topproductfordepartment()
	def run(self):
		
		zipf=zipfile.ZipFile(self.output().path,'w',zipfile.ZIP_DEFLATED)
		zipf.write(readandmerge().output().path)
		zipf.write(topsellersforproductfordayhour().output().path)
		zipf.write(famousdepartment().output().path)
		zipf.write(mostboughtitemforday().output().path)
		zipf.write(mostboughproduct().output().path)
		zipf.write(userbasedheuristic().output().path)
		zipf.write(producthour().output().path)
		zipf.write(topproductfordepartment().output().path)
		zipf.close()
	def output(self):
		return luigi.LocalTarget('Instacartdata.zip')
		
class uploadziptos3(luigi.Task):
	akey=luigi.Parameter()
	skey=luigi.Parameter()
	def requires(self):
		yield createzip()
	def run(self):
		if str(self.akey) == "1" or str(self.skey) == "1":
			print("please enter both access key and secret access key and rerun the program ")
			sys.exit()
		
		now=datetime.datetime.now()
		fin2=now1.replace(":","")
		fin3=fin2.replace("-","")
		fin=fin3.replace(" ","")
		s3 = boto3.resource('s3')
		buckname="finalprojectinstacartdata"+str(fin)
		client = boto3.client('s3','us-west-2',aws_access_key_id=self.akey,aws_secret_access_key=self.skey)
		client.create_bucket(Bucket=buckname,CreateBucketConfiguration={'LocationConstraint':'us-west-2'})
		client.upload_file("Instacartdata.zip", buckname, "Instacartdata.zip")
		

	
		
if __name__=='__main__':
	try:
		luigi.run()
	except MissingParameterException:
		print("Please provide Access Keys and Secret Access Keys")
		sys.exit()