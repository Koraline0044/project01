# -*- coding: utf-8 -*-
"""
plot_ai_intensity_paper.py

输出：
- ai_intensity_boxplot_by_result.(png/pdf)
- ai_intensity_hist_with_normal.(png/pdf)

运行：
python plot_ai_intensity_paper.py --input 02.xls --outdir outputs_figs --bins 20
"""

import os
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy  # 只是为了保证scipy环境，非必须


def read_table(path: str, sheet=0) -> pd.DataFrame:
    if path.lower().endswith(".csv"):
        return pd.read_csv(path)
    try:
        return pd.read_excel(path, sheet_name=sheet)
    except (ImportError, ValueError, KeyError):
        try:
            return pd.read_excel(path, sheet_name=sheet, engine="xlrd")
        except (ImportError, ValueError, KeyError):
            return pd.read_excel(path, sheet_name=sheet, engine="openpyxl")


def set_paper_style():
    """更接近论文排版的 rcParams（不手动指定颜色）。"""
    plt.rcParams.update({
        "figure.dpi": 120,
        "savefig.dpi": 300,
        "font.size": 10,
        "axes.labelsize": 10,
        "axes.titlesize": 10,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "legend.fontsize": 9,
        "axes.linewidth": 0.8,
        "xtick.major.width": 0.8,
        "ytick.major.width": 0.8,
        "xtick.major.size": 3,
        "ytick.major.size": 3,
    })


def despine(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def normal_pdf(x: np.ndarray, mu: float, sigma: float) -> np.ndarray:
    return (1.0 / (sigma * np.sqrt(2.0 * np.pi))) * np.exp(-0.5 * ((x - mu) / sigma) ** 2)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True, help="输入表：02.xls / .xlsx / .csv")
    p.add_argument("--outdir", default="outputs_figs", help="输出目录")
    p.add_argument("--sheet", default=0, help="Excel sheet（默认0）")
    p.add_argument("--bins", type=int, default=20, help="直方图 bins（默认20）")
    args = p.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    set_paper_style()

    df = read_table(args.input, sheet=args.sheet)
    need = ["AI_intensity", "Result"]
    miss = [c for c in need if c not in df.columns]
    if miss:
        raise ValueError(f"缺少必要列：{miss}")

    df = df.copy()
    df["AI_intensity"] = pd.to_numeric(df["AI_intensity"], errors="coerce")
    df["Result"] = pd.to_numeric(df["Result"], errors="coerce")
    df = df.dropna(subset=["AI_intensity", "Result"])

    # =========================
    # 1) 箱线图：按 Result 分组
    # =========================
    data0 = df.loc[df["Result"] == 0, "AI_intensity"].values.astype(float)
    data1 = df.loc[df["Result"] == 1, "AI_intensity"].values.astype(float)

    n0, n1 = len(data0), len(data1)

    # 单栏论文常用宽度：~3.35in（≈85mm），这里略放大便于阅读
    fig, ax = plt.subplots(figsize=(4.2, 3.0), dpi=120)

    ax.boxplot(
        [data0, data1],
        tick_labels=[f"Result=0\n(n={n0})", f"Result=1\n(n={n1})"],
        showmeans=True,
        meanline=True,
        widths=0.55,
        whis=1.5,
        showfliers=True,
    )

    ax.set_ylabel("AI_intensity")
    ax.set_ylim(0, 1.0)
    ax.grid(axis="y", linestyle="--", linewidth=0.6, alpha=0.35)
    despine(ax)
    fig.tight_layout()

    fig.savefig(os.path.join(args.outdir, "ai_intensity_boxplot_by_result.png"), bbox_inches="tight")
    fig.savefig(os.path.join(args.outdir, "ai_intensity_boxplot_by_result.pdf"), bbox_inches="tight")
    plt.close(fig)

    # =========================
    # 2) 直方图：总体分布 + 正态拟合曲线
    # =========================
    data = df["AI_intensity"].values.astype(float)
    n = len(data)

    # 在 0~1 范围内固定分箱，避免极端值影响边界
    bins = args.bins
    counts, edges = np.histogram(data, bins=bins, range=(0, 1))
    bin_width = edges[1] - edges[0]

    mu = float(np.mean(data))
    sigma = float(np.std(data, ddof=1)) if n > 1 else 0.0

    fig, ax = plt.subplots(figsize=(4.2, 3.0), dpi=120)

    # 柱间留缝：rwidth < 1；alpha 让曲线更清晰（不指定颜色）
    ax.hist(
        data,
        bins=bins,
        range=(0, 1),
        rwidth=0.92,     # 柱子间隔（可微调 0.88~0.95）
        alpha=0.85,
        label="Histogram",
    )

    # 正态曲线按"计数尺度"缩放：pdf * n * bin_width
    if sigma > 0:
        x = np.linspace(0, 1, 400)
        y = normal_pdf(x, mu, sigma) * n * bin_width
        ax.plot(x, y, linestyle="--", linewidth=2.0, label="Normal fit")
        ax.text(
            0.02, 0.98,
            f"$\\mu$={mu:.3f}, $\\sigma$={sigma:.3f}, n={n}",
            transform=ax.transAxes,
            ha="left", va="top"
        )

    ax.set_xlabel("AI_intensity")
    ax.set_ylabel("Count")
    ax.set_xlim(0, 1.0)
    ax.grid(axis="y", linestyle="--", linewidth=0.6, alpha=0.35)
    ax.legend(frameon=False, loc="upper left")
    despine(ax)
    fig.tight_layout()

    fig.savefig(os.path.join(args.outdir, "ai_intensity_hist_with_normal.png"), bbox_inches="tight")
    fig.savefig(os.path.join(args.outdir, "ai_intensity_hist_with_normal.pdf"), bbox_inches="tight")
    plt.close(fig)

    print("✅ 已输出：")
    print(" - ai_intensity_boxplot_by_result.(png/pdf)")
    print(" - ai_intensity_hist_with_normal.(png/pdf)")
    print("输出目录：", args.outdir)


if __name__ == "__main__":
    main()
