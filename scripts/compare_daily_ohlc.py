"""
EUR/USD daily OHLC comparison:
  A) TwelveData 1day bars (direct API)
  B) Manually built from raw 1h bars using 21:00 UTC day-start (user convention)
  C) Manually built from raw 1h bars using 20:00 UTC day-start (TwelveData convention)

Raw hourly data is fetched WITHOUT any weekend-bar filtering so that Sunday
evening bars (20:00 / 21:00 UTC) that open Monday's session are included.
"""

import os, sys
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
TD_KEY = os.getenv("TD_API_KEY")
if not TD_KEY:
    sys.exit("TD_API_KEY not set")

from twelvedata import TDClient
client = TDClient(apikey=TD_KEY)

# ── Fetch raw data ────────────────────────────────────────────────────────────
print("Fetching 1day bars...")
daily_raw = (
    client.time_series(symbol="EUR/USD", interval="1day",
                       outputsize=20, timezone="UTC")
    .as_pandas()[::-1].reset_index()
)
daily_raw.rename(columns={"datetime": "Date", "open": "Open", "high": "High",
                            "low": "Low", "close": "Close"}, inplace=True)
daily_raw["Date"] = pd.to_datetime(daily_raw["Date"])

print("Fetching 1h bars (raw, no filter)...")
hourly_raw = (
    client.time_series(symbol="EUR/USD", interval="1h",
                       outputsize=500, timezone="UTC")
    .as_pandas()[::-1].reset_index()
)
hourly_raw.rename(columns={"datetime": "Date"}, inplace=True)
hourly_raw["Date"] = pd.to_datetime(hourly_raw["Date"])
for col in ["open", "high", "low", "close"]:
    hourly_raw.rename(columns={col: col.capitalize()}, inplace=True)

print(f"  Daily bars : {len(daily_raw)}")
print(f"  Hourly bars: {len(hourly_raw)}  ({hourly_raw['Date'].min()} -> {hourly_raw['Date'].max()})")

# Drop Saturday entirely from both (full-day weekend)
daily_raw  = daily_raw[daily_raw["Date"].dt.dayofweek != 5]   # Sat=5
hourly_raw = hourly_raw[hourly_raw["Date"].dt.dayofweek != 5] # Sat=5

# ── Helper: build daily OHLC from hourly given a session start hour (UTC) ────
def build_from_hourly(df: pd.DataFrame, start_hour: int) -> pd.DataFrame:
    """
    Group hourly bars into sessions that begin at `start_hour` UTC.

    Session for day D:  (D-1) at start_hour UTC  ...  D at (start_hour-1) UTC

    Shift bars FORWARD by (24 - start_hour) hours so that the first bar of
    day D (which lands on D-1 at start_hour) maps to D 00:00 after normalise.

      e.g. start_hour=20:  Sunday 20:00 + 4h = Monday 00:00  -> label Monday
                           Monday 19:00 + 4h = Monday 23:00  -> label Monday
    """
    h = df.copy()
    h["session_date"] = (h["Date"] + pd.Timedelta(hours=24 - start_hour)).dt.normalize()
    # Drop sessions that land on Saturday or Sunday
    h = h[h["session_date"].dt.dayofweek < 5]
    g = h.groupby("session_date")
    agg = g.agg(
        bar_count=("Open",  "count"),
        Open      =("Open",  "first"),
        High      =("High",  "max"),
        Low       =("Low",   "min"),
        Close     =("Close", "last"),
    ).reset_index().rename(columns={"session_date": "Date"})
    return agg

calc_21 = build_from_hourly(hourly_raw, start_hour=21)   # user convention
calc_20 = build_from_hourly(hourly_raw, start_hour=20)   # TwelveData convention

# ── Filter: last 7 weekday dates present in all three datasets ────────────────
daily_wk = daily_raw[daily_raw["Date"].dt.dayofweek < 5].set_index("Date")
last7_dates = sorted(daily_wk.index)[-7:]

def align(df, dates):
    d = df[df["Date"].isin(dates)].set_index("Date")
    return d

api   = align(daily_raw,  last7_dates)
c21   = align(calc_21,    last7_dates)
c20   = align(calc_20,    last7_dates)

# ── Print comparison ─────────────────────────────────────────────────────────
def pips(a, b):
    return (b - a) * 10_000

HEADER = f"{'Field':<6}  {'API 1day':>10}  {'21:00 calc':>10}  {'diff':>8}  {'20:00 calc':>10}  {'diff':>8}"
SEP    = "-" * len(HEADER)

print()
print("=" * 72)
print("EUR/USD  |  1day API  vs  calc@21:00 UTC  vs  calc@20:00 UTC (TwelveData)")
print("=" * 72)

for date in last7_dates:
    a = api.loc[date] if date in api.index else None
    r21 = c21.loc[date] if date in c21.index else None
    r20 = c20.loc[date] if date in c20.index else None
    bc21 = int(c21.loc[date, "bar_count"]) if r21 is not None else 0
    bc20 = int(c20.loc[date, "bar_count"]) if r20 is not None else 0

    print(f"\n{date.date()}  {date.strftime('%A')}   "
          f"(bars: 21h-start={bc21}, 20h-start={bc20})")
    print(HEADER)
    print(SEP)
    for field in ["Open", "High", "Low", "Close"]:
        av   = a[field]   if a   is not None else float("nan")
        v21  = r21[field] if r21 is not None else float("nan")
        v20  = r20[field] if r20 is not None else float("nan")
        d21  = pips(av, v21)
        d20  = pips(av, v20)
        f21  = " <" if abs(d21) > 2 else ""
        f20  = " <" if abs(d20) > 2 else ""
        print(f"{field:<6}  {av:>10.5f}  {v21:>10.5f}  {d21:>+7.1f}p{f21:<2}  "
              f"{v20:>10.5f}  {d20:>+7.1f}p{f20:<2}")

# ── Summary ───────────────────────────────────────────────────────────────────
print()
print("=" * 72)
print("AVERAGE ABSOLUTE ERROR (pips) across last 7 trading days")
print("=" * 72)
rows_21, rows_20 = [], []
for date in last7_dates:
    if date not in api.index: continue
    a = api.loc[date]
    for field in ["Open", "High", "Low", "Close"]:
        if date in c21.index:
            rows_21.append({"field": field, "err": abs(pips(a[field], c21.loc[date, field]))})
        if date in c20.index:
            rows_20.append({"field": field, "err": abs(pips(a[field], c20.loc[date, field]))})

s21 = pd.DataFrame(rows_21).groupby("field")["err"].mean().rename("21h-start")
s20 = pd.DataFrame(rows_20).groupby("field")["err"].mean().rename("20h-start")
print(pd.concat([s21, s20], axis=1).round(2).to_string())

# ── Show what Sunday evening bars TwelveData returns ─────────────────────────
print()
print("=" * 72)
print("Sunday evening bars returned by TwelveData (raw, unfiltered):")
print("=" * 72)
sun = hourly_raw[hourly_raw["Date"].dt.dayofweek == 6]  # Sunday=6
print(sun[["Date","Open","High","Low","Close"]].to_string(index=False))
