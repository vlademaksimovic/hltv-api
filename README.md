# HLTV API
An unofficial API for [HLTV.org](HLTV.org).

# Table of Contents
- [API Usage](#api-usage)
    - [Match Results](#match-results)
    - [Upcoming Matches](#upcoming-matches)
    - [Rankings](#team-rankings)
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
- TODO

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
      "match_link": "https://www.hltv.org/matches/2314656/teamplay-vs-ex-outlaws-epicenter-2017-europe-qualifier-2",
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
You might get a _500_ or _502_. See the [Error Responses](#error-responses) section for more information.


## Upcoming Matches
Returns data about the live as well as the upcoming matches.

### URL
`/v1/matches`

### Method
`GET`

### URL Parameters
Use **filter** to get a subset of the upcoming matches.
Available values: `live`

Example:
```
/v1/matches?filter=live
```

### Success Response
200 OK
```json
{
  "count": 348,
  "matches": [
    {
      "date": "2017-09-09",
      "event": "ESG Tour Mykonos 2017",
      "map": "bo3",
      "match_link": "https://www.hltv.org/matches/2314537/sk-vs-liquid-esg-tour-mykonos-2017",
      "team1": "SK",
      "team2": "Liquid",
      "time": "19:30"
    },
    ...
  ]
}
```

### Error Response
You might get a _500_ or _502_. See the [Error Responses](#error-responses) section for more information.


## Team Rankings
Returns the current team rankings.

### URL
`/v1/rankings`

### Method
`GET`

### URL Parameters
- TODO

### Success Response
200 OK
```json
{
  "count": 30,
  "ranking": [
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
You might get a _500_ or _502_. See the [Error Responses](#error-responses) section for more information.

# Error Responses
## 500 Internal Server Error
If the fetched data could not be parsed correctly this will be returned. This could mean HLTV has changed their HTML code and thus would require manual work to fix it. It could also mean that a corner-case that has not been thought of occurred on HLTV and that the API can't support it.
## 502 Bad Gateway
This means no data could be retrieved from HLTV and that it's probably not the API's fault. Make sure HLTV is up and try again later.

# License
MIT
