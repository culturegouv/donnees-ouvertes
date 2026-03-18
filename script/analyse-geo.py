import pandas as pd
from csv_detective.format import FormatsManager

fmtm = FormatsManager()

url = "https://object.data.gouv.fr/ministere-culture/POP/joconde.csv"

df = pd.read_csv(url, dtype=str, sep="|", usecols=["coordonnees"])

print(df.loc[
    (df["coordonnees"].notna())
    & (~df["coordonnees"].apply(lambda c: fmtm.formats["latlon_wgs"].func(c)))
])