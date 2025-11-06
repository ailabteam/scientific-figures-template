# Professional Scientific Figures Template

This repository provides a Python-based toolkit for generating high-quality, publication-ready figures for scientific papers, conferences, and journals. Built upon Matplotlib and Seaborn, the templates are designed to produce visuals that are not only accurate but also aesthetically pleasing, consistent, and professional.

## Table of Contents

- [Core Philosophy](#core-philosophy)
- [Setup and Installation](#setup-and-installation)
- [Directory Structure](#directory-structure)
- [How to Use](#how-to-use)
- [Figure Gallery & Use Cases](#figure-gallery--use-cases)
  - [1. Line Plot](#1-line-plot)
  - [2. Grouped Bar Chart](#2-grouped-bar-chart)
  - [3. Heatmap](#3-heatmap)
  - [4. Distribution Plot (Histogram/KDE)](#4-distribution-plot-histogramkde)
  - [5. Box & Violin Plot](#5-box--violin-plot)
  - [6. Plots with Error Bars](#6-plots-with-error-bars)
  - [7. Subplots (Compound Figures)](#7-subplots-compound-figures)
  - [8. Contour Plot](#8-contour-plot)
  - [9. t-SNE Visualization](#9-t-sne-visualization)
  - [10. Dual-Axis Plot](#10-dual-axis-plot)
  - [11. Stacked Bar Chart](#11-stacked-bar-chart)
- [Customizing the Style](#customizing-the-style)
- [Contributing](#contributing)

## Core Philosophy

- **Consistency:** Ensures all figures in a publication share a uniform style (font, size, colors).
- **High Quality:** Automatically saves figures in vector format (`.pdf`) at high resolution (600 DPI), guaranteeing sharpness in print and digital formats.
- **Reusability:** Easily generate plots for new datasets without rewriting visualization code from scratch.
- **Best Practices:** Templates are built on effective data visualization principles, helping to avoid common pitfalls.

## Setup and Installation

This project uses `conda` for environment management to ensure reproducibility.

1.  **Create the Conda Environment:**
    Create a new environment named `pubfigures` from the `environment.yml` file.
    ```bash
    conda env create -f environment.yml
    ```
2.  **Activate the Environment:**
    Before running any script, activate the newly created environment.
    ```bash
    conda activate pubfigures
    ```

## Directory Structure

```
.
├── data/                 # Contains sample data files (.csv)
├── examples/             # Contains example scripts for generating each plot type
├── figures/              # Default output directory for generated figures
├── src/                  # Source code for the plotting templates
│   ├── publication_style.py  # Master style file defining the global look and feel
│   └── plot_templates.py     # Contains all plotting template functions
├── environment.yml       # Conda environment definition file
└── README.md             # This guide
```

## How to Use

Follow this basic workflow to create a new figure:

1.  **Prepare Data:** Place your data file (e.g., `my_data.csv`) in the `data/` directory.
2.  **Create a New Script:** Create a new Python file in the `examples/` directory (e.g., `my_new_plot.py`).
3.  **Write the Code:**
    *   **Import necessary modules:**
        ```python
        import sys, os, pandas as pd
        # Add the src directory to the Python path to import our modules
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        sys.path.append(os.path.join(project_root, 'src'))
        # Import the style setter and the desired plotting function
        from publication_style import set_publication_style
        from plot_templates import plot_line_comparison
        ```
    *   **Set the Style:** Call `set_publication_style()` at the beginning of your script.
    *   **Load Data:** Use `pandas.read_csv()` to load your data into a DataFrame.
    *   **Call the Template Function:** Call the corresponding plotting function from `plot_templates.py`, passing your data, labels, and the desired output path.
4.  **Run the Script:**
    ```bash
    # Make sure the environment is active
    conda activate pubfigures
    python examples/my_new_plot.py
    ```
5.  **Find Your Figure:** The generated plot will be saved in the `figures/` directory.

---

## Figure Gallery & Use Cases

Here is a guide to the available plot types, their intended use, and the relevant example scripts.

### 1. Line Plot
- **Use Case:** Showing the trend of a continuous variable over another (e.g., time, distance, epochs). Ideal for comparing the performance of multiple algorithms.
- **Function:** `plot_line_comparison()`
- **Examples:** `examples/02_line_plot_example.py`, `examples/07_errorbar_example.py`

### 2. Grouped Bar Chart
- **Use Case:** Comparing discrete categories across several quantitative metrics.
- **Function:** `plot_grouped_bar_chart()`
- **Example:** `examples/03_bar_chart_example.py`

### 3. Heatmap
- **Use Case:** Visualizing matrix data. Excellent for confusion matrices and correlation matrices.
- **Function:** `plot_heatmap()`
- **Example:** `examples/04_heatmap_example.py`

### 4. Distribution Plot (Histogram/KDE)
- **Use Case:** Understanding the distribution (frequency, probability density) of a single continuous variable.
- **Function:** `plot_distribution()`
- **Example:** `examples/05_distribution_plot_example.py`

### 5. Box & Violin Plot
- **Use Case:** Comparing the distribution of a continuous variable across multiple groups or categories.
- **Function:** `plot_distribution_comparison()`
- **Example:** `examples/06_box_violin_example.py`

### 6. Plots with Error Bars
- **Use Case:** Representing the uncertainty or variability of data (e.g., Standard Deviation, SEM, Confidence Intervals).
- **Functions:** Integrated into `plot_line_comparison` (as error bands) and `plot_grouped_bar_chart` (as error bars).
- **Example:** `examples/07_errorbar_example.py`

### 7. Subplots (Compound Figures)
- **Use Case:** Combining multiple related plots into a single figure for direct comparison and to save space.
- **How-to:** All plotting functions in `plot_templates.py` accept an `ax` argument. Create a subplot grid with `plt.subplots()` and pass each `ax` object to the desired plotting function.
- **Example:** `examples/08_subplots_example.py`

### 8. Contour Plot
- **Use Case:** Visualizing how a third value (Z) varies across a 2D plane of two input variables (X and Y). Ideal for analyzing parameter spaces and finding optimal points.
- **Function:** `plot_contour()`
- **Example:** `examples/09_contour_plot_example.py`

### 9. t-SNE Visualization
- **Use Case:** Visualizing high-dimensional data in 2D. A powerful tool for comparing the quality of feature spaces generated by different AI models.
- **Function:** `plot_tsne()`
- **Example:** `examples/10_tsne_example.py`

### 10. Dual-Axis Plot
- **Use Case:** Comparing the trends of two variables with different units and/or scales over the same X-axis. Excellent for showing trade-offs.
- **Function:** `plot_dual_axis()`
- **Example:** `examples/11_dual_axis_example.py`

### 11. Stacked Bar Chart
- **Use Case:** Comparing a total quantity across categories while showing the contribution of sub-components to the total. Available in absolute and 100% proportional versions.
- **Function:** `plot_stacked_bar_chart()`
- **Example:** `examples/12_stacked_bar_example.py`

---

## Customizing the Style

The visual identity of all figures is controlled by the central style file: `src/publication_style.py`. You can easily customize the following in the `set_publication_style()` function:

- **Font Family:** Change `font.family` to `'serif'` and update `font.serif` to `['Times New Roman']` if required by a journal.
- **Font Sizes:** Adjust the various `*.size` parameters to match your publication's specific figure size requirements.
- **Colors:** Add or modify colors in the `COLOR_PALETTE` and `CONTEXT_COLORS` dictionaries to create a custom theme.

## Contributing

Contributions are welcome! If you have ideas for new plot types or improvements to existing templates, please feel free to create a Pull Request or open an Issue on GitHub.
