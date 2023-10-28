import pandas as pd
import matplotlib.pyplot as plt
confirmed = pd.read_csv('covid19_confirmed.csv')
deaths = pd.read_csv('covid19_deaths.csv')
recovered = pd.read_csv('covid19_recovered.csv')
confirmed = confirmed.drop(['Province/State', 'Lat', 'Long'], axis=1)
deaths = deaths.drop(['Province/State', 'Lat', 'Long'], axis=1)
recovered = recovered.drop(['Province/State', 'Lat', 'Long'], axis=1)
confirmed = confirmed.groupby(confirmed['Country/Region']).aggregate('sum')
deaths = deaths.groupby(deaths['Country/Region']).aggregate('sum')
recovered = recovered.groupby(recovered['Country/Region']).aggregate('sum')
confirmed = confirmed.T
deaths = deaths.T
recovered = recovered.T
print("****confirmed*****",confirmed)
print("****deaths*****",deaths)
print("****recovered*****",recovered)
new_cases = confirmed.copy()
for day in range(1, len(confirmed)):
    new_cases.iloc[day] = confirmed.iloc[day] - confirmed.iloc[day - 1]
print("****new cases*****",new_cases.tail(10))
active_cases = confirmed.copy()
for day in range(0, len(confirmed)):
    active_cases.iloc[day] = confirmed.iloc[day] - deaths.iloc[day] - recovered.iloc[day] 
overall_growth_rate = confirmed.copy()
for day in range(1, len(confirmed)):
    overall_growth_rate.iloc[day] = ((active_cases.iloc[day] - active_cases.iloc[day-1]) / active_cases.iloc[day - 1]) * 100
print("*****overall growth rate*****", overall_growth_rate["Pakistan"].tail(10))
death_rate = confirmed.copy()
for day in range(0, len(confirmed)):
    death_rate.iloc[day] = (deaths.iloc[day] / confirmed.iloc[day]) * 100
hospitalization_rate_estimate = 0.05
hospitalization_needed = confirmed.copy()
for day in range(0, len(confirmed)):
    hospitalization_needed.iloc[day] = active_cases.iloc[day] * hospitalization_rate_estimate
estimated_death_rate = 0.03
print(deaths['India'].tail()[4] / estimated_death_rate)
ax = plt.subplot()
ax.set_facecolor('black')
ax.figure.set_facecolor('#121212')
ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')
ax.set_title('COVID-19 - Total Confirmed Cases', color='white')
ax.legend()
countries = ['Austria', 'Italy', 'US', 'Spain', 'China', 'Germany', 'India']
for country in countries:
    confirmed[country][0:].plot(label = country)
plt.legend(loc='upper left')
plt.show()
countries = ['India']
for country in countries:
    ax = plt.subplot()
    ax.set_facecolor('black')
    ax.figure.set_facecolor('#121212')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    ax.set_title(f'COVID-19 - Overall Active Growth Rate [{country}]', color='white')
    overall_growth_rate[country][800:].plot.bar()
    plt.show()
simulation_growth_rate = 0.001
dates = pd.date_range(start='3/29/2022', periods=50, freq='D')
dates = pd.Series(dates)
dates = dates.dt.strftime('%m/%d/%Y')
simulated = confirmed.copy()
simulated = simulated.append(pd.DataFrame(index=dates))
for day in range(len(confirmed), len(confirmed)+40):
    simulated.iloc[day] = simulated.iloc[day - 1] * (simulation_growth_rate + 1)
ax = simulated['India'][10:].plot(label="India")
ax.set_axisbelow(True)
ax.set_facecolor('black')
ax.figure.set_facecolor('#121212')
ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')
ax.set_title('simulated growth rate of COVID-19 in India', color='white')
ax.legend()
plt.show()