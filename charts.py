"""
charts.py  —  All 10 required chart types + 1 bonus
Global Forest Watch Dashboard

 1. chart_pie       — Pie Chart        (proportional distribution of a category)
 2. chart_histogram — Histogram        (frequency distribution of numerical column)
 3. chart_line      — Line Chart       (trends over time / sequence)
 4. chart_bar       — Bar Chart        (compare values across categories)
 5. chart_scatter   — Scatter Plot     (relationship between two numerical variables)
 6. chart_boxplot   — Box Plot         (data spread, median, outliers)
 7. chart_heatmap   — Heatmap          (correlation matrix of features)
 8. chart_area      — Area Chart       (cumulative trends over time)
 9. chart_countplot — Count Plot       (frequency count of categorical variable)
10. chart_violin    — Violin Plot      (distribution and probability density)
 B. chart_bubble    — Bubble Chart     (BONUS)
"""

import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.patches as mpatches
import seaborn as sns
from typing import List, Optional

# ── Palette ───────────────────────────────────────────────────────────────────
BG      = "#0B1E10"
SURFACE = "#112B18"
BORDER  = "#1F4028"
TXT     = "#E8F5E9"
MUTED   = "#7DAA87"

CATS = ["#4CAF50","#FF7043","#FFD54F","#29B6F6","#AB47BC",
        "#EF5350","#26C6DA","#FFCA28","#66BB6A","#FFA726"]


def _fig(w=9, h=4.8):
    fig, ax = plt.subplots(figsize=(w, h))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(SURFACE)
    ax.tick_params(colors=MUTED, labelsize=9)
    ax.xaxis.label.set_color(TXT); ax.yaxis.label.set_color(TXT)
    ax.title.set_color(TXT)
    for s in ax.spines.values(): s.set_edgecolor(BORDER)
    return fig, ax


def _done(fig):
    fig.tight_layout(pad=1.8)
    return fig


def _kfmt(x, _):
    return f"{x/1e6:.1f}M" if abs(x)>=1e6 else (f"{x/1e3:.0f}K" if abs(x)>=1e3 else f"{x:.0f}")


def _empty():
    fig, ax = _fig(7, 3)
    ax.text(0.5, 0.5, "No data for current filter selection",
            ha="center", va="center", color=MUTED, fontsize=11,
            transform=ax.transAxes)
    ax.axis("off")
    return _done(fig)


# ─────────────────────────────────────────────────────────────────────────────
# 1  PIE CHART — proportional distribution of a category
# ─────────────────────────────────────────────────────────────────────────────
def chart_pie(df: pd.DataFrame) -> plt.Figure:
    if df.empty: return _empty()
    data = df.groupby("PrimaryDriver")["TreeCoverLoss_ha"].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(7, 5))
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    wedges, texts, autos = ax.pie(
        data.values, labels=data.index, autopct="%1.1f%%",
        colors=CATS[:len(data)], startangle=130, pctdistance=0.78,
        wedgeprops=dict(linewidth=0.7, edgecolor=BG))
    for t in texts:  t.set_color(TXT);  t.set_fontsize(8.5)
    for a in autos:  a.set_color(BG);   a.set_fontsize(7.5); a.set_fontweight("bold")
    ax.set_title("1 · Pie Chart — Tree Cover Loss Share by Deforestation Driver",
                 color=TXT, fontsize=11, pad=14)
    return _done(fig)


# ─────────────────────────────────────────────────────────────────────────────
# 2  HISTOGRAM — frequency distribution of a numerical column
# ─────────────────────────────────────────────────────────────────────────────
def chart_histogram(df: pd.DataFrame) -> plt.Figure:
    if df.empty: return _empty()
    data = df["TreeCoverLoss_ha"].dropna()
    fig, ax = _fig(8, 4.5)
    ax.hist(data, bins=40, color=CATS[0], edgecolor=BG, linewidth=0.3, alpha=0.92)
    ax.axvline(data.mean(),   color=CATS[1], lw=2.2, ls="--", label=f"Mean  {data.mean():,.0f} ha")
    ax.axvline(data.median(), color=CATS[2], lw=2.2, ls=":",  label=f"Median {data.median():,.0f} ha")
    ax.set_xlabel("Annual Tree Cover Loss (ha)", fontsize=10)
    ax.set_ylabel("Frequency (country-year records)", fontsize=10)
    ax.set_title("2 · Histogram — Frequency Distribution of Annual Tree Cover Loss",
                 color=TXT, fontsize=11)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(_kfmt))
    ax.legend(fontsize=9, facecolor=SURFACE, labelcolor=TXT, edgecolor=BORDER)
    return _done(fig)


