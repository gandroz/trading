
from data import Data
import numpy as np
from bokeh.plotting import figure
from bokeh.io import export_png
from bokeh.palettes import Category10_10


def plot(df, filename=None, bollinger=None, ema=None, sma=None, 
         open_positions=None, close_positions=None):
    _df = df.copy()

    # plot candles
    inc = _df.Close > _df.Open
    dec = _df.Open > _df.Close

    w = 7*3600*2500

    p = figure(x_axis_type="datetime", plot_width=800, plot_height=500)
    p.segment(_df.index, _df.Low, _df.index, np.min([_df.Open, _df.Close], axis=0), color="black")
    p.segment(_df.index, np.max([_df.Open, _df.Close], axis=0), _df.index, _df.High, color="black")
    p.vbar(_df.index[inc], w, _df.Open[inc], _df.Close[inc], fill_alpha=0.7, fill_color="#3D9970", line_color="#3D9970")
    p.vbar(_df.index[dec], w, _df.Open[dec], _df.Close[dec], fill_alpha=0.7, fill_color="#FF4136", line_color="#FF4136")

    line_count = 0

    # plot sma
    if sma is not None:
        if not isinstance(sma, list): sma=[sma]
        for d in sma:
            _df[f"SMA{d}"] = _df.Close.rolling(window=d).mean()
            p.line(_df.index, _df[f"SMA{d}"], line_color=Category10_10[line_count], line_width=2)
            line_count += 1
            line_count = line_count % 10

    # plot ema
    if ema is not None:
        if not isinstance(ema, list): ema=[ema]
        for d in ema:
            _df[f"EMA{d}"] = _df.Close.ewm(span=d, adjust=False).mean()
            p.line(_df.index, _df[f"EMA{d}"], line_color=Category10_10[line_count], line_width=2)
            line_count += 1
            line_count = line_count % 10
    
    # plot Bollinger
    if bollinger is not None:
        _df[f"StdEMAbol{bollinger}"] = _df.Close.ewm(span=bollinger, adjust=False).std()
        _df[f"EMAbol{bollinger}"] = _df.Close.ewm(span=bollinger, adjust=False).mean()
        p.line(_df.index, _df[f"EMAbol{bollinger}"] + _df[f"StdEMAbol{bollinger}"], line_color=Category10_10[line_count], line_width=2)
        p.line(_df.index, _df[f"EMAbol{bollinger}"] - _df[f"StdEMAbol{bollinger}"], line_color=Category10_10[line_count], line_width=2)
        line_count += 1
        line_count = line_count % 10

    for index, val in close_positions.High.items():
        p.inverted_triangle(index, val*1.04, size=10, fill_color="red", line_alpha=0)
    for index, val in open_positions.Low.items():
        p.triangle(index, val*0.96, size=10, fill_color="green", line_alpha=0)
    
    _filename = filename or f"/home/guillaume/src/trading/data/res.png"
    # p.background_fill_color = None
    # p.border_fill_color = None
    export_png(p, filename=_filename)


if __name__ == "__main__":
    data = Data()
    data.read()
    plot(data.df["AAPL"], ema=20)
