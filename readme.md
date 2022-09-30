Repository can temporarily be found [here](https://github.com/jasonaesh/silclss-signage); the repository is private, so you may need to request access

# Dependencies 

This script requires `python` and the following `pip` packages: 
`pandas`, `requests`, `google-api-python-client`, `google-auth-httplib2`, `google-auth-oauthlib`, `markdownify`

```
pip install --upgrade pandas requests google-api-python-client google-auth-httplib2 google-auth-oauthlib markdownify
```
# Todo 
- ~~Document code (in progress)~~
- Secure API keys 
  - Maybe [this](https://stackoverflow.com/questions/40865425/how-to-remove-sensitive-data-api-key-across-git-commit-history) will help? 
  - Also [this](https://python.land/data-processing/python-yaml)
  - [This](https://stackoverflow.com/questions/52998628/correct-way-for-storing-api-keys-to-credentials-yml-enc) as well
- Document how to get API keys and tokens

# Contributors
Devesh Nath wrote most of the code, with help from the following API documentation: 

Google Calendar: https://developers.google.com/calendar/api/quickstart/python

Trello: https://developer.atlassian.com/cloud/trello/rest/api-group-cards/#api-cards-post

Alex Pho ([@jasonaesh](https://github.com/jasonaesh)) documented the code from Devesh's original Google Docs documentation, bugfixed odd behavior, and provided Calendar description functionality.
