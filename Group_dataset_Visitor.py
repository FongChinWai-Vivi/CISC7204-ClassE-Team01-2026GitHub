import pandas as pd
from pathlib import Path

folder = Path(r"C:\Users\user\Documents\cisc7204\Project\Github\CISC7204-ClassE-Team01-2026GitHub\Dataset")
markets = ["CN", "HK", "KR", "TW"]

#data cleaning for Visitors_Arrival_byOnday_Overnight
frames = []
for m in markets:
    f = folder / f"Visitors_Arrival_byOnday_Overnight_{m}.csv"  
    d = pd.read_csv(f, encoding="utf-8-sig")
    d.columns = d.columns.str.strip()
    d["Market"] = m
    frames.append(d)

df = pd.concat(frames, ignore_index=True)
print(df.shape)

keep = ["Year", "Quarter", "Month", "Market", "SameDay", "OverNight"]
df = df[keep].copy()

df["Year"] = pd.to_numeric(df["Year"], errors="coerce")

for c in ["SameDay", "OverNight"]:
    df[c] = (df[c].astype(str)
                  .str.replace(",", "", regex=False)
                  .str.strip()
                  .replace({"-": None, "": None, "nan": None}))
    df[c] = pd.to_numeric(df[c], errors="coerce")

calc = (df["Month"] - 1) // 3 + 1
df["Quarter"] = df["Quarter"].fillna(calc)

print(df.isna().sum())

df = df.dropna(subset=["Year", "Quarter", "Month"])
df["Year"] = df["Year"].astype(int)
df["Quarter"] = df["Quarter"].astype(int)
df["Month"] = df["Month"].astype(int)

df = df[df["Year"] >= 2023]
print(df["Year"].value_counts().sort_index())

summary = (df.groupby(["Year","Quarter","Month"], as_index=False)[["SameDay", "OverNight"]]
             .sum(min_count=1))
summary["Total"] = summary["SameDay"] + summary["OverNight"]

by_market = (df.groupby(["Year","Quarter", "Month", "Market"], as_index=False)[["SameDay", "OverNight"]]
               .sum(min_count=1))

print(df["Quarter"].isna().sum())
print(f"Quarter",df["Quarter"].unique())
print(summary.groupby("Year").size())            
print(df.duplicated(["Year","Month","Market"]).sum())   
print(df.groupby("Market")[["SameDay","OverNight"]].sum())

summary.to_csv(folder / "visitors_2023_2026_summary.csv", index=False, encoding="utf-8-sig")
by_market.to_csv(folder / "visitors_2023_2026_by_market_summary.csv", index=False, encoding="utf-8-sig")

# data cleaning for Hotel_occ_byHotelStar
path_hotel = r"C:\Users\user\Documents\cisc7204\Project\Github\CISC7204-ClassE-Team01-2026GitHub\Dataset\Hotel_Arr_byHotelStar.csv"
df1 = pd.read_csv(path_hotel, encoding="utf-8-sig")

df1.columns = df1.columns.str.strip().str.replace(r"\s+", "_", regex=True)
print(df1.columns.tolist())


df1["Year"] = pd.to_numeric(df1["Year"], errors="coerce")
df1["Month"] = pd.to_numeric(df1["Month"], errors="coerce")

df1["Number_of_guests"] = (df1["Number_of_guests"].astype(str)
                          .str.replace(",", "", regex=False).str.strip()
                          .replace({"-": None, "": None, "nan": None}))
df1["Number_of_guests"] = pd.to_numeric(df1["Number_of_guests"], errors="coerce")

df1 = df1.dropna(subset=["Year", "Month"])
df1[["Year", "Month"]] = df1[["Year", "Month"]].astype(int)

for c in ["Source_Markets", "Hotel_Establishments"]:
    df1[c] = df1[c].astype(str).str.strip()

df1 = df1[df1["Year"] >= 2023]
df1 = df1.drop(columns=["Quarter","Source_Markets"])
df1 = df1.drop_duplicates()

df1["Quarter"] = ((df1["Month"] - 1) // 3 + 1).astype(int)

summary = (df1.groupby(["Year", "Quarter", "Month","Hotel_Establishments"], as_index=False)
                ["Number_of_guests"].sum(min_count=1))

print(summary.groupby("Year").size())              
print(summary.duplicated(["Year", "Month", "Hotel_Establishments"]).sum())  

summary.to_csv(folder / "hotel_Arrival_byHotelStar_summary.csv", index=False, encoding="utf-8-sig")

#data cleaning for hotel occ total
path_hotel_occ = r"C:\Users\user\Documents\cisc7204\Project\Github\CISC7204-ClassE-Team01-2026GitHub\Dataset\Hotel_occ_total.csv"
df2 = pd.read_csv(path_hotel_occ, encoding="utf-8-sig")
df2.columns = df2.columns.str.strip().str.replace(r"\s+", "_", regex=True)

df2 = df2[df2["Year"] >= 2023]
hotel_occ = df2.copy()

hotel_occ["Year"] = pd.to_numeric(hotel_occ["Year"], errors="coerce")
hotel_occ["Month"] = pd.to_numeric(hotel_occ["Month"], errors="coerce")

hotel_occ["Occupancy_rate"] = (hotel_occ["Occupancy_rate"].astype(str)
                               .str.replace("%", "", regex=False)
                               .str.replace(",", "", regex=False)
                               .str.strip()
                               .replace({"-": None, "": None, "nan": None}))
hotel_occ["Occupancy_rate"] = pd.to_numeric(hotel_occ["Occupancy_rate"], errors="coerce")

hotel_occ = hotel_occ.dropna(subset=["Year", "Month"])
hotel_occ[["Year", "Month"]] = hotel_occ[["Year", "Month"]].astype(int)

hotel_occ["Quarter"] = ((hotel_occ["Month"] - 1) // 3 + 1).astype(int)

hotel_occ = hotel_occ[["Year", "Quarter", "Month", "Occupancy_rate"]].drop_duplicates()
hotel_occ = hotel_occ.sort_values(["Year", "Quarter","Month"]).reset_index(drop=True)

hotel_occ.to_csv(folder / "hotel_occ_total_summary.csv", index=False, encoding="utf-8-sig")