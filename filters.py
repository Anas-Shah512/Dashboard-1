"""
filters.py  —  Data generation, loading, cleaning, filtering & KPIs
Global Forest Watch Dashboard
"""
import os, pandas as pd, numpy as np
import streamlit as st


# ── 1. Dataset generation (no download needed) ────────────────────────────────
def _generate(path: str) -> None:
    np.random.seed(42)
    COUNTRIES = [
        ("Brazil",          "South America",  "Tropical",    420000, 4900000),
        ("Indonesia",       "Asia",           "Tropical",    195000, 1910000),
        ("DR Congo",        "Africa",         "Tropical",    130000, 2340000),
        ("Bolivia",         "South America",  "Tropical",     72000,  680000),
        ("Peru",            "South America",  "Tropical",     61000,  740000),
        ("Colombia",        "South America",  "Tropical",     52000,  600000),
        ("Angola",          "Africa",         "Tropical",     43000,  520000),
        ("Tanzania",        "Africa",         "Tropical",     36000,  390000),
        ("Mozambique",      "Africa",         "Tropical",     31000,  360000),
        ("Paraguay",        "South America",  "Subtropical",  27000,  170000),
        ("Myanmar",         "Asia",           "Tropical",     40000,  290000),
        ("Cambodia",        "Asia",           "Tropical",     18000,  130000),
        ("Laos",            "Asia",           "Tropical",     15000,  160000),
        ("Vietnam",         "Asia",           "Tropical",     12000,  140000),
        ("Malaysia",        "Asia",           "Tropical",     50000,  220000),
        ("Papua New Guinea","Oceania",        "Tropical",     34000,  360000),
        ("Mexico",          "North America",  "Subtropical",  30000,  640000),
        ("Honduras",        "North America",  "Tropical",     15000,   55000),
        ("Nicaragua",       "North America",  "Tropical",     11000,   32000),
        ("Guatemala",       "North America",  "Tropical",     10000,   38000),
        ("Russia",          "Europe/Asia",    "Boreal",       75000, 8090000),
        ("Canada",          "North America",  "Boreal",       55000, 3470000),
        ("United States",   "North America",  "Temperate",    37000, 3100000),
        ("China",           "Asia",           "Temperate",    27000, 2080000),
        ("India",           "Asia",           "Tropical",     15000,  720000),
        ("Australia",       "Oceania",        "Temperate",    24000, 1340000),
        ("Argentina",       "South America",  "Subtropical",  22000,  940000),
        ("Chile",           "South America",  "Temperate",    10000,  180000),
        ("Sweden",          "Europe",         "Boreal",        7000,  280000),
        ("Finland",         "Europe",         "Boreal",        6000,  220000),
        ("Norway",          "Europe",         "Boreal",        5000,  120000),
        ("Germany",         "Europe",         "Temperate",     3500,  114000),
        ("France",          "Europe",         "Temperate",     4200,  170000),
        ("Nigeria",         "Africa",         "Tropical",     29000,  120000),
        ("Ghana",           "Africa",         "Tropical",     16000,   59000),
        ("Cameroon",        "Africa",         "Tropical",     23000,  200000),
        ("Gabon",           "Africa",         "Tropical",     12000,  230000),
        ("Ethiopia",        "Africa",         "Tropical",     18000,  130000),
        ("Spain",           "Europe",         "Temperate",     5000,  185000),
        ("Philippines",     "Asia",           "Tropical",     22000,  100000),
    ]
    BPARAMS = {
        "Tropical":    dict(gr=(0.010,0.025), fire=0.35, carbon=280),
        "Subtropical": dict(gr=(0.007,0.015), fire=0.25, carbon=200),
        "Boreal":      dict(gr=(0.004,0.010), fire=0.15, carbon=120),
        "Temperate":   dict(gr=(0.003,0.008), fire=0.10, carbon=160),
    }
    DRIVERS = ["Agricultural Expansion","Logging","Fire","Urban Expansion",
               "Mining","Infrastructure","Climate/Drought","Unknown"]
    BASE_W  = np.array([0.35,0.20,0.15,0.10,0.08,0.05,0.04,0.03], float)
    YEARS   = list(range(2001, 2024))
    rows    = []
    for name, region, biome, base_loss, forest_km2 in COUNTRIES:
        bp    = BPARAMS[biome]
        gr    = np.random.uniform(*bp["gr"])
        trend = np.linspace(0.80, 1.35, len(YEARS))
        for i, year in enumerate(YEARS):
            loss   = max(base_loss * gr * trend[i] * 10 * np.random.normal(1,.10), 100)
            gain   = max(loss * np.random.uniform(0.10,0.35), 50)
            fire   = loss*(np.random.uniform(0.15,0.55) if np.random.random()<bp["fire"] else np.random.uniform(0.01,0.08))
            carbon = loss * bp["carbon"] * np.random.normal(1,.07)
            w = BASE_W.copy()
            if biome=="Tropical":   w[0]=0.50
            elif biome=="Boreal":   w[1]=0.38; w[0]=0.18
            w /= w.sum()
            driver   = np.random.choice(DRIVERS, p=w)
            tc_pct   = max(min(forest_km2/(forest_km2+base_loss*0.5)*100 - i*0.25 + np.random.normal(0,1.2),97),3)
            alerts   = int(loss * np.random.uniform(0.9,2.2))
            rows.append(dict(
                Country=name, Region=region, Biome=biome, Year=year,
                TreeCoverLoss_ha=round(loss,1), TreeCoverGain_ha=round(gain,1),
                NetForestChange_ha=round(gain-loss,1), FireArea_ha=round(fire,1),
                CarbonLoss_tCO2=round(carbon,1), TreeCoverPct=round(tc_pct,2),
                PrimaryDriver=driver, DeforestAlerts=alerts, ForestArea_km2=forest_km2,
            ))
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    pd.DataFrame(rows).to_csv(path, index=False)


