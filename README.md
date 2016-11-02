# legistar
# Welcome to HackLB/legistar

This repository is intended to mirror and archive records from the City of Long Beach [Legistar calendar](http://longbeach.legistar.com/Calendar.aspx). We use JSON as a convenient format for consuming and analyzing city meeting records, and git in order to maintain a historical record including changes over time. This repo groups records by commission or meeting name, and then by date, so you can easily see the history of meetings for each commission or group. Any agenda and minutes documents are also downloaded and saved.

This project is an activity of [HackLB](https://github.com/HackLB).


### Contributing to this repo

Pull requests are welcome - if you have an idea for an improvement (for instance, porting `update.py` to another language) you're welcome to make it and open a PR, or open an issue first for discussion.

### Sample record

A typical record is shown below for reference:

```
{
    "agenda": "http://longbeach.legistar.com/View.ashx?M=A&ID=506515&GUID=28596189-0E2D-4567-B867-6290850FC835",
    "datetime": "2016-09-28T15:30:00",
    "id": "28596189-0E2D-4567-B867-6290850FC835-2016-10-10-21-16-04",
    "link": "http://longbeach.legistar.com/Gateway.aspx?M=MD&From=RSS&ID=506515&GUID=28596189-0E2D-4567-B867-6290850FC835",
    "minutes": "http://longbeach.legistar.com/View.ashx?M=M&ID=506515&GUID=28596189-0E2D-4567-B867-6290850FC835",
    "name": "Technology and Innovation Commission",
    "summary": "",
    "title": "Technology and Innovation Commission - 9/28/2016 - 3:30 PM"
}
```