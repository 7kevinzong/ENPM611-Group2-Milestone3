## test_dataset_initialization
Test if DATASET is None by default

## test_run_with_closed_issues
<!--    fake_issue_data = {
            "number": 1,
            "title": "Fake Issue",
            "creator": "user1",
            "labels": ["bug"],
            "created_date": "2023-01-01T00:00:00Z",
            "updated_date": "2023-01-05T00:00:00Z",
            "state": "closed",
            "events": [
                {
                    "event_type": "comment",
                    "author": "user1",
                    "event_date": "2023-01-02T00:00:00Z",
                    "comment": "sample comment",
                }
            ],
        }  -->
Set "state": "closed" --> expect code will printout either             
<!--    print(
                f"Analyzing {len(closed_issues)} closed issues with label {self.LABEL}"
            )
        else:
            print(f"Analyzing {len(closed_issues)} closed issues") -->

## test_run_with_no_closed_issues
similar to test_run_with_closed_issues, but set state: "open"
Expected:
    <!-- print(f"Analyzing {len(closed_issues)} closed issues") -->

## test_run_with_label_mismatch
<!--    mock_get_parameter.side_effect = lambda key: "security" if key == "label" else 0

        issue_data = {
            "number": 2,
            "title": "Label mismatch test",
            "creator": "user2",
            "labels": ["bug"],
            "created_date": "2023-03-01T00:00:00Z",
            "updated_date": "2023-03-05T00:00:00Z",
            "state": "closed",
            "events": [],
        } -->
Set LABEL = "sercurity" is not in labels["bug"]
Expected:
<!--        print(
                f"Analyzing {len(closed_issues)} closed issues with label {self.LABEL}"
            ) -->
where len(closed_issues) = 0, because "sercurity" is not in labels["bug"]

## test_issue_with_different_comment_author
<!-- mock_get_parameter.side_effect = lambda key: "bug" if key == "label" else 0
        issue_data = {
            "number": 3,
            "title": "Author mismatch",
            "creator": "user3",
            "labels": ["bug"],
            "created_date": "2023-04-01T00:00:00Z",
            "updated_date": "2023-04-03T00:00:00Z",
            "state": "closed",
            "events": [
                {
                    "event_type": "comment",
                    "author": "other_user",
                    "event_date": "2023-04-02T00:00:00Z",
                    "comment": "Helpful comment",
                }
            ],
        } -->
Set different author: "other_user", and it shoudn't effect anything to the code.
Expected it will run to the end of the code:
<!-- print(f"Fastest resolution time: {df['resolution_time'].min()} days") -->

## test_run_with_invalid_data
<!--    mock_get_parameter.side_effect = lambda key: "bug" if key == "label" else 0

        invalid_issue_data = {
            "number": 1,
            "title": "Invalid Issue",
            "creator": "user4",
            "labels": ["bug"],
            "created_date": "invalid_date",
            "updated_date": "invalid_date",
            "state": "closed",
            "events": [],
        } -->

Set created_date and updated_date to invalid_date which is wrong date format.
Expected:
<!--
        if not issue_data:
            print("No valid lifecycle data found to analyze.")
            return
 -->