# ── 2. Load & clean ───────────────────────────────────────────────────────────
@st.cache_data(show_spinner="🌿 Loading dataset…")
def load_data(path="data/GlobalForestWatch_TreeCoverLoss.csv") -> pd.DataFrame:
    if not os.path.exists(path):
        _generate(path)
    df = pd.read_csv(path, low_memory=False)
    df.columns = [c.strip() for c in df.columns]
    for col in ["TreeCoverLoss_ha","TreeCoverGain_ha","NetForestChange_ha",
                "FireArea_ha","CarbonLoss_tCO2","TreeCoverPct",
                "DeforestAlerts","ForestArea_km2","Year"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    df.dropna(subset=["Country","Year","TreeCoverLoss_ha"], inplace=True)
    df["LossGainRatio"]    = (df["TreeCoverLoss_ha"] / df["TreeCoverGain_ha"].replace(0,np.nan)).round(3)
    df["CarbonLoss_MtCO2"] = (df["CarbonLoss_tCO2"] / 1e6).round(5)
    return df.reset_index(drop=True)


# ── 3. Apply all 6 filters ────────────────────────────────────────────────────
def apply_filters(df, year_range, region, biomes, countries, loss_range, search):
    f = df.copy()
    f = f[(f["Year"]>=year_range[0]) & (f["Year"]<=year_range[1])]          # F1 date/time
    if region != "All":                                                        # F2 category
        f = f[f["Region"]==region]
    if biomes:                                                                 # F3 multi-select
        f = f[f["Biome"].isin(biomes)]
    if countries:                                                              # F4 multi-select
        f = f[f["Country"].isin(countries)]
    f = f[(f["TreeCoverLoss_ha"]>=loss_range[0]) &
          (f["TreeCoverLoss_ha"]<=loss_range[1])]                            # F5 numerical range
    if search.strip():                                                         # F6 text search
        f = f[f["Country"].str.contains(search.strip(), case=False, na=False)]
    return f.reset_index(drop=True)


# ── 4. KPIs ───────────────────────────────────────────────────────────────────
def compute_kpis(df):
    if df.empty:
        return dict(records=0, loss="0", ann="0", carbon="0", cover="0", country="—", driver="—", alerts="0")
    return dict(
        records = f"{len(df):,}",
        loss    = f"{df['TreeCoverLoss_ha'].sum()/1e6:.2f} M ha",
        ann     = f"{df.groupby('Year')['TreeCoverLoss_ha'].sum().mean()/1e3:.0f} K ha",
        carbon  = f"{df['CarbonLoss_tCO2'].sum()/1e9:.2f} Gt",
        cover   = f"{df['TreeCoverPct'].mean():.1f} %",
        country = df.groupby("Country")["TreeCoverLoss_ha"].sum().idxmax(),
        driver  = df["PrimaryDriver"].value_counts().idxmax(),
        alerts  = f"{int(df['DeforestAlerts'].sum()):,}",
    )
