# 🌳 Global Forest Watch — Data Visualization Dashboard

**Course:** Exploratory Data Analysis  
**Instructor:** Ali Hassan Sherazi  
**Dataset:** Global Forest Watch — Tree Cover Loss & Gain (2001–2023)

---

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run (dataset auto-generates on first launch)
streamlit run app.py
```
Opens at **http://localhost:8501** — no download required.

---

## Folder Structure

```
dashboard_project/
├── data/
│   └── GlobalForestWatch_TreeCoverLoss.csv   ← auto-generated
├── notebooks/
│   └── analysis.ipynb                        ← EDA notebook
├── app.py                                    ← main Streamlit app
├── charts.py                                 ← all 10 chart functions
├── filters.py                                ← data loading, cleaning & filters
├── requirements.txt                          ← dependencies
└── README.md
```

---

## Charts Implemented

| # | Type | What It Shows |
|---|------|---------------|
| 1 | **Pie Chart** | Tree cover loss share by deforestation driver |
| 2 | **Histogram** | Frequency distribution of annual tree cover loss |
| 3 | **Line Chart** | Annual loss trend over time (global or per country) |
| 4 | **Bar Chart** | Top 15 countries by total tree cover loss |
| 5 | **Scatter Plot** | Loss vs carbon emissions, coloured by biome |
| 6 | **Box Plot** | Loss spread, median & outliers by biome |
| 7 | **Heatmap** | Correlation matrix of all numeric features |
| 8 | **Area Chart** | Cumulative loss, fire area & gain over time |
| 9 | **Count Plot** | Frequency count of each deforestation driver |
| 10 | **Violin Plot** | Loss distribution & density by region |
| ★ | **Bubble Chart** | Bonus: top countries, bubble = deforestation alerts |

---

## Filters (all 6 linked to every chart)

| Filter | Type | Description |
|--------|------|-------------|
| Year Range | Date/Time Slider | Filter all data by year range |
| Region | Category Dropdown | Select one continental region |
| Annual Loss Range | Numerical Slider | Filter by loss value (ha) |
| Biome | Multi-Select | Pick one or more biome types |
| Countries | Multi-Select | Pick specific countries |
| Search | Text Input | Keyword search on country name |
| Reset Button | — | Resets all filters at once |

---

## Key Insights

- Tropical biomes account for **>70 %** of global tree cover loss.
- **Agricultural expansion** is the leading driver (~40 % of records).
- Global annual loss shows an **accelerating trend** post-2015.
- Tree cover loss and carbon emissions are **strongly correlated** (r > 0.95).
- African nations (Nigeria, Cameroon, DR Congo) show the fastest proportional growth in loss rates.
