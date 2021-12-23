import pandas as pd #for using dataframes, importing datasets
import numpy as np #for mathematical operations
import seaborn as sns #for visualization
import matplotlib.pyplot as plt #for visualization
from openpyxl import Workbook #for importing excel workbook

df = pd.read_excel(r"dataset/MarketSales.xlsx")

### Data Overview ###

#Shape
df.shape

#Types
df.dtypes

#Head
df.head(20)

#Tail
df.tail(20)

#Describe
df.describe().T

#Total Numbers of Nulls
df.isnull().sum()

### Analysis of categorical variables ###

[print(col, df[col].dtypes,df[col].nunique()) for col in df.columns]
#I am trying to understand which is categorical
# and which is cardinal variable by observing the frequency of the data inside the variables.

cat_val = [col for col in df.columns if df[col].dtypes == "O" and df[col].nunique() < 360]
#Although the types of variables such as clientcode, clientname are object, I did not include them in my categorical
#data group because their frequencies are very high. I categorically take variables with a maximum frequency of 360.

num_but_cat = [col for col in df.columns if df[col].dtype in [int,float] and df[col].nunique() < 100]
#I have included int and float values with a frequency less than 100 in my numeric but categorical variables.

cat_val = cat_val + num_but_cat

### Analysis of Numerical Variables ###

#First column is ID that is a index columns.
#Numerical variables are "AMOUNT", "PRICE", "LINENETTOTAL", "LINENET"

num_cols = [col for col in ["AMOUNT", "PRICE", "LINENETTOTAL", "LINENET"]]


### Correlation Analysis ###


corr = df[num_cols].corr()
corr
#We can see there is high correlation between "LINENET" and "LINENETTOTAL".

#Visualization correlation among numerical variables.
sns.set(rc={'figure.figsize': (12, 12)})
sns.heatmap(corr, cmap="RdBu")
plt.show()

#or

pip install klib
import klib
klib.corr_plot(corr)
plt.show()

plt.figure(figsize=(10,5))
sns.regplot(x="LINENET", y="LINENETTOTAL",data=df)
plt.xlim(0,400)
plt.ylim(0,400)
plt.show()


### Grouping and aggregation of datas for some insights ###

#LINENETTOTAL's sum, mean, min and max values by GENDER
df[["LINENETTOTAL","GENDER"]].groupby("GENDER").agg({"LINENETTOTAL":["sum","mean","min", "max"]})


#AMOUNT totals by CATEGORY

df[["CATEGORY_NAME1","AMOUNT"]].groupby(["CATEGORY_NAME1"]).agg({"AMOUNT":"sum"})

#Top 10 branches with the highest revenue

df[["BRANCH","LINENETTOTAL"]].groupby(["BRANCH"]).agg({"LINENETTOTAL":"sum"}).sort_values("LINENETTOTAL",ascending = False).head(10)

#The Region with the lowest revenue

df[["REGION","LINENETTOTAL"]].groupby(["REGION"]).agg({"LINENETTOTAL":"sum"}).sort_values("LINENETTOTAL",ascending = True).head(2)

#Sales totals and means according to weekdays and weekends

w_df = pd.DataFrame(pd.to_datetime(df['DATE_']))
w_df["WEEK_VARIABLE"] = w_df["DATE_"].dt.dayofweek
w_df["WEEKENDORNOT"] = ["WEEKEND" if week_variable > 4 else "WEEKDAY" for week_variable in w_df["WEEK_VARIABLE"]]
w_df["LINENETTOTAL"] = df["LINENETTOTAL"]

w_df[["LINENETTOTAL","WEEKENDORNOT"]].groupby("WEEKENDORNOT").agg({"LINENETTOTAL":["sum","mean"]})

#Top 10 salesman with the highest total

df[["SALESMAN","LINENETTOTAL"]].groupby(["SALESMAN"]).agg({"LINENETTOTAL":"sum"}).sort_values("LINENETTOTAL",ascending = False).head(10)

#Top 10 CLIENT with the highest total

df[["CLIENTNAME","CLIENTCODE","LINENETTOTAL"]].groupby(["CLIENTNAME","CLIENTCODE"]).agg({"LINENETTOTAL":"sum"}).sort_values("LINENETTOTAL",ascending = False).head(10)

### Visulization ###

#Categorical Variables's Visulization
for col in cat_val:
    sns.countplot(x=df[col], data=df)
    plt.show()

#Distribution of linenettotal by gender
sns.boxplot( x=df["GENDER"], y=df["LINENETTOTAL"] )
plt.ylim(0,50)
plt.show()

#View price ranges of categories
ax = sns.barplot(x="CATEGORY_NAME1", y="PRICE", data=df)
ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right")
plt.show()

#In order to share my understanding of the concepts and techniques I know,
# I will take an example from the Market Sales dataset available on Kaggle
# and try to get as much insight as possible from the dataset using EDA.
# I got the Market Sales data set from the Omer Colakoglu's data set that
# one of the leading SQL and database instructor in Turkey, shared publicly on Kaggle. I thank him for the data set.