# ─────────────────────────────────────────────────────────────────────────────
# 3  LINE CHART — trends over time / sequence
# ─────────────────────────────────────────────────────────────────────────────
def chart_line(df: pd.DataFrame, countries: Optional[List[str]] = None) -> plt.Figure:
    if df.empty: return _empty()
    fig, ax = _fig(9, 4.8)
    if countries:
        for i, c in enumerate(countries[:8]):
            g = df[df["Country"]==c].groupby("Year")["TreeCoverLoss_ha"].sum().reset_index().sort_values("Year")
            ax.plot(g["Year"], g["TreeCoverLoss_ha"]/1e3, label=c,
                    color=CATS[i%len(CATS)], lw=2.2, marker="o", markersize=3.5)
    else:
        g = df.groupby("Year")["TreeCoverLoss_ha"].sum().reset_index().sort_values("Year")
        ax.fill_between(g["Year"], g["TreeCoverLoss_ha"]/1e3, alpha=0.22, color=CATS[1])
        ax.plot(g["Year"], g["TreeCoverLoss_ha"]/1e3, color=CATS[1],
                lw=2.5, marker="o", markersize=4, label="Global total")
    ax.set_xlabel("Year", fontsize=10)
    ax.set_ylabel("Tree Cover Loss (thousand ha)", fontsize=10)
    ax.set_title("3 · Line Chart — Annual Tree Cover Loss Trend Over Time",
                 color=TXT, fontsize=11)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(_kfmt))
    ax.legend(fontsize=9, facecolor=SURFACE, labelcolor=TXT, edgecolor=BORDER, loc="upper left")
    return _done(fig)


# ─────────────────────────────────────────────────────────────────────────────
# 4  BAR CHART — compare values across categories
# ─────────────────────────────────────────────────────────────────────────────
def chart_bar(df: pd.DataFrame, top_n: int = 15) -> plt.Figure:
    if df.empty: return _empty()
    data = df.groupby("Country")["TreeCoverLoss_ha"].sum().nlargest(top_n).sort_values().reset_index()
    fig, ax = _fig(8, 6)
    colors = [CATS[1] if i >= len(data)-3 else CATS[0] for i in range(len(data))]
    bars = ax.barh(data["Country"], data["TreeCoverLoss_ha"]/1e3,
                   color=colors, edgecolor=BG, linewidth=0.3)
    for bar in bars:
        w = bar.get_width()
        ax.text(w*1.01, bar.get_y()+bar.get_height()/2,
                f"{w:,.0f}K", va="center", ha="left", fontsize=7.5, color=MUTED)
    ax.set_xlabel("Total Tree Cover Loss (thousand ha)", fontsize=10)
    ax.set_title(f"4 · Bar Chart — Top {top_n} Countries by Total Tree Cover Loss",
                 color=TXT, fontsize=11)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(_kfmt))
    return _done(fig)


# ─────────────────────────────────────────────────────────────────────────────
# 5  SCATTER PLOT — relationship between two numerical variables
# ─────────────────────────────────────────────────────────────────────────────
def chart_scatter(df: pd.DataFrame) -> plt.Figure:
    if df.empty: return _empty()
    agg = df.groupby(["Country","Biome"]).agg(
        Loss=("TreeCoverLoss_ha","sum"), Carbon=("CarbonLoss_tCO2","sum")).reset_index()
    if agg.empty: return _empty()
    fig, ax = _fig(8, 5)
    for i, (biome, sub) in enumerate(agg.groupby("Biome")):
        ax.scatter(sub["Loss"]/1e3, sub["Carbon"]/1e6, label=biome,
                   color=CATS[i%len(CATS)], s=70, alpha=0.82, edgecolors=BG, linewidths=0.4)
    x, y = agg["Loss"]/1e3, agg["Carbon"]/1e6
    if len(x) > 2:
        m, b = np.polyfit(x, y, 1)
        xp = np.linspace(x.min(), x.max(), 100)
        ax.plot(xp, m*xp+b, "--", color=CATS[2], lw=1.8, alpha=0.85, label="Trend")
    ax.set_xlabel("Total Tree Cover Loss (thousand ha)", fontsize=10)
    ax.set_ylabel("Total Carbon Loss (Mt CO₂)", fontsize=10)
    ax.set_title("5 · Scatter Plot — Tree Cover Loss vs Carbon Emissions by Country",
                 color=TXT, fontsize=11)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(_kfmt))
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(_kfmt))
    ax.legend(fontsize=9, facecolor=SURFACE, labelcolor=TXT, edgecolor=BORDER)
    return _done(fig)


