from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "American Banking Data - Fully_Cleaned_Data.csv"
ASSET_DIR = BASE_DIR / "assets"
OUTPUT_FILE = ASSET_DIR / "banking_dashboard.png"


def load_data() -> pd.DataFrame:
    data = pd.read_csv(DATA_FILE, index_col=0)
    data["Date Joined"] = pd.to_datetime(data["Date Joined"], errors="coerce")
    data["Age"] = pd.to_numeric(data["Age"], errors="coerce")
    data["Balance"] = pd.to_numeric(data["Balance"], errors="coerce")
    return data


def currency(value: float) -> str:
    return f"${value:,.0f}"


def save_dashboard_png() -> Path:
    df = load_data()
    ASSET_DIR.mkdir(exist_ok=True)

    customers = len(df)
    avg_balance = df["Balance"].mean()
    total_balance = df["Balance"].sum()
    default_rate = (df["Loan Default"].str.lower() == "yes").mean() * 100

    state_counts = df["State"].value_counts().head(10).sort_values()
    balance_by_job = df.groupby("Job Classification")["Balance"].mean().sort_values()
    joined = (
        df.dropna(subset=["Date Joined"])
        .set_index("Date Joined")
        .resample("ME")["Customer Code"]
        .count()
    )

    fig = plt.figure(figsize=(16, 10), facecolor="#f7f9fb")
    grid = fig.add_gridspec(3, 4, height_ratios=[0.75, 2, 2.1], hspace=0.48, wspace=0.35)

    fig.suptitle(
        "Banking Customer Dashboard",
        fontsize=24,
        fontweight="bold",
        x=0.06,
        y=0.965,
        ha="left",
        color="#132238",
    )

    metrics = [
        ("Customers", f"{customers:,}"),
        ("Average balance", currency(avg_balance)),
        ("Total balance", currency(total_balance)),
        ("Loan default rate", f"{default_rate:.1f}%"),
    ]

    for index, (label, value) in enumerate(metrics):
        ax = fig.add_subplot(grid[0, index])
        ax.set_facecolor("white")
        ax.text(0.05, 0.68, label, fontsize=12, color="#52616b", transform=ax.transAxes)
        ax.text(
            0.05,
            0.24,
            value,
            fontsize=22,
            fontweight="bold",
            color="#132238",
            transform=ax.transAxes,
        )
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_edgecolor("#d9e2ec")

    ax_state = fig.add_subplot(grid[1, :2])
    ax_state.barh(state_counts.index, state_counts.values, color="#287c8e")
    ax_state.set_title("Top States by Customers", loc="left", fontweight="bold")
    ax_state.set_xlabel("Customers")
    ax_state.grid(axis="x", color="#e8eef3")
    ax_state.set_axisbelow(True)

    ax_job = fig.add_subplot(grid[1, 2:])
    ax_job.bar(balance_by_job.index, balance_by_job.values, color="#d9822b")
    ax_job.set_title("Average Balance by Job", loc="left", fontweight="bold")
    ax_job.set_ylabel("Average balance")
    ax_job.tick_params(axis="x", rotation=15)
    ax_job.grid(axis="y", color="#e8eef3")
    ax_job.set_axisbelow(True)

    ax_joined = fig.add_subplot(grid[2, :])
    ax_joined.plot(joined.index, joined.values, color="#486581", linewidth=2.5)
    ax_joined.fill_between(joined.index, joined.values, color="#bcccdc", alpha=0.35)
    ax_joined.set_title("Monthly Customers Joined", loc="left", fontweight="bold")
    ax_joined.set_ylabel("Customers")
    ax_joined.grid(color="#e8eef3")
    ax_joined.set_axisbelow(True)

    for ax in [ax_state, ax_job, ax_joined]:
        ax.set_facecolor("white")
        for spine in ax.spines.values():
            spine.set_edgecolor("#d9e2ec")

    fig.savefig(OUTPUT_FILE, dpi=180, bbox_inches="tight")
    plt.close(fig)
    return OUTPUT_FILE


if __name__ == "__main__":
    output = save_dashboard_png()
    print(f"Saved dashboard image to {output}")
