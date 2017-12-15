# Final-Project for INFO 7390-Advanced Data Science
#### Project Name - Instacart Market Basket Analysis
#### Link to Video Proposal - https://www.youtube.com/watch?v=mqcd3F2N5Io&feature=youtu.be
#### Dataset Name and Link - 
https://www.instacart.com/datasets/grocery-shopping-2017 (This is the original source provided by instacart and we used this in our luigi pipeline)
https://www.kaggle.com/c/instacart-market-basket-analysis/data
#### Link to Project Demo Website - 35.190.167.191
##### Note to login try using any integer value from 1-230000 as username and any password, Also for accessing the admin page use username-admin, password-tushar

#### Link for the presentation on SlideShare: https://www.slideshare.net/TusharGoel42/final-project-ads-info7390

### Made by:
              1. Tushar Goel 
              2. Jaini Bhansali
### Professor-Srikanth Krishnamurthy

##### This Github Repo contains the final project for the course INFO 7390 under the guidance of Professor Srikanth Krishnamurthy and TA Nand Govind Modani.

##### Directory Structure of this repo:
  1. EDA and Summary Metrics - This folder contains the jupyter notebook that contains all the exploratory data analysis and tableau visualizations
  2. LuigiPipeline&Docker - This folder contains the luigi pipeline code in a python file along with docker commands to pull the docker image or create your own
  3. Models - This folder contains all the approaches with summary metrics that we used. It has 2 subfolders a. Apriori b. Recommendation Systems
  4. Webapp - Contains the whole code for the webapplication along with commands on how to run it and the script that can be used without the webapplication
  
 Our Goal 

Our aim was to create a recommendation system for Instacart. The recommendation system would help Instacart as follows: 
1.	Instacart has a faithful following of users. Hence, Recommender system has the ability to predict whether a particular user would prefer an item or not, based on the user’s profile. This helps the seller and the consumer.
2.	Instacart benefits as recommender systems reduce the transaction cost of finding and selecting items in an online shopping environment
3.	Instacart Users benefit as this will  improve the decision making process and quality 
4.	Recommender systems enhance revenue as it effectively enables selling products and hence, benefits by increasing revenues.
5.	This also allows users to beyond catalog searches.
Our Approach

We have primarily used the following recommendation Systems:
1.	Collaborative Filtering Technique – Model Based Filtration technique
2.	Association Rule Mining – Apriori Algorithm



Stakeholders Benefited
1.	Instacart will benefit by enhanced revenues and retain its faithful customers luring them to come back each time
2.	Instacart Customers will be the beneficiaries of this system as they will experience a better user experience, and also allow them to narrow their search based on the wide variety of products that Instacart provides. Thus, improving the decision making experience as well.

In order to achieve our goal we used the Instacart Dataset that has been made public. The details of the dataset are present below.

 
### To get more details on the project please check the file FinalProjectReport.pdf