# ─────────────────────────────────────────────────────────────────────────────
# 6  BOX PLOT — data spread, median, and outliers
# ─────────────────────────────────────────────────────────────────────────────
def chart_boxplot(df: pd.DataFrame) -> plt.Figure:
    if df.empty: return _empty()
    biomes = sorted(df["Biome"].dropna().unique())
    data   = [df[df["Biome"]==b]["TreeCoverLoss_ha"].dropna()/1e3 for b in biomes]
    fig, ax = _fig(8, 5)
    bp = ax.boxplot(data, labels=biomes, patch_artist=True,
                    medianprops=dict(color=CATS[2], linewidth=2.2),
                    whiskerprops=dict(color=MUTED, linewidth=1.2),
                    capprops=dict(color=MUTED, linewidth=1.2),
                    flierprops=dict(marker="o", color=CATS[1], markersize=3.5, alpha=0.55))
    for patch, col in zip(bp["boxes"], CATS):
        patch.set_facecolor(col); patch.set_alpha(0.72)
    ax.set_xlabel("Biome Type", fontsize=10)
    ax.set_ylabel("Annual Tree Cover Loss (thousand ha)", fontsize=10)
    ax.set_title("6 · Box Plot — Loss Distribution by Biome: Spread, Median & Outliers",
                 color=TXT, fontsize=11)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(_kfmt))
    return _done(fig)


# ─────────────────────────────────────────────────────────────────────────────
# 7  HEATMAP — correlation matrix of features
# ─────────────────────────────────────────────────────────────────────────────
def chart_heatmap(df: pd.DataFrame) -> plt.Figure:
    if df.empty: return _empty()
    WANT = ["TreeCoverLoss_ha","TreeCoverGain_ha","NetForestChange_ha",
            "FireArea_ha","CarbonLoss_tCO2","TreeCoverPct","DeforestAlerts","LossGainRatio"]
    cols = [c for c in WANT if c in df.columns]
    if len(cols) < 2: return _empty()
    SHORT = {"TreeCoverLoss_ha":"TC Loss","TreeCoverGain_ha":"TC Gain",
             "NetForestChange_ha":"Net Δ","FireArea_ha":"Fire",
             "CarbonLoss_tCO2":"Carbon","TreeCoverPct":"TC %",
             "DeforestAlerts":"Alerts","LossGainRatio":"L/G Ratio"}
    corr = df[cols].corr()
    fig, ax = plt.subplots(figsize=(8, 6))
    fig.patch.set_facecolor(BG); ax.set_facecolor(SURFACE)
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdYlGn_r",
                linewidths=0.5, linecolor=BG, ax=ax,
                annot_kws={"size":9,"color":"white"},
                xticklabels=[SHORT.get(c,c) for c in cols],
                yticklabels=[SHORT.get(c,c) for c in cols],
                cbar_kws={"shrink":0.8})
    ax.set_title("7 · Heatmap — Correlation Matrix of Forest & Environmental Features",
                 color=TXT, fontsize=11, pad=10)
    ax.tick_params(axis="x", colors=MUTED, rotation=30, labelsize=8.5)
    ax.tick_params(axis="y", colors=MUTED, rotation=0,  labelsize=8.5)
    plt.setp(ax.collections[0].colorbar.ax.yaxis.get_ticklabels(), color=MUTED, fontsize=8)
    return _done(fig)


# ─────────────────────────────────────────────────────────────────────────────
# 8  AREA CHART — cumulative trends over time
# ─────────────────────────────────────────────────────────────────────────────
def chart_area(df: pd.DataFrame) -> plt.Figure:
    if df.empty: return _empty()
    g = df.groupby("Year")[["TreeCoverLoss_ha","TreeCoverGain_ha","FireArea_ha"]].sum().reset_index().sort_values("Year")
    fig, ax = _fig(9, 4.8)
    ax.stackplot(g["Year"], g["TreeCoverLoss_ha"]/1e3, g["FireArea_ha"]/1e3,
                 labels=["Tree Cover Loss","Fire Area"], colors=[CATS[1],CATS[2]], alpha=0.82)
    ax.plot(g["Year"], g["TreeCoverGain_ha"]/1e3, color=CATS[0],
            lw=2.5, label="Tree Cover Gain", zorder=5)
    ax.set_xlabel("Year", fontsize=10)
    ax.set_ylabel("Area (thousand ha)", fontsize=10)
    ax.set_title("8 · Area Chart — Cumulative Forest Loss, Fire Area & Gain Over Time",
                 color=TXT, fontsize=11)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(_kfmt))
    ax.legend(fontsize=9, facecolor=SURFACE, labelcolor=TXT, edgecolor=BORDER, loc="upper left")
    return _done(fig)


