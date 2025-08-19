#!/usr/bin/env -S uv run --script
#
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "matplotlib>=3.8.0",
#     "pandas>=2.1.0", 
#     "numpy>=1.24.0"
# ]
# ///
# timeline_matplotlib.py
# Standalone script adapted from:
# https://coderzcolumn.com/tutorials/data-science/timeline-using-matplotlib

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pathlib import Path


matplotlib.use("Agg")  # Non-interactive backend for saving files

# Global date range for the visualization
START_DATE = pd.Timestamp("2021-01-01")
END_DATE = pd.Timestamp("2025-12-31")
DISPLAY_END_DATE = pd.Timestamp("2026-01-01")  # For axis display
CURRENT_DATE = pd.Timestamp("2025-08-16")  # Today's date for visualization


def build_dataset() -> pd.DataFrame:
    # Print version as in the tutorial
    print("Matplotlib Version : {}".format(matplotlib.__version__))

    dates_to_team_events = {
        "2021-06-15": "Work on EELS started\nby Quilt at Consensys &\nlater EF Protocol Support",
        "2023-01-10": "Testing Team Started\n(sub-team of Security)",
        "2024-01-01": "Testing Team becomes\nan independent team",
        "2024-10-01": "STEEL Team Created:\nEELS + EEST",
        "2025-05-15": "STEEL: +2\namazing interns",
        "2025-06-01": "EF Protocol:\nSTEEL 11 members",
        # "2025-10-01": "THE WELD: Merge EELS and EEST Repos",
    }

    dates = dates_to_team_events.keys()
    phones = dates_to_team_events.values()
    iphone_df = pd.DataFrame(data={"Date": dates, "Product": phones})
    iphone_df["Date"] = pd.to_datetime(iphone_df["Date"])

    # Team member count with role breakdown
    date_to_team_roles = {
        "2021-01-01": {"EELS": 0, "EEST": 0, "Consensus": 0, "Intern": 0},  # zero
        "2021-03-01": {"EELS": 1, "EEST": 0, "Consensus": 0, "Intern": 0},  # sam?
        "2021-05-01": {"EELS": 2, "EEST": 0, "Consensus": 0, "Intern": 0},  # guru
        "2021-10-01": {"EELS": 2, "EEST": 1, "Consensus": 0, "Intern": 0},  # mario
        "2022-10-01": {"EELS": 3, "EEST": 1, "Consensus": 0, "Intern": 0},  # peter
        "2023-01-10": {"EELS": 3, "EEST": 2, "Consensus": 0, "Intern": 0},  # spencer
        "2023-04-01": {"EELS": 3, "EEST": 3, "Consensus": 0, "Intern": 0},  # dan
        "2023-10-01": {"EELS": 3, "EEST": 4, "Consensus": 0, "Intern": 0},  # dimitry
        "2025-02-01": {"EELS": 3, "EEST": 5, "Consensus": 0, "Intern": 0},  # felix
        "2025-03-01": {"EELS": 4, "EEST": 5, "Consensus": 1, "Intern": 0},  # carson
        "2025-05-01": {"EELS": 4, "EEST": 5, "Consensus": 1, "Intern": 0},  # leo
        "2025-05-27": {"EELS": 4, "EEST": 5, "Consensus": 1, "Intern": 2},  # intern
        "2025-08-16": {
            "EELS": 4,
            "EEST": 5,
            "Consensus": 1,
            "Intern": 0,
            "Grantee": 1,
        },  # Current date
        "2025-12-31": {
            "EELS": 4,
            "EEST": 5,
            "Consensus": 1,
            "Intern": 0,
            "Grantee": 1,
        },  # Projected: intern converts to Grantee
    }

    # Convert to DataFrame for easier plotting
    team_df = pd.DataFrame(date_to_team_roles).T
    team_df.index = pd.to_datetime(team_df.index)
    team_df = team_df.fillna(0).astype(int)

    # Generate Level column (alternating +/- ranges) as in the tutorial
    # Seed to make the script reproducible (optional)
    rng = np.random.default_rng(42)
    levels = []
    for i in range(len(iphone_df)):
        if (i % 2) == 0:
            levels.append(rng.integers(-6, -2))  # negative range: -6 .. -3
        else:
            levels.append(rng.integers(2, 6))  # positive range: 2 .. 5
    iphone_df["Level"] = levels

    return iphone_df, team_df


