# HLTV API
[![Build Status](https://travis-ci.org/simeg/hltv-api.svg?branch=master)](https://travis-ci.org/simeg/hltv-api)

An unofficial API for [HLTV.org](http://HLTV.org).

# Table of Contents
- [API Usage](#api-usage)
    - [Match Results](#match-results)
    - [Upcoming Matches](#upcoming-matches)
    - [News](#news)
    - [Team Rankings](#team-rankings)
    - [Stats](#stats)
- [Error Responses](#error-responses)
- [License](#license)

# API Usage
**Base URL:** `http://hltv-api.herokuapp.com`


## Match Results
Returns data about finished matches. By default it will return the 100 latest matches.

### URL
`/v1/results`

### Method
`GET`

### URL Parameters
- `limit=[integer]` - Limit the number of items in the response
- `offset=[integer]` - How many items to offset when reading from HLTV

### Success Response
200 OK
```json
{
  "count": 100,
  "results": [
    {
      "date": "September 9th 2017",
      "event": "EPICENTER 2017 Europe Qualifier #2",
      "map": "inf",
      "match_url": "https://www.hltv.org/matches/2314656/teamplay-vs-ex-outlaws-epicenter-2017-europe-qualifier-2",
      "score_lost": 8,
      "score_won": 6,
      "team1": "TEAMPLAY",
      "team2": "ex-Outlaws",
      "winner": "TEAMPLAY"
    },
    ...
  ]
}
```

### Error Response
_400_, _500_ or _502_. See the [Error Responses](#error-responses) section.

### Example
```sh
$ curl http://hltv-api.herokuapp.com/v1/results?limit=10
```


## Upcoming Matches
Returns data about the upcoming and live matches.

### URL
`/v1/matches`

### Method
`GET`

### URL Parameters
- `limit=[integer]` - Limit the number of **total** items in the response. The limit applies to each type separately, so using `limit=5` will equal in a total of 10 matches, 5 live and 5 upcoming (assuming they are available)
- `filter=[upcoming|live]` - Specify the type of match you want

### Success Response
200 OK
```json
{
  "count": 349,
  "matches": {
    "live": [
      {
        "event": "DreamHack Open Montreal 2017",
        "maps": [
          {
            "name": "cch",
            "team1_score": 16,
            "team2_score": 12
          },
          {
            "name": "trn",
            "team1_score": 13,
            "team2_score": 2
          },
          {
            "name": "inf",
            "team1_score": "-",
            "team2_score": "-"
          }
        ],
        "match_type": "Best of 3",
        "team1": "Cloud9",
        "team2": "Luminosity"
      },
      ...
    ],
    "upcoming": [
      {
        "date": "2017-09-10",
        "event": "eXTREMESLAND 2017 Indonesia Regional Finals",
        "map": "bo3",
        "match_url": "https://www.hltv.org/matches/2314581/akara-vs-boom-extremesland-2017-indonesia-regional-finals",
        "team1": "AKARA",
        "team2": "BOOM",
        "start_time": "05:00"
      },
      ...
    ]
  }
}
```

**NOTE:** If `teamX_score` is equal to `"-"` it means that the match has not been started and that there's no score yet.

### Error Response
_400_, _500_ or _502_. See the [Error Responses](#error-responses) section.

### Example
```sh
$ curl http://hltv-api.herokuapp.com/v1/matches?filter=upcoming
```


## News
Returns the news from the front page of HLTV.

### URL
`/v1/news`

### Method
`GET`

### URL Parameters
- `limit=[integer]` - Limit the number of items in the response
- `year=[integer]` - Get items from this year, minimum value is `2005` (requires the `month` param to be defined)
- `month=[string]` - Get items from this month. **Example:** `december` (requires the `year` param to be defined)

### Success Response
200 OK
```json
{
  "count": 30,
  "news": [
    {
      "comments_count": 57,
      "country": "hungary",
      "news_url": "https://www.hltv.org/news/21472/gameagents-recruit-volgare",
      "published_at": "3 hours ago",
      "title": "GameAgents recruit volgare"
    },
    ...
  ]
}
```

### Error Response
_400_, _500_ or _502_. See the [Error Responses](#error-responses) section.

### Example
```sh
$ curl http://hltv-api.herokuapp.com/v1/news?year=2015&month=may
```


## Team Rankings
Returns the current team rankings.

### URL
`/v1/rankings`

### Method
`GET`

### URL Parameters
- `limit=[integer]` - Limit the number of items in the response

### Success Response
200 OK
```json
{
  "count": 30,
  "rankings": [
    {
      "name": "SK",
      "points": 886,
      "position": 1
    },
    ...
  ]
}
```

### Error Response
_400_, _500_ or _502_. See the [Error Responses](#error-responses) section.

### Example
```sh
$ curl http://hltv-api.herokuapp.com/v1/rankings?limit=5
```


## Stats
Returns the current **rating** statistics for top 8 players and teams. Default returns statistics for both players and teams.
The response is ordered, meaning the first player in the response is the highest rated player, and the same rule applies for teams.

### URL
`/v1/stats`

### Method
`GET`

### URL Parameters
- `limit=[integer]` - Limit the number of **total** items in the response. The limit applies to each type separately, so using `limit=5` will equal in a total of 10 items, 5 players and 5 teams (assuming they are available)
- `type=[players|teams]` - The type of statistics you want in the response (default is both)

### Success Response
200 OK
```json
{
  "count": 16,
  "stats": {
    "players": [
      {
        "maps": 548,
        "name": "XANTARES",
        "origin": "turkey",
        "picture_url": "https://static.hltv.org/images/playerprofile/thumb/7938/100.jpeg?v=3",
        "profile_url": "https://www.hltv.org/stats/players/7938/XANTARES",
        "rating": 1.25
      },
      ...
    ],
    "teams": [
      {
        "maps": 443,
        "name": "TyLoo",
        "picture_url": "https://static.hltv.org/images/team/logo/4863",
        "profile_url": "https://www.hltv.org/stats/teams/4863/TyLoo",
        "rating": 1.09
      },
      ...
    ]
  }
}
```

### Error Response
_400_, _500_ or _502_. See the [Error Responses](#error-responses) section.

### Example
```sh
$ curl http://hltv-api.herokuapp.com/v1/stats?type=teams
```


# Error Responses
## 400 Bad Request
Your request was bad meaning you passed along some data that could not be parsed or was somehow faulty.
## 404 Not Found
Your request doesn't match anything on the server, you most likely are trying to access an endpoint that doesn't exist.
## 500 Internal Server Error
If the fetched data could not be parsed correctly this will be returned. This could mean HLTV has changed their HTML code and thus would require manual work to fix it. It could also mean that a corner-case that has not been thought of occurred on HLTV and that the API can't support it.
## 502 Bad Gateway
This means no data could be retrieved from HLTV and that it's probably not the API's fault. Make sure HLTV is up and try again later.

# License
MIT