# ─────────────────────────────────────────────────────────────────────────────
# 9  COUNT PLOT — frequency count of categorical variables
# ─────────────────────────────────────────────────────────────────────────────
def chart_countplot(df: pd.DataFrame) -> plt.Figure:
    if df.empty: return _empty()
    counts = df["PrimaryDriver"].value_counts().reset_index()
    counts.columns = ["Driver","Count"]
    fig, ax = _fig(8, 4.8)
    bars = ax.bar(counts["Driver"], counts["Count"],
                  color=CATS[:len(counts)], edgecolor=BG, linewidth=0.3)
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x()+bar.get_width()/2, h*1.01, f"{int(h):,}",
                ha="center", va="bottom", fontsize=8, color=MUTED)
    ax.set_xlabel("Primary Deforestation Driver", fontsize=10)
    ax.set_ylabel("Number of Country-Year Records", fontsize=10)
    ax.set_title("9 · Count Plot — Frequency Count of Each Deforestation Driver",
                 color=TXT, fontsize=11)
    ax.tick_params(axis="x", rotation=28, labelsize=8.5)
    return _done(fig)


# ─────────────────────────────────────────────────────────────────────────────
# 10  VIOLIN PLOT — distribution and probability density
# ─────────────────────────────────────────────────────────────────────────────
def chart_violin(df: pd.DataFrame) -> plt.Figure:
    if df.empty: return _empty()
    regions = [r for r in sorted(df["Region"].dropna().unique())
               if df[df["Region"]==r].shape[0] > 1]
    data = [np.log1p(df[df["Region"]==r]["TreeCoverLoss_ha"].dropna().values) for r in regions]
    if not data: return _empty()
    fig, ax = _fig(10, 5)
    parts = ax.violinplot(data, positions=range(len(regions)),
                          showmedians=True, showextrema=True)
    for i, pc in enumerate(parts["bodies"]):
        pc.set_facecolor(CATS[i%len(CATS)]); pc.set_alpha(0.75); pc.set_edgecolor(BG)
    parts["cmedians"].set_color(CATS[2]); parts["cmedians"].set_linewidth(2)
    for k in ["cmaxes","cmins","cbars"]:
        parts[k].set_color(MUTED); parts[k].set_linewidth(1)
    ax.set_xticks(range(len(regions)))
    ax.set_xticklabels(regions, rotation=25, ha="right", fontsize=9)
    ax.set_xlabel("Region", fontsize=10)
    ax.set_ylabel("log₁(Tree Cover Loss ha + 1)", fontsize=10)
    ax.set_title("10 · Violin Plot — Loss Distribution & Probability Density by Region",
                 color=TXT, fontsize=11)
    return _done(fig)


# ─────────────────────────────────────────────────────────────────────────────
# BONUS  BUBBLE CHART
# ─────────────────────────────────────────────────────────────────────────────
def chart_bubble(df: pd.DataFrame, top_n: int = 25) -> plt.Figure:
    if df.empty: return _empty()
    agg = df.groupby(["Country","Biome"]).agg(
        Loss=("TreeCoverLoss_ha","sum"), Carbon=("CarbonLoss_tCO2","sum"),
        Alerts=("DeforestAlerts","sum")).reset_index().nlargest(top_n,"Loss")
    if agg.empty: return _empty()
    biomes = sorted(agg["Biome"].unique())
    bc = {b: CATS[i] for i, b in enumerate(biomes)}
    fig, ax = _fig(9, 5.5)
    mx = agg["Alerts"].max() or 1
    for _, row in agg.iterrows():
        ax.scatter(row["Loss"]/1e3, row["Carbon"]/1e6,
                   s=(row["Alerts"]/mx)*1500+40, color=bc[row["Biome"]],
                   alpha=0.72, edgecolors=BG, linewidths=0.5)
        ax.annotate(row["Country"][:4], (row["Loss"]/1e3, row["Carbon"]/1e6),
                    fontsize=6, color=TXT, ha="center", va="center")
    patches = [mpatches.Patch(color=bc[b], label=b) for b in biomes]
    ax.legend(handles=patches, fontsize=9, facecolor=SURFACE, labelcolor=TXT,
              edgecolor=BORDER, title="Biome", title_fontsize=9)
    ax.set_xlabel("Total Tree Cover Loss (thousand ha)", fontsize=10)
    ax.set_ylabel("Total Carbon Loss (Mt CO₂)", fontsize=10)
    ax.set_title(f"Bonus · Bubble Chart — Top {top_n} Countries: Loss vs Carbon  (bubble = alerts)",
                 color=TXT, fontsize=11)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(_kfmt))
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(_kfmt))
    return _done(fig)
