import numpy as np
from scipy.signal import argrelextrema

PIVOT_ORDER = 5

def get_pivot_lows(series):
return argrelextrema(
series.values,
np.less,
order=PIVOT_ORDER
)[0]

def get_pivot_highs(series):
return argrelextrema(
series.values,
np.greater,
order=PIVOT_ORDER
)[0]

def regular_bullish(df):

```
lows = get_pivot_lows(df["low"])

if len(lows) < 2:
    return None

l1 = lows[-2]
l2 = lows[-1]

if (
    df["low"].iloc[l2] < df["low"].iloc[l1]
    and
    df["rsi"].iloc[l2] > df["rsi"].iloc[l1]
):
    return l2

return None
```

def regular_bearish(df):

```
highs = get_pivot_highs(df["high"])

if len(highs) < 2:
    return None

h1 = highs[-2]
h2 = highs[-1]

if (
    df["high"].iloc[h2] > df["high"].iloc[h1]
    and
    df["rsi"].iloc[h2] < df["rsi"].iloc[h1]
):
    return h2

return None
```

def hidden_bullish(df):

```
lows = get_pivot_lows(df["low"])

if len(lows) < 2:
    return None

l1 = lows[-2]
l2 = lows[-1]

if (
    df["low"].iloc[l2] > df["low"].iloc[l1]
    and
    df["rsi"].iloc[l2] < df["rsi"].iloc[l1]
):
    return l2

return None
```

def hidden_bearish(df):

```
highs = get_pivot_highs(df["high"])

if len(highs) < 2:
    return None

h1 = highs[-2]
h2 = highs[-1]

if (
    df["high"].iloc[h2] < df["high"].iloc[h1]
    and
    df["rsi"].iloc[h2] > df["rsi"].iloc[h1]
):
    return h2

return None
```
