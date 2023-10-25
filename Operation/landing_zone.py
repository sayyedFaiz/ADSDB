import datetime
import pandas as pd

def ingestinTime():
    now = datetime.datetime.now()
    now = now.strftime("%Y_%m_%d_%H_%M_%S")
    return now

barca_rent = pd.read_csv(
    "C:/Users/sayye/OneDrive/Desktop/college/PG/UPC/ADSDB/landing/temporal/Barcelona_rent_price.csv"
)
years = {2018, 2019, 2020}

for year in years:
  rent_df = barca_rent.loc[barca_rent['Year'] == year]
  rent_df.reset_index(drop=True, inplace=True)
  rent_df.to_csv(f'C:/Users/sayye/OneDrive/Desktop/college/PG/UPC/ADSDB/landing/Persistent/rents_{year}_{ingestinTime()}.csv', index=False)



income_2018 = pd.read_csv(
    "C:/Users/sayye/OneDrive/Desktop/college/PG/UPC/ADSDB/landing/temporal/2018_atles_renda_bruta_persona.csv"
)
income_2019 = pd.read_csv(
    "C:/Users/sayye/OneDrive/Desktop/college/PG/UPC/ADSDB/landing/temporal/2019_atles_renda_bruta_persona.csv"
)
income_2020 = pd.read_csv(
    "C:/Users/sayye/OneDrive/Desktop/college/PG/UPC/ADSDB/landing/temporal/2020_atles_renda_bruta_persona.csv"
)

income_2018.to_csv(
    f"C:/Users/sayye/OneDrive/Desktop/college/PG/UPC/ADSDB/landing/Persistent/income_2018_{ingestinTime()}.csv",
    index=False,
)
income_2019.to_csv(
    f"C:/Users/sayye/OneDrive/Desktop/college/PG/UPC/ADSDB/landing/Persistent/income_2019_{ingestinTime()}.csv",
    index=False,
)
income_2020.to_csv(
    f"C:/Users/sayye/OneDrive/Desktop/college/PG/UPC/ADSDB/landing/Persistent/income_2020_{ingestinTime()}.csv",
    index=False,
)
