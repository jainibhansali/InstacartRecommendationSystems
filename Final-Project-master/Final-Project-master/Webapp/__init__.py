from flask import Flask,render_template, session, request,redirect,url_for,jsonify
from functools import wraps
import pandas as pd
from logger import logger
import datetime
import urllib2
import json
import random


app = Flask(__name__)


def login_required(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if'logged_in' in session: 
			if session['logged_in']:
				return f(*args,**kwargs)
		else:
			return redirect (url_for('homepage'))
	return wrap


	
	
def getrecommendationsaslist(rec):
	items=rec['Results']['output1'][0].keys()
	recommended=[]
	prod=pd.read_csv('static/products.csv')
	for i in items:
		id=rec['Results']['output1'][0][i]
		if i=='User':
			continue
		name=prod.loc[prod.product_id==int(id),'product_name'].iloc[0]
		
		recommended.append(name.decode('utf-8'))
	return recommended
	
	
	
	
	
def getitems(url,api_key,userid):
	headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}
	data = {"Inputs": {"input1":[{'user_id':userid,}],},"GlobalParameters":  {}}
	body = str.encode(json.dumps(data))

	req = urllib2.Request(url, body, headers)

	try:
		response = urllib2.urlopen(req)

		result = response.read()
		return(result)
	except urllib2.HTTPError, error:
		return("error")
	


	
@app.route('/',methods=['GET','POST'])
def homepage(user=None,regerror=None):	
	day=datetime.date.today().weekday()
	time=datetime.datetime.now().hour
	mostbought=pd.read_csv('static/mostboughtproduct.csv')
	topprods=mostbought['product_name'].tolist()
	
	
	api_key="7LBsHEGMh3tWhJoUYvFxkyJuI9fU6vUlfWBeCvNe6OiVlHLtau3ba3HZ20YAih5ZBiyeYiwa7dhpsZsw6EniMQ=="	
	url='https://ussouthcentral.services.azureml.net/workspaces/708fc30f05a343069bc21c29cd66dadf/services/d606bcd2fcd741019c40ed77ee63bc1d/execute?api-version=2.0&format=swagger'
	if user:
		restock=pd.read_csv('static/topuserbought.csv')
		restock=(restock[restock.user_id==int(user)]['product_name']).tolist()
		recommendations=json.loads(getitems(url,api_key,user))
		modelrec=getrecommendationsaslist(recommendations)	
		return render_template("home.html",user=user,topprods=topprods,restock=restock,modelrec=modelrec)

	else:
		recommendations=json.loads(getitems(url,api_key,'250000'))
		newusermodelrec=getrecommendationsaslist(recommendations)
		return render_template("home.html",user=user,topprods=topprods,newusermodelrec=newusermodelrec)


