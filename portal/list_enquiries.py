""" List Enquiries
"""
from portal import jiraclient


def main():
    """ List all Enquiries
    """
    client = jiraclient.get_jira_client()
    for item in client.jql('project="ENQ"')["issues"]:
        print(item)


if __name__ == "__main__":
    main()
