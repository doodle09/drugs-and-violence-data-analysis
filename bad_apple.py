import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

crime=pd.read_csv(r"C:\Users\hardi\Downloads\archive\crimes_us_states.csv")
drugs=pd.read_csv(r"C:\Users\hardi\Downloads\archive\Youth_Risk_Behavior_Surveillance_System.csv")

#                                              crime table analysis

# print("The shape of crime table is: ")
# print(crime.shape)
# print(" The columns present in the crime table are: ")
# print(crime.columns)
# print("Other basic info regarding the crime table")
# print(crime.head())
# print(crime.tail())
# print(crime.info())
# print(crime.describe())

#                                             drugs table analysis
# print("The shape of the drugs table is: ")
# print(drugs.shape)
# print("The columns present in the drugs table are: ")
# print(drugs.columns)
# print("Other basic info regarding the drugs table")
# print(drugs.head())
# print(drugs.tail())
# print(drugs.info())
# print(drugs.describe())

# drop unwanted columns and rows from drugs

drugs.drop( columns=["greater_risk_low_confidence_limit","greater_risk_high_confidence_limit","lesser_risk_low_confidence_limit","lesser_risk_high_confidence_limit"], inplace=True)
# print(drugs.columns)

# print(drugs.isnull())
drugs.drop(drugs[drugs['sample_size']==0].index, inplace=True)
drugs.drop(drugs[drugs['greater_risk_data_value'].isna()] .index, inplace=True)
drugs.drop(drugs[drugs['lesser_risk_data_value'].isna()] .index, inplace=True)

drugs.drop(drugs[drugs['topic']=='Dietary Behaviors'].index, inplace=True)
drugs.drop(drugs[drugs['topic']=='Obesity, Overweight, and Weight Control'].index, inplace=True)
drugs.drop(drugs[drugs['topic']=='Other Health Topics'].index, inplace=True)

#                                             data analysis on drugs 

# greater risk vs location
risk_vs_location=drugs.groupby('location')['greater_risk_data_value'].mean().sort_values(ascending=False)
print('Overall risk vs location : ')
print(risk_vs_location.head())

# alcohol and drugs vs location
state_with_drugs=drugs[drugs['topic']=='Alcohol and Other Drug Use'] 
drug_by_location= state_with_drugs.groupby('location')['greater_risk_data_value'].mean().sort_values(ascending=False)
print('Alcohol and drugs vs location : ')
print(drug_by_location.head())

# drugs vs violence
violence= drugs[drugs['topic']=='Unintentional Injuries and Violence']
violence_by_location= violence.groupby('location')['greater_risk_data_value'].mean().sort_values(ascending=False)
drug_vs_violence= pd.concat([drug_by_location,violence_by_location],axis=1)
drug_vs_violence.columns=['drugs risk','violence risk']
print('Drugs vs violence : ')
print(drug_vs_violence.head())

# drugs vs gender
drugs_vs_sex= state_with_drugs.groupby(['location','sex'])['greater_risk_data_value'].mean().unstack().sort_index()
drugs_vs_sex.columns=['females doing drugs','males doing drugs','total']
print('Drugs vs gender : ')
print(drugs_vs_sex.head())

# drugs vs race
drugs_vs_race=state_with_drugs.groupby('race')['greater_risk_data_value'].mean().sort_values(ascending=False)
print('Drug vs race : ')
print(drugs_vs_race.head())

# risk vs year
year_risk= drugs.groupby('year')['greater_risk_data_value'].mean().sort_index()
print('Risk vs year : ')
print(year_risk.head())

# year vs drugs
year_drugs= state_with_drugs.groupby('year')['greater_risk_data_value'].mean().sort_index()
print('Drugs vs year : ')
print(year_drugs.head())


#                                               data analysis on crime
# state vs murder
state_murder= crime[['location','Murder']].sort_values(by='Murder', ascending=False)
print('State vs murder : ')
print(state_murder.head())

# state vs assault
state_assault=crime[['location','Assault']].sort_values(by='Assault', ascending=False)
print('State vs assault')
print(state_assault.head())

# state vs rape
state_rape=crime[['location','Rape']].sort_values(by='Rape', ascending=False)
print('State vs rape : ')
print(state_rape.head())

# state vs murder vs assault vs rape
state_all=crime[['location','Murder','Assault','Rape']].sort_values(by='Murder', ascending=False)
print('State vs avg_murder  vs avg_assault vs avg_rape : ')
print(state_all.head())

#                                                    analysis on both -

# location vs risk, murder, assault, rape
merged=pd.merge(drugs,crime, on='location',how='inner')
risk_all=merged.groupby('location')[['greater_risk_data_value','Murder','Assault','Rape']].mean().sort_values(by='greater_risk_data_value', ascending=False)
print('Risk vs avg_murder vs avg_assault vs avg_rape : ')
print(risk_all.head())