def plot_horizontal_basic(df: pd.DataFrame, team_df: pd.DataFrame):
    # Create figure with 2 subplots NOT sharing x-axis (to allow separate tick control)
    fig, (ax1, ax2) = plt.subplots(
        2, 1, figsize=(20, 12), gridspec_kw={"height_ratios": [2, 1]}, sharex=False
    )

    # Set background color for presentation
    fig.patch.set_facecolor("#f8f9fa")

    # SUBPLOT 1: Timeline
    # Dotted horizontal line across full timeline
    ax1.plot(
        [START_DATE, DISPLAY_END_DATE],
        [0, 0],
        ":",
        color="gray",
        linewidth=2,
        alpha=0.6,
    )
    # Horizontal timeline line with circle markers
    ax1.plot(df.Date, [0] * len(df), "-o", color="black", markerfacecolor="white")

    # Set x-axis limits and ticks with year labels
    ax1.set_xlim(START_DATE - pd.Timedelta(days=30), DISPLAY_END_DATE)
    ax1.set_ylim(-7, 7)
    ax1.set_xticks(pd.date_range("2021-1-1", "2026-1-1", freq="YS"))
    ax1.set_xticklabels(
        [str(year) for year in range(2021, 2027)],
        fontsize=20,
        color="#444",
        weight="bold",
    )
    ax1.tick_params(axis="x", labelsize=20, colors="#444", pad=10)

    # Add Ethereum upgrade markers
    # LONDON_DATE = pd.Timestamp("2021-08-05")
    # ax1.axvline(x=LONDON_DATE, color='#e74c3c', linestyle='--', linewidth=2, alpha=0.7, zorder=1)
    # ax1.text(LONDON_DATE, -7.5, 'London', ha='center', fontsize=16,
    #          color='#e74c3c', fontweight='bold', bbox=dict(boxstyle='round,pad=0.3',
    #          facecolor='white', edgecolor='#e74c3c', alpha=0.8))

    MERGE_DATE = pd.Timestamp("2022-09-15")
    ax1.axvline(
        x=MERGE_DATE, color="#e74c3c", linestyle="--", linewidth=2, alpha=0.7, zorder=1
    )
    ax1.text(
        MERGE_DATE,
        -7.5,
        "The Merge",
        ha="center",
        fontsize=16,
        color="#e74c3c",
        fontweight="bold",
        bbox=dict(
            boxstyle="round,pad=0.3", facecolor="white", edgecolor="#e74c3c", alpha=0.8
        ),
    )

    # SHAPELLA_DATE = pd.Timestamp("2023-04-12")
    # ax1.axvline(x=SHAPELLA_DATE, color='#e74c3c', linestyle='--', linewidth=2, alpha=0.7, zorder=1)
    # ax1.text(SHAPELLA_DATE, -7.5, 'Shapella', ha='center', fontsize=16,
    #          color='#e74c3c', fontweight='bold', bbox=dict(boxstyle='round,pad=0.3',
    #          facecolor='white', edgecolor='#e74c3c', alpha=0.8))

    # DENCUN_DATE = pd.Timestamp("2024-03-13")
    # ax1.axvline(x=DENCUN_DATE, color='#e74c3c', linestyle='--', linewidth=2, alpha=0.7, zorder=1)
    # ax1.text(DENCUN_DATE, -7.5, 'Dencun', ha='center', fontsize=16,
    #          color='#e74c3c', fontweight='bold', bbox=dict(boxstyle='round,pad=0.3',
    #          facecolor='white', edgecolor='#e74c3c', alpha=0.8))

    # PECTRA_DATE = pd.Timestamp("2025-03-07")
    # ax1.axvline(x=PECTRA_DATE, color='#e74c3c', linestyle='--', linewidth=2, alpha=0.7, zorder=1)
    # ax1.text(PECTRA_DATE, -7.5, 'Pectra', ha='center', fontsize=16,
    #          color='#e74c3c', fontweight='bold', bbox=dict(boxstyle='round,pad=0.3',
    #          facecolor='white', edgecolor='#e74c3c', alpha=0.8))

    # Add current date marker
    ax1.axvline(
        x=CURRENT_DATE,
        color="#098a34",
        linestyle="--",
        linewidth=2,
        alpha=0.7,
        zorder=1,
    )
    ax1.text(
        CURRENT_DATE,
        -7.5,
        "Today",
        ha="center",
        fontsize=16,
        color="#098a34",
        fontweight="bold",
        bbox=dict(
            boxstyle="round,pad=0.3", facecolor="white", edgecolor="#098a34", alpha=0.8
        ),
    )

    # Annotate each release with month-year and product, with a line to Level
    for idx in range(len(df)):
        dt, product, level = df["Date"][idx], df["Product"][idx], df["Level"][idx]
        dt_str = dt.strftime("%b %Y")

        # Different styling for past vs future events
        if dt <= CURRENT_DATE:
            color = "#2c3e50"
            alpha = 1.0
            linecolor = "#e74c3c"
        else:
            color = "#7f8c8d"
            alpha = 0.7
            linecolor = "#95a5a6"

        ax1.annotate(
            dt_str + "\n" + product,
            xy=(dt, 0.1 if level > 0 else -0.1),
            xytext=(dt, level),
            arrowprops=dict(
                arrowstyle="-", color=linecolor, linewidth=1.2, alpha=alpha
            ),
            ha="center",
            fontsize=16,
            fontweight="semibold",
            color=color,
            alpha=alpha,
            bbox=dict(
                boxstyle="round,pad=0.4",
                facecolor="white",
                edgecolor=linecolor,
                alpha=0.9 * alpha,
            ),
        )

    # Remove spines and center the x-axis
    for side in ["left", "top", "right", "bottom"]:
        ax1.spines[side].set_visible(False)
    ax1.spines["bottom"].set_position(("axes", 0.5))
    ax1.yaxis.set_visible(False)
    ax1.set_facecolor("#f8f9fa")

    # SUBPLOT 2: Team member stacked area chart
    # Define colors for each role - enhanced for presentation
    role_colors = {
        "EEST": "#3498db",  # Bright Blue
        "EELS": "#27ae60",  # Emerald Green
        "Consensus": "#e67e22",  # Carrot Orange
        "Intern": "#9b59b6",  # Purple
    }

    # Create a more continuous dataset by interpolating between points
    # Split data into actual and projected
    actual_mask = team_df.index <= CURRENT_DATE
    projected_mask = team_df.index >= CURRENT_DATE

    # Use step functions (no interpolation) - values stay constant until next change
    date_range = pd.date_range(
        start=team_df.index.min(), end=team_df.index.max(), freq="D"
    )
    team_df_interpolated = team_df.reindex(date_range).ffill().fillna(0)

    # Split interpolated data
    actual_data = team_df_interpolated[team_df_interpolated.index <= CURRENT_DATE]
    projected_data = team_df_interpolated[team_df_interpolated.index >= CURRENT_DATE]

    # Plot actual data (solid)
    bottom_actual = np.zeros(len(actual_data))
    for role in team_df.columns:
        ax2.fill_between(
            actual_data.index,
            bottom_actual,
            bottom_actual + actual_data[role],
            alpha=0.9,
            label=role,
            color=role_colors.get(role, "#95a5a6"),
            edgecolor="none",
        )
        bottom_actual += actual_data[role].values

    # Plot projected data (with pattern/transparency)
    bottom_proj = np.zeros(len(projected_data))
    for role in team_df.columns:
        ax2.fill_between(
            projected_data.index,
            bottom_proj,
            bottom_proj + projected_data[role],
            alpha=0.4,
            color=role_colors.get(role, "#95a5a6"),
            edgecolor="none",
            hatch="//",
        )
        bottom_proj += projected_data[role].values

    # Add Ethereum upgrade lines
    # ax2.axvline(x=LONDON_DATE, color='#e74c3c', linestyle='--', linewidth=2, alpha=0.7)
    ax2.axvline(x=MERGE_DATE, color="#e74c3c", linestyle="--", linewidth=2, alpha=0.7)
    # ax2.axvline(x=SHAPELLA_DATE, color='#e74c3c', linestyle='--', linewidth=2, alpha=0.7)
    # ax2.axvline(x=DENCUN_DATE, color='#e74c3c', linestyle='--', linewidth=2, alpha=0.7)
    # ax2.axvline(x=PECTRA_DATE, color='#e74c3c', linestyle='--', linewidth=2, alpha=0.7)

    # Add current date line
    ax2.axvline(x=CURRENT_DATE, color="#e74c3c", linestyle="--", linewidth=2, alpha=0.7)

    # Configure histogram subplot - remove frame and improve aesthetics
    ax2.set_ylim(0, team_df.sum(axis=1).max() * 1.25)

    # Remove all spines (frame)
    for spine in ax2.spines.values():
        spine.set_visible(False)

    # Subtle horizontal grid
    ax2.yaxis.grid(True, alpha=0.2, linestyle=":", color="#bdc3c7")
    ax2.set_axisbelow(True)  # Put grid behind bars
    ax2.set_facecolor("#f8f9fa")

    # Format x-axis to match timeline
    ax2.set_xlim(START_DATE - pd.Timedelta(days=30), DISPLAY_END_DATE)
    ax2.set_xticks(pd.date_range("2021-1-1", "2026-1-1", freq="YS"))
    ax2.set_xticklabels(range(2021, 2027), fontsize=20, color="#444")

    # Move y-axis to the right side
    ax2.yaxis.tick_right()
    ax2.yaxis.set_label_position("right")

    # Format y-axis labels - integers only
    ax2.tick_params(axis="y", labelsize=16, colors="#444")
    ax2.yaxis.set_major_locator(plt.MaxNLocator(integer=True))

    # Remove tick marks
    ax2.tick_params(bottom=False, left=False, right=False)

    # Add legend inside the plot area - upper left corner
    ax2.legend(
        loc="upper left",
        frameon=True,
        title="Team Roles",
        ncol=1,
        bbox_to_anchor=(0.02, 0.98),
        title_fontsize=16,
        fontsize=14,
        fancybox=True,
        shadow=True,
        framealpha=0.95,
    )

    # Overall figure title - removed for presentation
    # fig.suptitle("STEEL Team Evolution", fontsize=20, fontweight="bold", y=0.98)

    plt.tight_layout()

    # Create build directory if it doesn't exist
    script_dir = Path(__file__).parent
    build_dir = script_dir / "build"
    build_dir.mkdir(exist_ok=True)

    # Save the figure with high quality for presentation
    filename = build_dir / "team_timeline.png"
    plt.savefig(
        filename,
        dpi=200,
        bbox_inches="tight",
        facecolor="#f8f9fa",
        edgecolor="none",
    )
    print(f"Figure saved as '{filename}'")

    return fig, (ax1, ax2)


