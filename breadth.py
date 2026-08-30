"""
Proxy diario del BofA Breadth Rule (Hartnett).
Calcula el % de un universo de índices bursátiles globales que cotizan
simultáneamente por encima de su SMA50 y su SMA200.

Esto es una réplica construida con datos públicos (yfinance), NO el dato
oficial de BofA. Sirve para tener una serie diaria comparable, no para
igualar el número exacto que publica Hartnett en su Flow Show.
"""

import os
from datetime import datetime, timezone

import pandas as pd
import yfinance as yf

# Universo de 21 índices, un representante por país/región.
# Elegido para cubrir el grueso de la capitalización bursátil mundial.
TICKERS = {
    "USA": "^GSPC",
    "Eurozona": "^STOXX50E",
    "Reino_Unido": "^FTSE",
    "Alemania": "^GDAXI",
    "Francia": "^FCHI",
    "Espana": "^IBEX",
    "Suiza": "^SSMI",
    "Japon": "^N225",
    "China_onshore": "000001.SS",
    "China_HK": "^HSI",
    "India": "^BSESN",
    "Brasil": "^BVSP",
    "Mexico": "^MXX",
    "Canada": "^GSPTSE",
    "Australia": "^AXJO",
    "Corea_Sur": "^KS11",
    "Taiwan": "^TWII",
    "Indonesia": "^JKSE",
    "Singapur": "^STI",
    "Turquia": "XU100.IS",
    "Argentina": "^MERV",
}

DATA_DIR = "data"
HISTORY_PATH = os.path.join(DATA_DIR, "breadth_history.csv")


def compute_breadth() -> None:
    os.makedirs(DATA_DIR, exist_ok=True)

    rows = []
    above_both = 0
    total = 0

    for country, ticker in TICKERS.items():
        try:
            hist = yf.Ticker(ticker).history(period="400d")
            if hist.empty or len(hist) < 200:
                rows.append({
                    "country": country, "ticker": ticker,
                    "error": "datos insuficientes (<200 sesiones)"
                })
                continue

            close = hist["Close"]
            sma50 = close.rolling(50).mean().iloc[-1]
            sma200 = close.rolling(200).mean().iloc[-1]
            last = close.iloc[-1]
            above = bool((last > sma50) and (last > sma200))

            rows.append({
                "country": country,
                "ticker": ticker,
                "last_close": round(float(last), 2),
                "sma50": round(float(sma50), 2),
                "sma200": round(float(sma200), 2),
                "above_both": above,
            })
            total += 1
            if above:
                above_both += 1

        except Exception as e:
            rows.append({"country": country, "ticker": ticker, "error": str(e)})

    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    pct = round(100 * above_both / total, 1) if total else None

    # Detalle del día (para depurar qué país está o no por encima)
    detail_df = pd.DataFrame(rows)
    detail_df.to_csv(os.path.join(DATA_DIR, f"detail_{date_str}.csv"), index=False)

    # Serie histórica acumulada (esto es lo que lee la tarea programada)
    new_row = pd.DataFrame([{
        "date": date_str,
        "pct_above_both": pct,
        "n_above_both": above_both,
        "n_total": total,
    }])

    if os.path.exists(HISTORY_PATH):
        hist_df = pd.read_csv(HISTORY_PATH)
        # Evita duplicar si se relanza el workflow el mismo día
        hist_df = hist_df[hist_df["date"] != date_str]
        hist_df = pd.concat([hist_df, new_row], ignore_index=True)
    else:
        hist_df = new_row

    hist_df.to_csv(HISTORY_PATH, index=False)
    print(f"{date_str}: {pct}% ({above_both}/{total} índices sobre SMA50 y SMA200)")


if __name__ == "__main__":
    compute_breadth()
