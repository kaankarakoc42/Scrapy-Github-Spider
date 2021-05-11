# Scrapy-Github-Spider
Github spider with scrapy

# skills used
| skills | state |
| ------------- | ------------- |
| selectors | ✔️ |
| items | ✔️ |
| piplines | ✔️ |
| spider with args | ✔️ |
| middlewares | ❌ |




# run
```scrapy crawl github -a username="your github username"```
or
```scrapy crawl github -a usernames=['1','2']```

for setting output path

```scrapy crawl github -a username="your github username" -o test.json```