def plot_horizontal_fivethirtyeight(df: pd.DataFrame):
    with plt.style.context("fivethirtyeight"):
        fig, ax = plt.subplots(figsize=(18, 9))

        ax.plot(df.Date, [0] * len(df), "-o", color="black", markerfacecolor="white")
        ax.set_xticks(
            pd.date_range("2023-1-1", "2025-8-1", freq="ys"), range(2023, 2026)
        )
        # ax.set_xticks(pd.date_range("2007-1-1", "2023-1-1", freq="ys"), range(2007, 2024))
        ax.set_ylim(-7, 7)

        for idx in range(len(df)):
            dt, product, level = df["Date"][idx], df["Product"][idx], df["Level"][idx]
            dt_str = dt.strftime("%b-%Y")
            ax.annotate(
                dt_str + "\n" + product,
                xy=(dt, 0.1 if level > 0 else -0.1),
                xytext=(dt, level),
                arrowprops=dict(arrowstyle="-", color="red", linewidth=0.8),
                ha="center",
            )

        for side in ["left", "top", "right", "bottom"]:
            ax.spines[side].set_visible(False)
        ax.spines["bottom"].set_position(("axes", 0.5))
        ax.yaxis.set_visible(False)
        ax.set_title(
            "iPhone Release Dates", pad=10, loc="left", fontsize=25, fontweight="bold"
        )
        ax.grid(False)

        return fig, ax


