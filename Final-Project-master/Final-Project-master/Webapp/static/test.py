import pandas as pd

p=pd.read_csv('userlist.csv')
check=p[p['userid']==1]
print(check)
if check['userid'].empty:
	print("no")
else:
	print("yes")