# location vs drugs & alcohol vs murder, assault, rape
merge_drug=pd.merge(state_with_drugs,crime, on='location',how='inner')
drugs_all =merge_drug.groupby('location')[['greater_risk_data_value','Murder','Assault','Rape']].mean().sort_values(by='greater_risk_data_value', ascending=False)
print('Drugs vs avg_murder vs avg_assault vs avg_rape : ')
print(drugs_all.head())

#                                                        GRAPHS   

# subplot (location vs drugs-- bar  &  race vs drugs-- pie)
top_5= drug_by_location.tail(5)
fig,ax= plt.subplots(2,1,figsize=(10,8))
ax[0].bar(top_5.index,top_5.values, color='orange')
ax[0].set_xlabel('locations')
ax[0].set_ylabel('drugs & alcohol consumption %')
ax[0].set_title('location vs drugs & alcohol consumption')
ax[0].set_ylim(10)

# ax[1].pie(drugs_vs_race.values, labels=drugs_vs_race.index,autopct='%1.1f%%',shadow=True,explode=[0.2,0.2,0,0,0,0,0,0],startangle=90)
# ax[1].set_title('DRUGS VS RACE')
# plt.tight_layout()
# plt.savefig('plot1.png',dpi=300,bbox_inches='tight')
# plt.show()

# subplot ( drugs vs violence-- scatter plot  &  drugs vs year-- line chart)
top_drug_violence= drug_vs_violence.tail(7)
# fig,ax=plt.subplots(1,2,figsize=(15,4))
ax[1].scatter(top_drug_violence.index, top_drug_violence['drugs risk'],s=top_drug_violence['violence risk']*70,edgecolors='black')
ax[1].set_xlabel('locations')
ax[1].set_ylabel('drug & alcohol consumptions')
# ax[0].text(1,32, ' buble size= violence , As drugs consumption increases the violence increases',fontsize=10,bbox=dict(alpha=0.5))
ax[1].set_title('Top 7 locations for drugs vs violence')

# ax[1].plot(year_drugs.index, year_drugs.values, marker='o')
# ax[1].set_xlabel('years')
# ax[1].set_ylabel('drugs consumption')
# ax[1].set_title('Drugs consumption by year')
plt.tight_layout()
plt.savefig('this.png',dpi=300,bbox_inches='tight')
plt.show()

# # subplot (location vs murder count  &  assault count  &  rape count)
# top7_m= state_murder.head(7)
# top7_a= state_assault.head(7)
# top7_r=state_rape.head(7)
# fig,ax=plt.subplots(2,2,figsize=(12,5))
# ax[0,0].barh(top7_m['location'],top7_m['Murder'],color='red',label='murder')
# ax[0,0].set_xlabel('Locations')
# ax[0,0].set_ylabel('Murders count')
# ax[0,0].legend()
# ax[0,0].set_title(' top 7 location with highest Murder count')

# ax[0,1].barh(top7_a['location'],top7_a['Assault'],color='orange', label='assault')
# ax[0,1].set_xlabel('locations')
# ax[0,1].set_ylabel('Assault count')
# ax[0,1].legend()
# ax[0,1].set_title('top 7 locations with highest assault count')

# ax[1,0].barh(top7_r['location'],top7_r['Rape'],color= 'blue', label='rape')
# ax[1,0].set_xlabel('locations')
# ax[1,0].set_ylabel('Rape count')
# ax[1,0].legend()
# ax[1,0].set_title('top 7 locations with highest rape count')

# ax[1,1].axis('off')
# plt.tight_layout()
# plt.savefig('plot3.png',dpi=300,bbox_inches='tight')
# plt.show()

# # location vs drugs by gender
# top_gender= drugs_vs_sex.head(10)
# melted=top_gender.reset_index().melt(id_vars='location',value_vars=['females doing drugs','males doing drugs'],var_name='Gender',value_name='overall')
# sns.barplot(data=melted, x='location',y='overall',hue='Gender',palette='Set1')
# sns.set_style('dark')
# plt.savefig('plot4.png',dpi=300,bbox_inches='tight')
# plt.show()

# # correlation btwn risk $ all crimes
# sns.heatmap(data=risk_all.corr(), annot=True, cmap='coolwarm')
# plt.title('Correlation btwn risk and crimes')
# plt.savefig('plot5.png',dpi=300,bbox_inches='tight')
# plt.show()

# # relation btwn drugs & all crimes
# graph=sns.PairGrid(data=drugs_all,palette='Set1')
# graph.map_upper(sns.scatterplot)
# graph.map_lower(sns.kdeplot,fill=True)
# graph.map_diag(sns.histplot)
# graph.fig.suptitle('RELATIONSHIP BTWN DRUGS AND CRIMES' ,fontsize=14)
# plt.subplots_adjust(top=0.93)
# plt.savefig('plot6.png',dpi=300,bbox_inches='tight')
# plt.show()