# def plot_vertical_fivethirtyeight(df: pd.DataFrame):
#     with plt.style.context("fivethirtyeight"):
#         fig, ax = plt.subplots(figsize=(9, 18))

#         ax.plot([0] * len(df), df.Date, "-o", color="black", markerfacecolor="white")
#         ax.set_yticks(pd.date_range("2007-1-1", "2023-1-1", freq="ys"), range(2007, 2024))
#         ax.set_xlim(-7, 7)

#         for idx in range(len(df)):
#             dt, product, level = df["Date"][idx], df["Product"][idx], df["Level"][idx]
#             dt_str = dt.strftime("%b-%Y")
#             ax.annotate(
#                 dt_str + "\n" + product,
#                 xy=(0.1 if level > 0 else -0.1, dt),
#                 xytext=(level, dt),
#                 arrowprops=dict(arrowstyle="-", color="red", linewidth=0.8),
#                 va="center",
#             )

#         for side in ["left", "top", "right", "bottom"]:
#             ax.spines[side].set_visible(False)
#         ax.spines["left"].set_position(("axes", 0.5))
#         ax.xaxis.set_visible(False)
#         ax.set_title("iPhone Release Dates", pad=10, loc="left", fontsize=25, fontweight="bold")
#         ax.grid(False)

#         return fig, ax


def main():
    df, team_df = build_dataset()

    # 1) Basic horizontal with team member histogram
    plot_horizontal_basic(df, team_df)

    # 2) Horizontal with fivethirtyeight style
    # plot_horizontal_fivethirtyeight(df)

    # 3) Vertical timeline
    # plot_vertical_fivethirtyeight(df)

    # plt.show()  # Commented out for non-interactive mode
    plt.close()  # Close the figure to free memory


if __name__ == "__main__":
    main()
