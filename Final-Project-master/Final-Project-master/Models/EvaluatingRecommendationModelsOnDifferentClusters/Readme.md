### This Directory Contains the three recommendation models performance and comparison notebooks that we ran on different clustered and non-clustered data
### We used the Graphlab library because it utilized the spark clusters on the IBM DSX and gave us results
### Without it we were getting memory errors even on 100gb memory cloud vm 


#### We tested these sets on 3 models:
  1.  Item-based Recommendation models
  2.  Popularity Based Recommendation models
  3.  Model-Based Recommendation system
  
  
### Please find the description of datsets used in the ipynb files below
   
   1. aisleclusterrecommendation.ipynb - Data used is the clustered data on basis of the aisle to which the products belongs
   2.  alldatarecommendation.ipynb - All Data No clustering
   3.  DaytimeClusterrecommendation.ipynb - Data is clustered on the basis of the particular hour of the day
   4. DepartmentClusterrecommendation.ipynb - Data is clustered on the basis of the department the product belongs to
   5.  DOWRecommendation.ipynb - Data is clustered on the basis of the Day the product was bought
   6.  hourrecommendation.ipyb-  Data is clustered on the basis of the hour the product was bought
   
   
#### So far for all the datasets used the best results were given to us by Model-based recommendation system which converts users features into latent variables and use them for recommendation

The best mean recall found was 0.28

