# pylint: skip-file
"""

"""
import jiraclient


def main():
    """ Sample Jira Request
    """
    client = jiraclient.get_jira_client()
    data = {
        "project": {"key": "ENQ"},
        "summary": "New issue from jira-python",
        "description": "Look into this one",
        "issuetype": {"name": "Task"},
    }
    client.create_issue(data)


if __name__ == "__main__":
    main()
