# X is the Dark Souls of Y

Twitter bot that tells you what X is the Dark Souls of

## Usage

```python
python x-darksouls-y.py --consumer-key CONSUMER_KEY
                        --consumer-secret CONSUMER_SECRET
                        --access-token-key ACCESS_TOKEN_KEY
                        --access-token-secret ACCESS_TOKEN_SECRET
                        [--search SEARCH_TERM]
                        [--pattern PATTERN]
```

Create a [Twitter app](https://apps.twitter.com/) to generate your:

* `CONSUMER_KEY`
* `CONSUMER_SECRET`
* `ACCESS_TOKEN_KEY`
* `ACCESS_TOKEN_SECRET`

Optional arguments:

* `SEARCH` - Phrase to search Twitter for (Defaults to "is harder than")
* `PATTERN` - Pattern to replace search with (Defaults to "is the Dark Souls of")

## Deploy

Follow the steps on Heroku's website [here](https://devcenter.heroku.com/articles/git) to deploy or click this button:

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/kevinselwyn/x-darksouls-y)

Set `CONSUMER_KEY`, `CONSUMER_SECRET`, `ACCESS_TOKEN_KEY`, and `ACCESS_TOKEN_SECRET` in the Config Variables of the Heroku app.
