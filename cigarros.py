# -*- coding: utf-8 -*-
"""cigarros.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1g1pIFeBRrAcAAe1D_CfuzAoJNFT4XvtC

#**Notebook 06**
- **Professor:** Iális Cavalcante
- **Monitor:** Iago Magalhães
- **Disciplina:** Ciência de dados
- **Curso:** Engenharia da Computação
- **Descrição:**
No notebook 06 iremos aprender sobre regressão múltipla.
- **Questão:** O número de fumantes ainda é gigantesco e entender o comportamento desse público é de fundamental importância para campanhas de conscientização. Neste dataset, possuimos informações sobre consumidores de cigarros. Ajude a equipe de saúde a entender mais sobre os dados presente nessa base de dados, auxiliando com uma análise de dados sobre qual faixa de idade e sexo que mais consomem este produto e através de um algoritmo de regressão indique qual o valor gasto com cigarro por cada cliente.

##Importações de bibliotecas
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import metrics
import statsmodels.api as sm
pd.set_option('display.max_columns', 500)
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings("ignore")
from scipy.stats import kurtosis
import statsmodels.stats.api as sms
from statsmodels.compat import lzip
from statsmodels.graphics.gofplots import qqplot
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.stats.diagnostic import het_breuschpagan, het_goldfeldquandt,het_white
from statsmodels.stats.diagnostic import linear_harvey_collier, linear_reset, spec_white
from statsmodels.stats.diagnostic import linear_rainbow
from statsmodels.graphics.regressionplots import plot_leverage_resid2
from yellowbrick.regressor import CooksDistance
from statsmodels.stats.outliers_influence import OLSInfluence, variance_inflation_factor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error, r2_score

"""##Leitura de dados"""

df = pd.read_csv('insurance.csv')
df.head()

"""##Análise de dados"""

df.describe()

le = LabelEncoder()

#sex
le.fit(df.sex)
df.sex = le.transform(df.sex)

# smoker
le.fit(df.smoker)
df.smoker = le.transform(df.smoker)

#region
le.fit(df.region)
df.region = le.transform(df.region)

df.info()

corr = df.corr()
corr

f, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(corr, cmap=sns.color_palette("Blues"), linewidths=.5, annot=True);

plt.figure(figsize=(12,5))
plt.title("Distribuição dos custos")
ax = sns.distplot(df["charges"], color = 'b')

fig= plt.figure(figsize=(17,6))

ax=fig.add_subplot(121)
sns.distplot(df[(df.smoker == 1)]["charges"],color='r',ax=ax)
ax.set_title('Distribuição de gastos por fumantes');

ax=fig.add_subplot(122)
sns.distplot(df[(df.smoker == 0)]['charges'],color='c',ax=ax)
ax.set_title('Distribuição de gastos por não fumantes');

g = sns.catplot(x="smoker", kind="count",hue = 'sex', palette="Blues_r", data=df,legend_out= True)

# Eixos
(g.set_axis_labels("", "Total")
  .set_xticklabels(["Não Fumante", "Fumante"])
  )

# Legenda
g._legend.set_title('Sexo')
new_labels = ['Mulheres', 'Homens']
for t, l in zip(g._legend.texts, new_labels): t.set_text(l)

#Distribuição de gastos por fumante e não fumante por sexo
g= sns.catplot(x="sex", y="charges", hue="smoker",
            kind="violin", data=df, palette = 'Blues', legend_out= False, ax=ax);

# Eixos
(g.set_axis_labels("", "Gasto Total")
  .set_xticklabels(["Homens", "Mulheres"])
  )

# Legenda
leg = g.axes.flat[0].get_legend()
new_title = ''
leg.set_title(new_title)
new_labels = ["Não Fumante", "Fumante"]
for t, l in zip(g._legend.texts, new_labels): t.set_text(l)
g._legend.set_bbox_to_anchor((.39,1))

plt.figure(figsize=(12,5))
plt.title("Distribuição de idade")
ax = sns.distplot(df["age"], color = 'b')

plt.figure(figsize=(12,5))
plt.title("Distribuição de custos por idade e por fumantes")

#Distribuição de gastos por fumante e não fumante por sexo
sns.scatterplot(x=df.age,y=df.charges, hue= df.smoker, sizes=(12,5),  palette="ch:r=-.2,d=.3_r");

plt.figure(figsize=(12,5))
plt.title("Distribuição de IMC")
ax = sns.distplot(df["bmi"], color = 'b')

plt.figure(figsize=(12,5))
plt.title("Distribuição de custos com pacientes com IMC maior que 30")
ax = sns.distplot(df[(df.bmi >= 30)]['charges'], color = 'b')

plt.figure(figsize=(12,5))
plt.title("Distribuição de custos com pacientes com IMC menor que 30")
ax = sns.distplot(df[(df.bmi < 30)]['charges'], color = 'b')

sns.catplot(x="children", kind="count", palette="Blues", data=df);

#Distruição de Gastos por Fumantes e não fumantes
plt.figure(figsize=(12,5))
plt.title("Distribuição de custos por idade e por fumantes")
#Distribuição de gastos por fumante e não fumante por sexo
sns.scatterplot(x=df.children,y=df.charges, sizes=(12,5),  palette="ch:r=-.2,d=.3_r");

"""##Algoritmo de Machine Learning

###Algoritmo de Regressão Linear
"""

#Separando os dados
x = df.drop(['charges'], axis = 1)
y = df.charges

#Separe os dados de Treino e Teste
x_train, x_test, y_train, y_test = train_test_split(x, y)

#Criando um Objeto de Regressão Linear
lr = LinearRegression()

#Treine o Modelo
lr.fit(x_train, y_train)

#Calcule o score do modelo
r_sq = lr.score(x, y)
print('Coeficiente de Determinação (R²):', r_sq)

print('Intercepto:', lr.intercept_)

coeff_df = pd.DataFrame(lr.coef_,x.columns,columns=['Coefficient'])
coeff_df

y_pred = lr.predict(x_test)
print('MAE:', metrics.mean_absolute_error(y_test, y_pred))
print('MSE:', metrics.mean_squared_error(y_test, y_pred))
print('RMSE:', np.sqrt(metrics.mean_squared_error(y_test, y_pred)))

"""##Atividades de casa
- Utilize os algortimos de regressão linear e polinomial na mesma base de dados e realize uma análise comparativa.
"""

# Dividindo os dados em treino e teste
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)

# Regressão Linear
lin_reg = LinearRegression()
lin_reg.fit(X_train, y_train)
y_pred_linear = lin_reg.predict(X_test)

# Regressão Polinomial
poly_features = PolynomialFeatures()
X_train_poly = poly_features.fit_transform(X_train)
X_test_poly = poly_features.transform(X_test)

poly_reg = LinearRegression()
poly_reg.fit(X_train_poly, y_train)
y_pred_poly = poly_reg.predict(X_test_poly)

# Avaliando os Modelos
r2_linear = r2_score(y_test, y_pred_linear)
r2_poly = r2_score(y_test, y_pred_poly)

# Mostrando metricas
print(f'R2 linear: {r2_linear:.2f}')
print(f'R2 polinomial: {r2_poly:.2f}')

"""##Referências
- [Regressão Múltipla](https://medium.com/@lamartine_sl/regress%C3%A3o-linear-com-sklearn-modelo-de-previs%C3%A3o-de-custos-com-plano-de-sa%C3%BAde-5e963e590f4c)
- [Insurance](https://github.com/stedy/Machine-Learning-with-R-datasets/blob/master/insurance.csv)
"""