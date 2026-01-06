# AI Intensity Analysis

This repository contains a Python script for analyzing and visualizing AI intensity data.

## Files

- `plot_ai_intensity_paper.py` - Main script for generating AI intensity visualizations
- `标注结果进展/王哲1027结果反馈-900篇文章LLM标注结果/统计结果/02/02.xlsx` - Sample data file

## Requirements

Install the required Python packages:

```bash
pip install pandas openpyxl xlrd matplotlib scipy numpy
```

## Usage

Run the script with the following command:

```bash
python plot_ai_intensity_paper.py --input "标注结果进展/王哲1027结果反馈-900篇文章LLM标注结果/统计结果/02/02.xlsx" --outdir outputs_figs --bins 20
```

### Parameters

- `--input`: Path to the input Excel file (.xls, .xlsx, or .csv)
- `--outdir`: Output directory for generated figures (default: `outputs_figs`)
- `--sheet`: Excel sheet number or name (default: 0)
- `--bins`: Number of bins for histogram (default: 20)

## Output

The script generates the following files:

1. **ai_intensity_boxplot_by_result.png/.pdf** - Boxplot comparing AI_intensity values grouped by Result (0 vs 1)
2. **ai_intensity_hist_with_normal.png/.pdf** - Histogram of AI_intensity distribution with normal curve fit

## Data Format

The input Excel file must contain the following columns:

- `AI_intensity` - Numeric values between 0 and 1
- `Result` - Binary values (0 or 1)

## Example Output

The script produces publication-quality figures with:
- High resolution (300 DPI for saved figures)
- Professional styling (minimal design, no top/right spines)
- Statistical information (mean, standard deviation, sample counts)
- Both PNG and PDF formats for flexibility
