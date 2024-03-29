Repository can temporarily be found [here](https://github.com/jasonaesh/silclss-signage); the repository is private, so you may need to request access
# Instructions
## config.yaml
Rename `config_template.yaml` to `config.yaml`

### config.yaml: trello fields
1) Make sure you are logged into a [Trello](https://trello.com) account with access to the board you want
2) Generate a [Trello API key](https://trello.com/1/appKey/generate)
3) There will be two keys on the page once you generate the keys. The block below describes which goes where.
4) A third key (token) will be generated by clicking **Generate a Token**, below **Personal Key**

The following table describe which key goes where:
| config.yaml field | Corresponding key/token |
| -                 | -                       |
| API_key           | Personal key            |
| API_secret        | OAuth Secret            |
| Token             | Token                   |

### config.yaml: google fields
Go to [Google Calendar](https://calendar.google.com)
For each calendar you want to add, do the following:
1) Click the three dots by the calendar in the sidebar, then open Settings
2) Scroll down to **Integrate calendar** and copy the Calendar ID
3) Add a new field to config.yaml under google, and paste your calendar ID after it (e.g. `calendarID1: 'lsdkghqwruhg@group.calendar.google.com'`)

### config.yaml: path
Copy the directory name of the folder containing all the files into the field

# Dependencies 

This script requires `python` and the following `pip` packages: 
`pandas`, `requests`, `google-api-python-client`, `google-auth-httplib2`, `google-auth-oauthlib`, `markdownify`

```
pip install --upgrade pandas requests google-api-python-client google-auth-httplib2 google-auth-oauthlib markdownify
```

# Todo
Generalize the list ID as well, forgot to do this

# Contributors
Devesh Nath wrote most of the code, with help from the following API documentation: 

Google Calendar: https://developers.google.com/calendar/api/quickstart/python

Trello: https://developer.atlassian.com/cloud/trello/rest/api-group-cards/#api-cards-post

Alex Pho ([@jasonaesh](https://github.com/jasonaesh)) documented the code from Devesh's original Google Docs documentation, bugfixed odd behavior, and provided Calendar description functionality.