@app.route('/itempage/<itemname>',methods=['GET'])
def itempage(itemname=None):
	prod=pd.read_csv('static/products.csv')
	if prod[prod.product_name==itemname].empty:
		return render_template('price.html',itemname=itemname,associates=None)
	depid=prod.loc[prod.product_name==itemname,'department_id'].iloc[0]
	asscoiationfinder=pd.DataFrame()
	associates=[]
	if depid==1:
		associtaionfinder=pd.read_csv('static/Frozen.csv')
		if associtaionfinder[associtaionfinder.antecedants==itemname].empty:
			associates=None
		else:
			associates=(associtaionfinder[associtaionfinder.antecedants==itemname]['consequents']).tolist()
		
	elif depid==2:
		associtaionfinder=pd.read_csv('static/other.csv')
		if associtaionfinder[associtaionfinder.antecedants==itemname].empty:
			associates=None
		else:
			associates=(associtaionfinder[associtaionfinder.antecedants==itemname]['consequents']).tolist()
		
	elif depid==3:
		associtaionfinder=pd.read_csv('static/Bakery.csv')
		if associtaionfinder[associtaionfinder.antecedants==itemname].empty:
			associates=None
		else:
			associates=(associtaionfinder[associtaionfinder.antecedants==itemname]['consequents']).tolist()
		
	elif depid==4:
		associtaionfinder=pd.read_csv('static/Produce.csv')
		if associtaionfinder[associtaionfinder.antecedants==itemname].empty:
			associates=None
		else:
			associates=(associtaionfinder[associtaionfinder.antecedants==itemname]['consequents']).tolist()
		
	elif depid==5:
		associtaionfinder=pd.read_csv('static/alchohol.csv')
		if associtaionfinder[associtaionfinder.antecedants==itemname].empty:
			associates=None
		else:
			associates=(associtaionfinder[associtaionfinder.antecedants==itemname]['consequents']).tolist()
		
	elif depid==6:
		associtaionfinder=pd.read_csv('static/international.csv')
		if associtaionfinder[associtaionfinder.antecedants==itemname].empty:
			associates=None
		else:
			associates=(associtaionfinder[associtaionfinder.antecedants==itemname]['consequents']).tolist()
		
	elif depid==7:
		associtaionfinder=pd.read_csv('static/Beverages.csv')
		if associtaionfinder[associtaionfinder.antecedants==itemname].empty:
			associates=None
		else:
			associates=(associtaionfinder[associtaionfinder.antecedants==itemname]['consequents']).tolist()
		
	elif depid==8:
		associtaionfinder=pd.read_csv('static/pets.csv')
		if associtaionfinder[associtaionfinder.antecedants==itemname].empty:
			associates=None
		else:
			associates=(associtaionfinder[associtaionfinder.antecedants==itemname]['consequents']).tolist()
		
	elif depid==9:
		associtaionfinder=pd.read_csv('static/drygoodspasta.csv')
		if associtaionfinder[associtaionfinder.antecedants==itemname].empty:
			associates=None
		else:
			associates=(associtaionfinder[associtaionfinder.antecedants==itemname]['consequents']).tolist()
		
	elif depid==10:
		associtaionfinder=pd.read_csv('static/bulk.csv')
		if associtaionfinder[associtaionfinder.antecedants==itemname].empty:
			associates=None
		else:
			associates=(associtaionfinder[associtaionfinder.antecedants==itemname]['consequents']).tolist()
		
	elif depid==11:
		associtaionfinder=pd.read_csv('static/PersonalCare.csv')
		if associtaionfinder[associtaionfinder.antecedants==itemname].empty:
			associates=None
		else:
			associates=(associtaionfinder[associtaionfinder.antecedants==itemname]['consequents']).tolist()
		
	elif depid==12:
		associtaionfinder=pd.read_csv('static/MeatSeafood.csv')
		if associtaionfinder[associtaionfinder.antecedants==itemname].empty:
			associates=None
		else:
			associates=(associtaionfinder[associtaionfinder.antecedants==itemname]['consequents']).tolist()
		
	elif depid==13:
		associtaionfinder=pd.read_csv('static/Pantry.csv')
		return render_template('price.html',itemname=itemname,associates=None)
		
	elif depid==14:
		associtaionfinder=pd.read_csv('static/Breakfast.csv')
		if associtaionfinder[associtaionfinder.antecedants==itemname].empty:
			associates=None
		else:
			associates=(associtaionfinder[associtaionfinder.antecedants==itemname]['consequents']).tolist()
		
	elif depid==15:
		associtaionfinder=pd.read_csv('static/cannedgoods.csv')
		if associtaionfinder[associtaionfinder.antecedants==itemname].empty:
			associates=None
		else:
			associates=(associtaionfinder[associtaionfinder.antecedants==itemname]['consequents']).tolist()
		
	elif depid==16:
		associtaionfinder=pd.read_csv('static/DairyEggs.csv')
		if associtaionfinder[associtaionfinder.antecedants==itemname].empty:
			associates=None
		else:
			associates=(associtaionfinder[associtaionfinder.antecedants==itemname]['consequents']).tolist()
		
	elif depid==17:
		associtaionfinder=pd.read_csv('static/household.csv')
		if associtaionfinder[associtaionfinder.antecedants==itemname].empty:
			associates=None
		else:
			associates=(associtaionfinder[associtaionfinder.antecedants==itemname]['consequents']).tolist()
		
	elif depid==18:
		associtaionfinder=pd.read_csv('static/babies.csv')
		if associtaionfinder[associtaionfinder.antecedants==itemname].empty:
			associates=None
		else:
			associates=(associtaionfinder[associtaionfinder.antecedants==itemname]['consequents']).tolist()
		
	elif depid==19:
		return render_template('price.html',itemname=itemname,associates=None)
		
	elif depid==20:
		associtaionfinder=pd.read_csv('static/Deli.csv')
		if associtaionfinder[associtaionfinder.antecedants==itemname].empty:
			associates=None
		else:
			associates=(associtaionfinder[associtaionfinder.antecedants==itemname]['consequents']).tolist()
		
	elif depid==21:
		associtaionfinder=pd.read_csv('static/missing.csv')
		if associtaionfinder[associtaionfinder.antecedants==itemname].empty:
			associates=None
		else:
			associates=(associtaionfinder[associtaionfinder.antecedants==itemname]['consequents']).tolist()
	topsellerdf=pd.read_csv('static/recommendationperdepartmen.csv')
	topseller=(topsellerdf[topsellerdf['department_id']== depid]['product_name']).tolist()
		
	
	if not associates:
		return render_template('price.html',itemname=itemname,associates=None,topseller=topseller)
	else:
		return render_template('price.html',itemname=itemname,associates=associates)


	

	
