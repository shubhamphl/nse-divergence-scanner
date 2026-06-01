import pandas as pd
from tvDatafeed import TvDatafeed, Interval
from ta.momentum import RSIIndicator

from divergence import (
regular_bullish,
regular_bearish,
hidden_bullish,
hidden_bearish
)

MAX_AGE = 2

tv = TvDatafeed()

symbols = pd.read_csv(
"data/fno_symbols.csv"
)["symbol"].tolist()

bullish = []
bearish = []
hidden_bull = []
hidden_bear = []

for symbol in symbols:

```
try:

    df = tv.get_hist(
        symbol=symbol,
        exchange="NSE",
        interval=Interval.in_1_hour,
        n_bars=300
    )

    df.columns = [
        c.lower()
        for c in df.columns
    ]

    df["rsi"] = RSIIndicator(
        close=df["close"],
        window=14
    ).rsi()

    scans = [
        ("Bullish", regular_bullish(df)),
        ("Bearish", regular_bearish(df)),
        ("Hidden Bullish", hidden_bullish(df)),
        ("Hidden Bearish", hidden_bearish(df))
    ]

    for kind, idx in scans:

        if idx is None:
            continue

        age = len(df) - idx - 1

        if age > MAX_AGE:
            continue

        score = 100 - age * 10

        row = {
            "symbol": symbol,
            "type": kind,
            "age": age,
            "score": score
        }

        if kind == "Bullish":
            bullish.append(row)

        elif kind == "Bearish":
            bearish.append(row)

        elif kind == "Hidden Bullish":
            hidden_bull.append(row)

        else:
            hidden_bear.append(row)

except Exception as e:
    print(symbol, e)
```

pd.DataFrame(
bullish
).sort_values(
"score",
ascending=False
).to_csv(
"docs/bullish.csv",
index=False
)

pd.DataFrame(
bearish
).sort_values(
"score",
ascending=False
).to_csv(
"docs/bearish.csv",
index=False
)

pd.DataFrame(
hidden_bull
).sort_values(
"score",
ascending=False
).to_csv(
"docs/hidden_bullish.csv",
index=False
)

pd.DataFrame(
hidden_bear
).sort_values(
"score",
ascending=False
).to_csv(
"docs/hidden_bearish.csv",
index=False
)

html = """

<html>
<head>
<title>NSE Divergence Scanner</title>
</head>
<body>
<h1>NSE Hourly Divergence Scanner</h1>

<p>
Download CSV files from repository docs folder.
</p>

</body>
</html>
"""

with open(
"docs/index.html",
"w"
) as f:
f.write(html)
