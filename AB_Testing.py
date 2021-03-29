import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import shapiro
import scipy.stats as stats

df_control = pd.read_excel("dataset/ab_testing_data.xlsx", sheet_name="Control Group")
df_test = pd.read_excel("dataset/ab_testing_data.xlsx", sheet_name="Test Group")

df_test.head()
df_control.head()


# Aykırı değerler için eşik değeri belirleme


def outlier_thresholds(dataframe, variable, low_quantile=0.05, up_quantile=0.95):
    quantile_one = dataframe[variable].quantile(low_quantile)
    quantile_three = dataframe[variable].quantile(up_quantile)
    interquantile_range = quantile_three - quantile_one
    up_limit = quantile_three + 1.5 * interquantile_range
    low_limit = quantile_one - 1.5 * interquantile_range
    return low_limit, up_limit


# Değişkende herhangi bir aykırı değer olup olmadığını kontrol ediyor.
def has_outliers(dataframe, numeric_columns):
    for col in numeric_columns:
        low_limit, up_limit = outlier_thresholds(dataframe, col)
        if dataframe[(dataframe[col] > up_limit) | (dataframe[col] < low_limit)].any(axis=None):
            number_of_outliers = dataframe[(dataframe[col] > up_limit) | (dataframe[col] < low_limit)].shape[0]
            print(col, " : ", number_of_outliers, "outliers")


# Kontrol Grup için aykırı değer olup olmadığı kontrol edildi.
for var in df_control:
    print(var, "has ", has_outliers(df_control, [var]), "Outliers")

# Test Grup için aykırı değer olup olmadığı kontrol edildi.
for var in df_test:
    print(var, "has ", has_outliers(df_test, [var]), "Outliers")

#################################
# Soru 1
#################################
# Bu A / B testinin hipotezini nasıl tanımlarsınız?
# H0 : Kontrol ve test grupları arasında ortalama satın alma sayısı bakımından  istatistiksel olarak farklılık yoktur.
# H1 : Kontrol ve test grupları arasında ortalama satın alma sayısı bakımından  istatistiksel olarak farklılık vardır.


group_a = df_control["Purchase"]
group_b = df_test["Purchase"]

############################
# 1. Varsayım Kontrolü
############################

# 1.1 Normallik Varsayımı
# 1.2 Varyans Homojenliği


############################
# 1.1 Normallik Varsayımı
############################

# H0: Normal dağılım varsayımı sağlanmaktadır.
# H1: Normal dağılım varsayımı sağlanmamaktadır.

test_istatistigi, pvalue = shapiro(group_a)
print('Test İstatistiği = %.4f, p-değeri = %.4f' % (test_istatistigi, pvalue))

pvalue < 0.05
# p değeri > 0.05 olduğu için H0 red edilemez. Yani veri normal dağılmaktadır.

test_istatistigi, pvalue = shapiro(group_a)
print('Test İstatistiği = %.4f, p-değeri = %.4f' % (test_istatistigi, pvalue))

pvalue < 0.05
# p değeri > 0.05 olduğu için H0 red edilemez. Yani veri normal dağılmaktadır


############################
# 1.2 Varyans Homojenligi Varsayımı
############################

# H0: Varyanslar Homojendir
# H1: Varyanslar Homojen Değildir

from scipy import stats

test_istatistigi, pvalue = stats.levene(group_a,
                                        group_b)
print('Test İstatistiği = %.4f, p-değeri = %.4f' % (test_istatistigi, pvalue))

pvalue < 0.05
# p değeri > 0.05 olduğu için H0 red edilemez. Yani varyans homojenliği sağlanmış oldu.

# Test İstatistiği
# H0 : Kontrol ve test grupları arasında ortalama satın alma sayısı bakımından  istatistiksel olarak farklılık yoktur.
# H1 : Kontrol ve test grupları arasında ortalama satın alma sayısı bakımından  istatistiksel olarak farklılık vardır.

test_istatistigi, pvalue = stats.ttest_ind(group_a,
                                           group_b,
                                           equal_var=True)
print('Test İstatistiği = %.4f, p-değeri = %.4f' % (test_istatistigi, pvalue))

pvalue < 0.05
# p değeri > 0.05 olduğu için H0 red edilemez.
# Yani kontrol ve test grupları arasında ortalama satın alma sayısı bakımından  istatistiksel olarak farklılık yoktur.


# İstatistiksel olarak anlamlı sonuçlar çıkarabilir miyiz?

# Kontrol grubu ve test grupları arasında istatistiksel olarak anlamlı bir farklılık yoktur.
# İki grup birbirine benzemektedir.

# Hangi testi kullandınız? Neden?

# Normallik varsayımı ve varyans homojenlik varsayımı sağlandığı için 2 Bağımsız Örneklem Ortalama T Testi kullanildi.
# İki bağımsız değişken nicel ve ölçme düzeyleri orandır.

# Soru 2'ye verdiğiniz cevaba göre, müşteriye tavsiyeniz nedir?

# İki yöntemden biri seçilebilir. Tıklama başına hangi method'a göre daha az ücret ödüyorsak o method seçilebilir.
# Etkileşim, kazanç ve dönüşüm oranlarındaki farklılıklar değerlendirilip hangi yöntemin daha kazançlı olduğunu
# tespit edebiliriz.
# Test 1 aylık bir test ve gözlem sayısı az olduğu için veri toplama süreci uzatılabilir.