@app.route('/eda',methods=['GET'])
def eda():
	return render_template('eda.html')

	
@app.route('/company',methods=['GET'])
@app.route('/company',methods=['GET'])
def company():
	return render_template('company.html')

	
@app.route('/products',methods=['GET'])
def products():

	prod=pd.read_csv('static/products.csv')
	prodstoshow=[]
	count=0
	for index,row in prod.iterrows():
		if count == 50:
			break
		prodstoshow.append(row['product_name'].decode('utf-8'))
		count +=1
	return render_template('product.html',names=prodstoshow)

	
@app.route('/login',methods=['GET'])
def loginpage(loginerror=None):
	return render_template('loginform.html',loginerror=loginerror)


	
@app.route('/login',methods=['POST'])
def login(user=None):
	if ((request.form['username'] == 'admin') & (request.form['password'] == "tushar")):
		session['logged_in']=True
		session['username']=request.form['username']
		session['isadmin']=True
		return render_template('admin.html')
	else:
		userlist=pd.read_csv('static/userlist.csv')
		userlist['userid']=userlist['userid'].astype('str')
		username=str(request.form['username'])
		check=userlist[userlist['userid']==username]
		if check['userid'].empty:
			return loginpage(loginerror="Wrong Credentials")
		else:
			username = request.form['username']
			session['logged_in']=True
			session['username']=username
			session['isadmin']=False
			return homepage(user=username)


			
			
