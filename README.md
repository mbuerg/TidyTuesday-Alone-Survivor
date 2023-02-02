# TidyTuesday-Alone-Survivor
Ein Beitrag zum tidy tuesday

Eine paar deskriptive plots und eine Survival Analyse der Alone Show. Es ist eine Überlebensshow in der die Teilnehmer
Gegenstände erhalten und eine gewisse Zeit in der Wildnis "überleben" müssen. Wer als letztes übrig bleibt gewinnt. Tidy Tuesday 2023 Woche 4. 
Daten stammen von 

https://gradientdescending.com/alone-r-package-datasets-from-the-survival-tv-series/

## Die Plots sollten größtenteils selbsterklärend sein
![1](https://user-images.githubusercontent.com/106337257/216415716-50a21607-acce-42c3-acfb-b5e4acc2072e.png)
![2](https://user-images.githubusercontent.com/106337257/216415937-a927351e-9b8e-4969-b23a-ebc4eb51a529.png)
![3](https://user-images.githubusercontent.com/106337257/216415950-a21dca58-785d-4822-9eab-f4d1f56ac0cb.png)
![4](https://user-images.githubusercontent.com/106337257/216415959-cac5081f-64c1-4f94-a7c6-3c2ad5602b81.png)
![5](https://user-images.githubusercontent.com/106337257/216415973-eb5c2b3c-e2d0-425c-bda1-30a0539ce525.png)
![6](https://user-images.githubusercontent.com/106337257/216415985-82a828a1-e2f6-4e65-8f92-220224eccb74.png)
![7](https://user-images.githubusercontent.com/106337257/216415995-a798e11b-15b3-46b1-8b6d-17762e881329.png)
![8](https://user-images.githubusercontent.com/106337257/216416003-922a0254-ea47-4cf9-b611-83750f853090.png)
![9](https://user-images.githubusercontent.com/106337257/216416023-8af4d8dd-b275-4793-ad81-e67afd4ee94a.png)

## 
Das Modell besteht aus den unabhängigen Variablen state, gender, age und dem Ausscheidungsgrund. 
Im folgenden Plot sieht man den Einfluss, den Variablen auf die Wahrscheinlichkeit haben, auszuscheiden. Positiv ist schlecht, Negativ ist gut. Die letzte Variable ist
natürlich selbstverständlich stark negativ. Überraschend ist, dass das Alter keinen Einfluss zu haben scheint. Eine interessante Frage ist, ob es einen
Grund gibt, warum manche US Bundesstaaten als Herkunftsländer der Teilnehmer besser abschneiden als andere. Denkbar wäre, dass es in einigen Staaten eher eine
Kultur gibt, wo Hobbies die Überlebensfähigkeiten in der Wildnis schulen. Ähnlichkeit der Drehorte mit den Herkunftsorten der Gewinner ist eine Untersuchung wert.
Des Weiteren überrascht es, dass Männer einfacher ausscheiden. Vielleicht liegt dies an einer höheren Risikobereitschaft? Dies könnte man testen, indem man 
den statistischen Zusammenhang zwischen Geschlecht und Ausstiegsgrund überprüft.Vielleicht ist es auch nur Zufall, da bisher nur vergleichsweise wenige 
Frauen teilgenommen haben und hier ein Selektionsbias vorherrscht.

![10](https://user-images.githubusercontent.com/106337257/216416040-1974d01f-73f3-4cc7-a8f7-53db4631f7cb.png)
