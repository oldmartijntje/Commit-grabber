# Commit-grabber
Want to know your most common commit message? you got it!

create a .env:
```
API_KEY=ghp_00000000000000000
GH_NAME=username
```

you find this api key [here](https://github.com/settings/tokens), an old classic token type with `repo` access.

run `run.py` to get the `commit_details.csv`. And then you can load it into the yupiter notebook for analysis.