@app.route('/department/<name>',methods=['GET'])
def department(name=None):
	user=None
	if 'logged_in' in session:
		if session['logged_in']:
			user=session['username']
	else:	
		user=250000
	dept=pd.read_csv('static/departments.csv')
	id=dept.loc[dept['department']==name,'department_id'].iloc[0]
	url=None
	api_key=None
	if id ==1:
		api_key="UfAiP3dtJcMrpclbLeINZ78+Ls4DFGd7OK8h/VVMyv9qeewC9Owb42hoqf6ivfclUchCg/mtKTPbLeLV+hKtvg=="
		url='https://ussouthcentral.services.azureml.net/workspaces/567e2fd383474b1ea65f5da77b3ddc17/services/1927a353d366443a8d98b3aaeae4cf39/execute?api-version=2.0&format=swagger'
		
	elif id == 2:
		api_key="AsOdFXW+oUEmzk0p04bk1whWsKc7L2D0cm0LbEUzepxADf4FatYOrKWciOuqNsk6jdbaJPB5KXTnNpoVj7Cvlg=="
		url='https://ussouthcentral.services.azureml.net/workspaces/567e2fd383474b1ea65f5da77b3ddc17/services/7b950437bb844234b83b398c2472f125/execute?api-version=2.0&format=swagger'
		
	elif id == 3:
		api_key="4VdP49bGACDeMKJpXYSTTMfGP4z29YlsaWqjX2VhY55t2kKqoGloXeJfoSMghgDc1S/ZkqG1PJBctPqgHzQlvg=="
		url='https://ussouthcentral.services.azureml.net/workspaces/567e2fd383474b1ea65f5da77b3ddc17/services/7e57268bb6644bc0b8420424542d1543/execute?api-version=2.0&format=swagger'
	
	
	elif id == 4:
		url = 'https://ussouthcentral.services.azureml.net/workspaces/708fc30f05a343069bc21c29cd66dadf/services/125df5e1dfd14fe3affb71e6ac6756a4/execute?api-version=2.0&format=swagger'
		api_key = 'wP5Nc1cKiMa+/voqUbhp5gxhMfBe/AmC/6U90YJVo27obgiwWoYKrIr6Pp6cbgVlt14oUrtq0sma1NBfxiqytw==' 
		
	elif id == 5:
		api_key="6uD950nNAcGHQJlJLJ8qPC0Fmn1T7eCdC//R4KXB10dxvrqZ+xwOMezG1eg2DMJAWmDoHbV6EvgiKCOpcojOdg=="
		url='https://ussouthcentral.services.azureml.net/workspaces/567e2fd383474b1ea65f5da77b3ddc17/services/bebef894118845bc95535a800c617b63/execute?api-version=2.0&format=swagger'
		
	elif id == 6:
		api_key="32mNyo7lUt/YzgcAZA4X5dKGAPoSf3SwHAMoMgYQNOiUhIcbs0+qczfYfeNP29FaziqtlYlizmV42mZ6FItOlg=="
		url='https://ussouthcentral.services.azureml.net/workspaces/567e2fd383474b1ea65f5da77b3ddc17/services/1d5f679bc5be4c3a9da6564a707905aa/execute?api-version=2.0&format=swagger'
	
	elif id == 7:
		api_key="ak0JoPVTQjtj8jOLZFdYGys26Gf3WkBsQpTndXF0lUgncm5DtRjk6Qzy18P4LQ7SyNTM7Ha4YUtXQRgshgWsUg=="
		url='https://ussouthcentral.services.azureml.net/workspaces/d904bbdcfe384a06a037b26cf8651f38/services/ff18d53972994a0689afc2ab26b8a620/execute?api-version=2.0&format=swagger'
	
	elif id == 8:
		api_key="z+PEel+TS7PJYARDVIJFn5w7YC194O/VD2fiq54P2lxgaL2J2iZt2bevSxfaYWA6DjBWxSnX+BSbXCIESuxHQA=="
		url= 'https://ussouthcentral.services.azureml.net/workspaces/567e2fd383474b1ea65f5da77b3ddc17/services/7d9ab8c28cf44749a4d741cd00b08316/execute?api-version=2.0&format=swagger'
	
	elif id == 9:
		api_key="O3ZWkqz8rty55Hx2XyGxF54tGz5ghzoH//Nvg4bxDbJ/ZInJMw840gJPjWpw9utc/F7RZCLq7u+wzpFJkbjFbw=="
		url='https://ussouthcentral.services.azureml.net/workspaces/d904bbdcfe384a06a037b26cf8651f38/services/4cd109819f75423f832e08c20865a994/execute?api-version=2.0&format=swagger'
	
	elif id == 10:
		api_key="AsOdFXW+oUEmzk0p04bk1whWsKc7L2D0cm0LbEUzepxADf4FatYOrKWciOuqNsk6jdbaJPB5KXTnNpoVj7Cvlg=="
		url='https://ussouthcentral.services.azureml.net/workspaces/567e2fd383474b1ea65f5da77b3ddc17/services/7b950437bb844234b83b398c2472f125/execute?api-version=2.0&format=swagger'
		
	elif id == 11:
		api_key="HcEndW0uOSxBd1ejNw7jjyz7IQj+Qm4azZV1G6xECu4adxqAm+yuiN7Wlk3Q2mKcTX3UOYCwYppAJuQnhfgQDQ=="
		url='https://ussouthcentral.services.azureml.net/workspaces/567e2fd383474b1ea65f5da77b3ddc17/services/bdf64a0d965e431c9ff0143c3069b41e/execute?api-version=2.0&format=swagger'
	
	elif id == 12:
		api_key="3cmEXp9Qnps/UfKT6onzSGPDHuWNBUIc0X2uYc0yQqOw7KUhY4jaik9i03WzIO76O+HrrqpGA/ENBCX2ddPzyA=="
		url='https://ussouthcentral.services.azureml.net/workspaces/567e2fd383474b1ea65f5da77b3ddc17/services/63ad912ea5e241bab3c701bc7957cef0/execute?api-version=2.0&format=swagger'
	
	elif id == 13:
		api_key="XB6oUXxOJcuF3NjUDWlWE9pl7V5KWxCOyvcdIS5HsyN0RyRg98g7FkfHOWSdP6SYpfmPQRcsTqf9BV7z2uYoPg=="
		url='https://ussouthcentral.services.azureml.net/workspaces/d904bbdcfe384a06a037b26cf8651f38/services/db2f42b580e14bc1b473795916a8612c/execute?api-version=2.0&format=swagger'
	
	elif id == 14:
		api_key="aEVWPtWRp21lANXirP4nPBaCbL1jngbMiOejUUDW4TWBrPgqWn/JasIqRl3IhVOxpRr7m/Zk050d+a4aj3/67A=="
		url='https://ussouthcentral.services.azureml.net/workspaces/567e2fd383474b1ea65f5da77b3ddc17/services/cc8291fe46b1461ab42fb87566cf0165/execute?api-version=2.0&format=swagger'
	
	elif id == 15:
		api_key="CeCH8JeHtOWjFO6ySykeqZeSUM/fQz8y9jNrjlf+1dFmDFFsXmM9F3NVeH7cqJRqeYJVpUxxYAl0H6WYZbwn+g=="
		url='https://ussouthcentral.services.azureml.net/workspaces/d904bbdcfe384a06a037b26cf8651f38/services/d42c1018d2b54590b49cb58ad22b55fd/execute?api-version=2.0&format=swagger'
	
	elif id == 16:
		api_key="AvyoanlF4qRT2cRAraomp0XyBNhstH5/G2/qPBecIkNUX38NQQQDmuU4sS0Ltl5Ra1YCmVhgUQ/da3cVlQVv3w=="
		url='https://ussouthcentral.services.azureml.net/workspaces/d904bbdcfe384a06a037b26cf8651f38/services/e5697e506a96497691c61ac97318cc58/execute?api-version=2.0&format=swagger'
	
	elif id == 17:
		api_key="wlc0YDUPQLDl8Na/nA8Bgvfvtqjc7zASGH0ZAbmRjVJTPH54eXGlvF6dzU8hVPxvfZsiGpGSy6o3OzTUuaZQlw=="
		url='https://ussouthcentral.services.azureml.net/workspaces/d904bbdcfe384a06a037b26cf8651f38/services/c2d07c4031914dc39d4dec5c967c3aff/execute?api-version=2.0&format=swagger'
	
	elif id == 18:
		api_key = "GCzAafypnJuAjRoR5ZPnb77SbNBikB4kHBsrrpLz74E8Lrb77EvrDUu0L0Y1ET1f57QIUTBF8Hfz0uZ+prrZTA=="
		url='https://ussouthcentral.services.azureml.net/workspaces/567e2fd383474b1ea65f5da77b3ddc17/services/41677f725ae54278a0dfee02088006b4/execute?api-version=2.0&format=swagger'
	
	elif id == 19:
		api_key="Lq/94AOq2/vI0EZWfj+s9Th1/HcgPEROF4hbdl40CBwQrSWF8gvEhDQUmD4OmeQcqmF0+6EgCZDMSwJPOzEFog=="
		url='https://ussouthcentral.services.azureml.net/workspaces/567e2fd383474b1ea65f5da77b3ddc17/services/05a56dc851444d4c95b39ccaa9f1d4ad/execute?api-version=2.0&format=swagger'
	
	elif id == 20:
		api_key="WqBTk/rqQ6KTgcjPBNizDyshm30kylwEiATgnRMHBomKt9FE6GwWykIEfzaul3CXHzdRVwSh0+ZhmacqqWcyng=="
		url='https://ussouthcentral.services.azureml.net/workspaces/567e2fd383474b1ea65f5da77b3ddc17/services/36d29b548d544ff4959d14b052811d8d/execute?api-version=2.0&format=swagger'
	
	elif id == 21:
		api_key="AsOdFXW+oUEmzk0p04bk1whWsKc7L2D0cm0LbEUzepxADf4FatYOrKWciOuqNsk6jdbaJPB5KXTnNpoVj7Cvlg=="
		url='https://ussouthcentral.services.azureml.net/workspaces/567e2fd383474b1ea65f5da77b3ddc17/services/7b950437bb844234b83b398c2472f125/execute?api-version=2.0&format=swagger'
	recommendations=None
	if getitems(url,api_key,user) != "error":
		recommendations=json.loads(getitems(url,api_key,user))
	departmentrec=getrecommendationsaslist(recommendations)	
	
	topsellerdf=pd.read_csv('static/recommendationperdepartmen.csv')
	topseller=(topsellerdf[topsellerdf['department_id']== id]['product_name']).tolist()
	return render_template('department.html',depname=name,user=user,departmentrec=departmentrec,topseller=topseller)


	
@app.route('/signup',methods=['POST'])
def signup(user=None):
	userlist=pd.read_csv('static/userlist.csv')
	userlist['userid']=userlist['userid'].astype('str')
	username=str(request.form['username'])
	
	check=userlist[userlist['userid']==username]
	logger.debug(check)
	if check['userid'].empty :
		
		username = request.form['username']
		
		session['logged_in']=True
		session['username']=username
		session['isadmin']=False
		return homepage(user=username)
	else:
		return homepage(regerror="Username Already exist")
		
	

	
@app.route('/logout/',methods=['GET'])
def logout():
	session.clear()
	return homepage()

	
	
	
@app.route('/admindashboard',methods=['GET'])
@login_required
def admindashboard():
	if session['isadmin']:
		urls=['https://us-east-1.online.tableau.com/t/dsproject/views/Instacart_Data/SalesMetric?:embed=y&:showAppBanner=false&:showShareOptions=true&:display_count=no&:showVizHome=no']
		iframe = random.choice(urls)
		 
		return render_template("admin.html",iframe=iframe)
	else:
		return render_template("main.html",user=None)



		
if __name__ == "__main__":
	
	app.secret_key= "Tusharapplicationasddsasadsdasa"
	app.run(port=80,debug=True)
	