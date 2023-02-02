# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 16:58:05 2023

@author: buerg
"""

# tidytuesday 2023-week-4
# Es handelt sich um 4 Datensätze. Die features beschreiben Eigenschaften
# von Teilnehmern einer Überlebensshow
# https://gradientdescending.com/alone-r-package-datasets-from-the-survival-tv-series/


# import modules

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from lifelines import KaplanMeierFitter
from lifelines import CoxPHFitter

survivalists = pd.read_csv(r"path\survivalists.csv",
                           index_col = 0)
loadouts = pd.read_csv(r"path\loadouts.csv",
                       index_col = 0)
episodes = pd.read_csv(r"path\episodes.csv",
                       index_col = 0)
seasons = pd.read_csv(r"path\seasons.csv",
                      index_col = 0)

# Die Daten sind von einer Struktur, dass mit unterschiedlichen Zeitpunkten
# Teilnehmer die Show verlassen. Dies ist äquivalent zu survival Studien, wo
# mehrmals die Zeit gestoppt wird und gemessen wird bei wievielen Teilnehmern
# ein Ereignis eingetreten ist (zB der Tot bei Krebsstudie).
# Solche Survival Analysen können simpel deskriptiv sein, aber auch inferentiell.

###############################################################################
# Daten vorbereiten
# Season und Episodes joinen
seasons_and_episodes = seasons.merge(episodes, how = "outer", on = "season")

# In Staffel sind Wiederholer drin. Diese werden umbenannt
survivalists["name"][survivalists["name"].duplicated()] = (survivalists["name"]
                                                           [survivalists["name"]
                                                            .duplicated()]
                                                           .str.lower())
loadouts["name"][loadouts["season"] == 5] = (loadouts["name"]
                                             [loadouts["season"] == 5]
                                             .str.lower())

survivalists_and_loadouts = (survivalists.merge(loadouts, how = "outer", 
                                                on = ["season", "name"]))



seasons_and_episodes_description = seasons_and_episodes.describe(include = "all")
seasons_and_episodes_info = seasons_and_episodes.info()


# version_x und version_y, die durchs mergen entstanden sind sind Konstanten
print(seasons_and_episodes["version_x"].unique())
print(seasons_and_episodes["version_y"].unique())

seasons_and_episodes = (seasons_and_episodes.drop(["version_x", "version_y"], 
                                                  axis = 1))

###############################################################################
# Entwicklung der EPisodenanzahl pro Staffel

seasons_grouped_loc = (seasons_and_episodes.groupby(by = ["season", "location"])
                   .count()["country"])

seasons = seasons_and_episodes["season"].unique()
location = seasons_grouped_loc.index.get_level_values(1)
bar_values = seasons_grouped_loc.values

# bar chart, Anzahl Episoden und Drehorte

def drehorte_fuer_barchart(drehort):
    for i in range(len(drehort)):   
        ax.text(i+0.9, 3, drehort[i], rotation = 90, color = "black")

fig, ax = plt.subplots()
ax.bar(seasons,bar_values)
ax.set_xticks(seasons, seasons)
drehorte_fuer_barchart(location)
ax.set_title("Anzahl Episoden und deren Drehort")
ax.set_xlabel("Staffel")
ax.set_ylabel("Anzahl Episoden")
ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)


# Viewer Entwicklung

seasons_grouped_viewers_avg = (seasons_and_episodes.groupby(by = ["season"])
                               .mean()["viewers"])


def datenbeschriftung(daten):
    for i, j in enumerate(daten):
        if i+1 in [1, 4, 6, 8]:
            ax.text(i+0.9, j+0.1, np.round(j, 2))
        

fig, ax = plt.subplots()
ax.plot(seasons_grouped_viewers_avg.index, seasons_grouped_viewers_avg)
ax.set_ylim(0, 2.5)
datenbeschriftung(seasons_grouped_viewers_avg)
ax.set_title("Durchschnittliche Zuschauer pro Staffel in Millionen")
ax.set_xlabel("Staffel")
ax.get_yaxis().set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)
ax.spines["left"].set_visible(False)


# imdb ratings, n ratings

seasons_grouped_imdb_ratings = (seasons_and_episodes.groupby(by = ["season"])
                                .mean()["imdb_rating"])
seasons_grouped_n_ratings = (seasons_and_episodes.groupby(by = ["season"])
                             .mean()["n_ratings"])


def datenbeschriftung_erste_achse(daten):
    for i, j in enumerate(daten):
        if i+1 in [1, 4, 7, 9]:
            ax1.text(i+0.8, j+4, int(np.round(j)))


def datenbeschriftung_zweite_achse(daten):
    for i, j in enumerate(daten):
        if i+1 in [1, 4, 7, 9]:
            ax2.text(i+0.8, j+0.3, np.round(j, 1))


fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
# Erste Achse
ax1.bar(seasons_grouped_n_ratings.index, seasons_grouped_n_ratings,
        label = "Anzahl Bewertungen")
ax1.set_ylim(0, 200)
ax1.set_ylabel("Anzahl Bewertungen")
datenbeschriftung_erste_achse(seasons_grouped_n_ratings)
# Zweite Achse
ax2.plot(seasons_grouped_imdb_ratings.index, seasons_grouped_imdb_ratings, 
        label = "IMDB Durchschnitt", color = "black")
ax2.set_ylabel("Durchschnittsbewertung IMDB")
ax2.set_ylim(0, 12)
datenbeschriftung_zweite_achse(seasons_grouped_imdb_ratings)
ax1.set_title("Durchschnittliche IMDB Bewertungen")
ax1.set_xlabel("Staffel")
ax1.set_xticks(seasons, seasons)
ax1.legend(loc='upper left')
ax1.spines["right"].set_visible(False)
ax1.spines["top"].set_visible(False)
ax1.spines["left"].set_visible(False)
ax2.legend(loc='upper right')
ax1.get_yaxis().set_visible(False)
ax2.get_yaxis().set_visible(False)
ax2.spines["right"].set_visible(False)
ax2.spines["top"].set_visible(False)
ax2.spines["left"].set_visible(False)

###############################################################################
# Deskriptive Analyse der survivalists
# Verteilung der Geschlechter
gender_grouped = survivalists.groupby(by = ["season", "gender"]).count()
gender_grouped["sex"] = gender_grouped.index.get_level_values(1)
x_coordinate = pd.Series(gender_grouped.index.get_level_values(0)).unique()
y_values_men = gender_grouped[gender_grouped["sex"] == "Male"]["name"]
y_values_women = gender_grouped[gender_grouped["sex"] == "Female"]["name"]

# In Season 1 gab es keine Frauen, y_values_women muss dort mit einer Null
# aufgefüllt werden, sonst kommt shape error

season_wo_women = (pd.Series(y_values_men.index.get_level_values(0))
                   .isin(pd.Series(y_values_women.index.get_level_values(0))))
season_wo_women_index = list(season_wo_women[season_wo_women == False].index)
y_values_women_complete = y_values_women.append(pd.Series(0, 
                                        index = [(1, "Female")])).sort_index()

def datenbeschriftung_m(daten):
    for i, j in enumerate(daten):
        ax.text(i+0.9, 1, np.round(j, 2))
        
def datenbeschriftung_w(daten, hoehe):
    for i, j in enumerate(daten):
        if i+1 != 1:
            ax.text(i+0.9, hoehe[i+1]+0.2, np.round(j, 2))

fig, ax = plt.subplots()
ax.bar(x_coordinate, y_values_men, label = "Männer")
ax.bar(x_coordinate, y_values_women_complete, label = "Frauen", 
       bottom = y_values_men)
datenbeschriftung_m(y_values_men)
datenbeschriftung_w(y_values_women_complete, y_values_men)
ax.set_xlabel("Staffel")
ax.set_xticks(x_coordinate, x_coordinate)
ax.legend()
ax.set_title("Anzahl Teilnehmer nach Geschlecht pro Staffel")
ax.get_yaxis().set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)
ax.spines["left"].set_visible(False)


# Histogramm für die Altersverteilung

alter = survivalists_and_loadouts.groupby(by = "name").mean()["age"]

fig, ax = plt.subplots()
ax.hist(alter, bins = 20, density = True)
ax.set_xlabel("Alter")
ax.set_ylabel("Wahrscheinlichkeit")
ax.set_title("Altersverteilung während der gesamten Serie")
ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)


# Plot für die items bauen

items = survivalists_and_loadouts.groupby("item").count()["season"]
items_top_ten = items.sort_values(ascending = False).iloc[:10]

def datenbeschriftung_items(daten):
    for i, j in enumerate(daten):
        ax.text(i-0.2, j+3, j)

fig, ax = plt.subplots()
ax.bar(items_top_ten.index, items_top_ten)
ax.set_xticklabels(items_top_ten.index, rotation=45, ha = "right")
ax.set_xlabel("Gegenstand")
ax.set_title("Top 10 Gegenstände")
datenbeschriftung_items(items_top_ten)
ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)
ax.spines["left"].set_visible(False)
ax.get_yaxis().set_visible(False)


# Plot für die Aussteigsgründe

reason = (survivalists_and_loadouts.groupby(by = "reason_category")
          .count()["season"].sort_values(ascending = False))

def datenbeschriftung_reasons(daten):
    for i, j in enumerate(daten):
        ax.text(i-0.1, j+10, j)

fig, ax = plt.subplots()
ax.bar(reason.index, reason)
datenbeschriftung_reasons(reason)
ax.set_xlabel("Grund")
ax.set_title("Ausstiegsgründe")
ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)
ax.spines["left"].set_visible(False)
ax.get_yaxis().set_visible(False)



###############################################################################
# Survival Analysis

survivalists_and_loadouts["state"] = (survivalists_and_loadouts["state"].
                                      fillna("Unknown"))
survivalists_and_loadouts["reason_category"] = (survivalists_and_loadouts["reason_category"]
                                                .fillna("Winner"))

data_to_fit = (survivalists_and_loadouts[["name","age", "gender", 
                                          "reason_category",
                                  "state", "days_lasted", "result"]].
               drop_duplicates().
               reset_index(drop = True))

data_to_fit["result"][data_to_fit["result"] != 1] = 0
data_to_fit["result"] = (data_to_fit["result"]-1).abs()

# Deskriptiv per Kaplan Meier
kmf = KaplanMeierFitter()
kmf.fit(data_to_fit["days_lasted"], event_observed = data_to_fit["result"])


fig, ax = plt.subplots()
ax.plot(kmf.survival_function_.index, kmf.survival_function_["KM_estimate"])
ax.set_xlabel("Dauer")
ax.set_ylabel ("Wahrscheinlichkeit")
ax.set_title("Survival Funktion der Teilnehmer")
ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)

# Survival Funktionen der Geschlechter
data_to_fit_female = data_to_fit[data_to_fit["gender"] == "Female"]
data_to_fit_male = data_to_fit[data_to_fit["gender"] == "Male"]
kmf_female = KaplanMeierFitter()
kmf_female.fit(data_to_fit_female["days_lasted"], 
               event_observed = data_to_fit_female["result"])

kmf_male = KaplanMeierFitter()
kmf_male.fit(data_to_fit_male["days_lasted"], 
             event_observed = data_to_fit_male["result"])


fig, ax = plt.subplots()
ax.plot(kmf_female.survival_function_.index, 
        kmf_female.survival_function_["KM_estimate"], label = "Frauen")
ax.plot(kmf_male.survival_function_.index, 
        kmf_male.survival_function_["KM_estimate"], label = "Männer")
ax.set_xlabel("Dauer")
ax.set_ylabel ("Wahrscheinlichkeit")
ax.set_title("Survival Funktionen der Geschlechter")
ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)
ax.legend()

# Regressiv per Cox Regression
# Modelle mit unterschiedlichen Penalizern durchlaufen lassen und das mit dem
# kleinsten AIC nehmen
penalizers = np.linspace(0.001, 1, 1000)
penalizers_dict = {}
for i in penalizers:
    cph = CoxPHFitter(penalizer = i)
    cph_fit = cph.fit(data_to_fit, duration_col="days_lasted", event_col="result",
            formula = "state + age + gender + reason_category")
    penalizers_dict[f"{i}"] = np.round(cph_fit.AIC_partial_, 0)

penalizer_lowerst_aic = np.round(float(min(penalizers_dict, 
                                           key=penalizers_dict.get)), 4)

cph = CoxPHFitter(penalizer = penalizer_lowerst_aic)
cph_fit = cph.fit(data_to_fit, duration_col="days_lasted", event_col="result",
        formula = "state + age + gender + reason_category")
cph_fit.print_summary()

fig, ax = plt.subplots()
cph_fit.plot()
plt.rc('ytick', labelsize=4)
