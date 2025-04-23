from typing import List
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import timedelta
import seaborn as sns

from data_loader import DataLoader
from model import Issue, Event, State
import config


class Analysis3:
    """Implements an analysis of Github issue lifecycles, showing resolution times and patterns"""

    def __init__(self):
        """
        Constructor for Analysis3 class
        """
        # Parameter is passed in via command line (--label)
        self.LABEL = config.get_parameter("label")
        # Dataset selection
        self.DATASET = config.get_parameter("dataset")
        if self.DATASET is None:
            self.DATASET = 0

    def run(self):
        """
        Starting point for this analysis.
        Analyzes issue lifecycle metrics including resolution times.
        """
        print("Started analyis 3: Issue Lifecycle Analysis")
        issues: List[Issue] = DataLoader(self.DATASET).get_issues()

        # Only analyze closed issues so we have complete lifecycle data
        closed_issues = [issue for issue in issues if issue.state == State.closed]

        if len(closed_issues) == 0:
            print("No closed issues found in the dataset.")
            return

        # Filter by label if specified
        if self.LABEL is not None:
            closed_issues = [
                issue for issue in closed_issues if self.LABEL in issue.labels
            ]
            print(
                f"Analyzing {len(closed_issues)} closed issues with label {self.LABEL}"
            )
        else:
            print(f"Analyzing {len(closed_issues)} closed issues")

        # Calculate resolution times (in days)
        issue_data = []
        for issue in closed_issues:
            if issue.created_date and issue.updated_date:
                resolution_time = (issue.updated_date - issue.created_date).days

                # Skip negative values
                if resolution_time < 0:
                    continue

                issue_data.append(
                    {
                        "issue_number": issue.number,
                        "issue_title": issue.title,
                        "creator": issue.creator,
                        "resolution_time": resolution_time,
                        "labels": ",".join(issue.labels),
                        "created_date": issue.created_date,
                        "updated_date": issue.updated_date,
                        "comment_count": len(
                            [e for e in issue.events if e.comment is not None]
                        ),
                    }
                )
        if not issue_data:
            print("No valid lifecycle data found to analyze.")
            return

        # Create a DataFrame from the issue data
        df = pd.DataFrame(issue_data)

        # --- Visualization 1: Resolution Time Distribution ---
        plt.figure(figsize=(10, 6))
        sns.histplot(df["resolution_time"], bins=30, kde=True)
        plt.title("Distribution of Issue Resolution Times")
        plt.xlabel("Resolution Time (days)")
        plt.ylabel("Number of Issues")
        plt.axvline(
            df["resolution_time"].median(),
            color="red",
            linestyle="--",
            label=f'Median: {df["resolution_time"].median():.4f} days',
        )
        plt.axvline(
            df["resolution_time"].mean(),
            color="red",
            linestyle="--",
            label=f'Mean: {df["resolution_time"].mean():.4f} days',
        )
        plt.legend()
        plt.grid()
        plt.tight_layout()
        plt.show()

        # --- Visualization 2: Top 15 Users by Average Resolution Time ---
        # Group by creator and calculate mean resolution time
        user_resoltuion = df.groupby("creator")["resolution_time"].agg(
            ["mean", "count"]
        )
        # Filter by users with at least 2 issues to have meaningful data
        user_resoltuion = user_resoltuion[user_resoltuion["count"] >= 2]
        user_resoltuion = user_resoltuion.sort_values("mean", ascending=True).head(15)

        plt.figure(figsize=(12, 6))
        bars = plt.barh(
            user_resoltuion.index,
            user_resoltuion["mean"],
            color=sns.color_palette("viridis", len(user_resoltuion)),
        )

        # Add issue counts to the bars
        for i, bar in enumerate(bars):
            plt.text(
                bar.get_width() + 0.5,
                bar.get_y() + bar.get_height() / 2,
                f"{user_resoltuion['count'].iloc[i]} issues",
                va="center",
                color="black",
            )

        plt.title("Top 15 Users by Average Resolution Time (with at least 2 issues)")
        plt.xlabel("Average Resolution Time (days)")
        plt.ylabel("User")
        plt.grid()
        plt.tight_layout()
        plt.show()

        # --- Visualization 3: Correlation between Comments and Resolution Time ---
        plt.figure(figsize=(10, 6))
        plt.scatter(df["comment_count"], df["resolution_time"], alpha=0.6)

        # Add a trend line
        z = np.polyfit(df["comment_count"], df["resolution_time"], 1)
        p = np.poly1d(z)
        plt.plot(
            np.sort(df["comment_count"]),
            p(np.sort(df["comment_count"])),
            "r--",
            linewidth=2,
            label=f"Trend Line (slope={z[0]:.2f})",
        )
        plt.title("Correlation between Comments and Resolution Time")
        plt.xlabel("Number of Comments")
        plt.ylabel("Resolution Time (days)")

        # Calculate correlation coefficient
        correlation = df["comment_count"].corr(df["resolution_time"])
        plt.annotate(
            f"Correlation: {correlation:.2f}",
            xy=(0.7, 0.9),
            xycoords="axes fraction",
            fontsize=12,
            color="black",
        )
        plt.tight_layout()
        plt.show()

        # Print summary statistics
        print("\nIssue Resolution Summary:")
        print(f"Average resolution time: {df['resolution_time'].mean():.2f} days")
        print(f"Median resolution time: {df['resolution_time'].median():.2f} days")
        print(f"Fastest resolution time: {df['resolution_time'].min()} days")
        print(f"Slowest resolution time: {df['resolution_time'].max()} days")

        if len(df) >= 10:
            # Find the 10 longest-lived issues
            longest_issues = df.nlargest(10, "resolution_time")
            print("\nTop 10 longest-lived issues:")
            for _, row in longest_issues.iterrows():
                print(
                    f"#{row['issue_number']} ({row['resolution_time']} days): {row['issue_title'][:60]}..."
                )


if __name__ == "__main__":
    analysis = Analysis3()
    analysis.run()
