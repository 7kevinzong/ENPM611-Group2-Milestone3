# ENPM611 GitHub Issue Analysis Project

This application analyzes GitHub issues for the [poetry](https://github.com/python-poetry/poetry/issues) Open Source project and generates insightful visualizations. Our team has implemented three custom analyses that provide different perspectives on the project's issue management patterns.

## Analyses Implemented

### Example Analysis (Feature 0)

This is the template analysis that shows basic statistics and displays a bar chart of the top 50 issue creators.

### Analysis 1 - Issue Creation Trends (Feature 1)

This analysis visualizes the trend of issue creation over time. It plots issue creation frequency across the project's timeline, allowing you to see patterns in project activity. You can filter results for a specific user with the `--user` parameter.

### Analysis 2 - Contributor Network Analysis (Feature 2)

This analysis creates an interactive network visualization showing the connections between users in the Poetry project. It displays how different contributors interact with each other across issues, highlighting the project's collaboration patterns.

### Analysis 3 - Issue Lifecycle Analysis (Feature 3)

This analysis examines how long issues remain open and identifies patterns in issue resolution. It provides:

-   A distribution of issue resolution times (with mean and median markers)
-   Top users by average resolution speed
-   Correlation between comment count and resolution time
-   Summary statistics on issue resolution patterns

## Setup

To get started with this project:

1. Clone this repository to your local computer
2. Create a virtual environment and install dependencies:

```
pip install -r requirements.txt
```

3. Download the data file (in `json` format) from the project assignment in Canvas
4. Update the `config.json` with the path to the file or set the environment variable `ENPM611_PROJECT_DATA_PATH`

## Running the Analyses

Run any of the implemented analyses using the following command:

```
python run.py --feature <feature_number>
```

Where `<feature_number>` is:

-   0: Example Analysis
-   1: Issue Creation Trends
-   2: Contributor Network Analysis
-   3: Issue Lifecycle Analysis

### Optional Parameters

You can customize the analyses with these additional parameters:

-   `--user <username>`: Filter analysis for a specific user (used in features 0 and 1)
-   `--label <label>`: Filter issues by a specific label (used in feature 3)
-   `--dataset <number>`: Select which dataset to use (defaults to 0)

Example:

```
python run.py --feature 1 --user sdispater
```

## VSCode Configuration

This project includes VSCode configuration files to make development easier:

-   Runtime configurations for debugging each analysis in `.vscode/launch.json`
-   UI customizations in `.vscode/settings.json` to improve navigation and debugging

To use these features, open the run button in the left sidebar and select the analysis you want to run.
