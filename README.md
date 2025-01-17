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
    "agenda": "http://longbeach.legistar.com/View.ashx?M=A&ID=509077&GUID=FEA0F02F-C707-4700-915D-2CB2EF247F9F",
    "agenda_items": [
        {
            "agenda_num": 1,
            "attachments": [],
            "file_num": "16-025AC",
            "name": "AAC Excuse Absent Commissioners",
            "title": "Recommendation to excuse Commissioners that are absent from the Airport Advisory Commission meeting on October 20, 2016.",
            "type": "AC-Agenda Item",
            "url": "http://longbeach.legistar.com/LegislationDetail.aspx?ID=2860724&GUID=4E0D5281-A121-4BBB-9C0E-1A8D624331C2&Options=&Search=",
            "version": 1
        },
        {
            "agenda_num": 2,
            "attachments": [],
            "file_num": "16-026AC",
            "name": "AAC Minutes 091516",
            "title": "Recommendation to approve the Minutes from the Airport Advisory Commission meeting on September 15, 2016.",
            "type": "AC-Agenda Item",
            "url": "http://longbeach.legistar.com/LegislationDetail.aspx?ID=2860725&GUID=70187ECB-88B3-42E6-96A9-EA62AA86F9F8&Options=&Search=",
            "version": 1
        },
        {
            "agenda_num": 3,
            "attachments": [
                {
                    "filename": "Public Comment - Jim Stok.pdf",
                    "num": 1,
                    "url": "http://longbeach.legistar.com/View.ashx?M=F&ID=4735778&GUID=94AA291B-8B28-4090-8256-4D3A31D4E638"
                },
                {
                    "filename": "Presentation - Feasibility Study for FIS at Long Beach Airport.pdf",
                    "num": 2,
                    "url": "http://longbeach.legistar.com/View.ashx?M=F&ID=4742949&GUID=6A64A33F-31D3-4689-8BAB-C00B73494EC4"
                },
                {
                    "filename": "102016_FIS STUDY SESSION AIRPORT COMM_MEP_fulltranscript.pdf",
                    "num": 3,
                    "url": "http://longbeach.legistar.com/View.ashx?M=F&ID=4754591&GUID=9D1C5D58-0614-4B59-A708-D2FC8F4CBCD0"
                }
            ],
            "file_num": "16-028AC",
            "name": "FIS Study Session",
            "title": "Recommendation to conduct a study session to receive and file a presentation on a feasibility study for a Federal Inspection Service (FIS) facility at the Long Beach Airport.",
            "type": "AC-Agenda Item",
            "url": "http://longbeach.legistar.com/LegislationDetail.aspx?ID=2860738&GUID=23D033B5-BD92-43F1-9736-248F704C06B8&Options=&Search=",
            "version": 1
        },
        {
            "agenda_num": 3,
            "attachments": [
                {
                    "filename": "Public Comment - Jim Stok.pdf",
                    "num": 1,
                    "url": "http://longbeach.legistar.com/View.ashx?M=F&ID=4735778&GUID=94AA291B-8B28-4090-8256-4D3A31D4E638"
                },
                {
                    "filename": "Presentation - Feasibility Study for FIS at Long Beach Airport.pdf",
                    "num": 2,
                    "url": "http://longbeach.legistar.com/View.ashx?M=F&ID=4742949&GUID=6A64A33F-31D3-4689-8BAB-C00B73494EC4"
                },
                {
                    "filename": "102016_FIS STUDY SESSION AIRPORT COMM_MEP_fulltranscript.pdf",
                    "num": 3,
                    "url": "http://longbeach.legistar.com/View.ashx?M=F&ID=4754591&GUID=9D1C5D58-0614-4B59-A708-D2FC8F4CBCD0"
                }
            ],
            "file_num": "16-028AC",
            "name": "FIS Study Session",
            "title": "Recommendation to conduct a study session to receive and file a presentation on a feasibility study for a Federal Inspection Service (FIS) facility at the Long Beach Airport.",
            "type": "AC-Agenda Item",
            "url": "http://longbeach.legistar.com/LegislationDetail.aspx?ID=2860738&GUID=23D033B5-BD92-43F1-9736-248F704C06B8&Options=&Search=",
            "version": 1
        },
        {
            "agenda_num": 4,
            "attachments": [
                {
                    "filename": "Draft AAC Annual Report.pdf",
                    "num": 1,
                    "url": "http://longbeach.legistar.com/View.ashx?M=F&ID=4732698&GUID=6F7FB8F2-67CD-4D88-A0C9-F9819581B8BE"
                }
            ],
            "file_num": "16-029AC",
            "name": "AAC Annual Report",
            "title": "Recommendation to consider the content of the Airport Advisory Commission Annual Report and take action to refer it to the City Council.",
            "type": "AC-Agenda Item",
            "url": "http://longbeach.legistar.com/LegislationDetail.aspx?ID=2861294&GUID=CAF452E2-7117-4CDC-BAF2-B6184343A810&Options=&Search=",
            "version": 1
        },
        {
            "agenda_num": 5,
            "attachments": [
                {
                    "filename": "AAC Monthly Noise Report August 2016.pdf",
                    "num": 1,
                    "url": "http://longbeach.legistar.com/View.ashx?M=F&ID=4730697&GUID=B1B59295-1B31-40B4-97EB-35B0A15EFABD"
                },
                {
                    "filename": "AAC Operations Report October 2016.pdf",
                    "num": 2,
                    "url": "http://longbeach.legistar.com/View.ashx?M=F&ID=4733407&GUID=E10F225A-4C8C-4E05-8F5D-8D927CF916E1"
                },
                {
                    "filename": "AAC Monthly Activity Report September 2016.revised.pdf",
                    "num": 3,
                    "url": "http://longbeach.legistar.com/View.ashx?M=F&ID=4733654&GUID=7CF15A3C-AADA-4CCB-A271-720FF4E37366"
                }
            ],
            "file_num": "16-027AC",
            "name": "AAC Staff Reports October 2016",
            "title": "Recommendation to receive and file monthly Airport Staff Reports for October 2016.",
            "type": "AC-Agenda Item",
            "url": "http://longbeach.legistar.com/LegislationDetail.aspx?ID=2860726&GUID=74C8C35C-0630-490A-9DA0-AB601D324627&Options=&Search=",
            "version": 1
        },
        {
            "agenda_num": 4,
            "attachments": [
                {
                    "filename": "Draft AAC Annual Report.pdf",
                    "num": 1,
                    "url": "http://longbeach.legistar.com/View.ashx?M=F&ID=4732698&GUID=6F7FB8F2-67CD-4D88-A0C9-F9819581B8BE"
                }
            ],
            "file_num": "16-029AC",
            "name": "AAC Annual Report",
            "title": "Recommendation to consider the content of the Airport Advisory Commission Annual Report and take action to refer it to the City Council.",
            "type": "AC-Agenda Item",
            "url": "http://longbeach.legistar.com/LegislationDetail.aspx?ID=2861294&GUID=CAF452E2-7117-4CDC-BAF2-B6184343A810&Options=&Search=",
            "version": 1
        }
    ],
    "coordinates": {
        "address": "Long Beach, CA 90806, USA",
        "latitude": 33.8065036,
        "longitude": -118.1912538
    },
    "datetime": "2016-10-20T18:30:00",
    "id": "FEA0F02F-C707-4700-915D-2CB2EF247F9F-2016-10-24-18-11-59",
    "link": "http://longbeach.legistar.com/Gateway.aspx?M=MD&From=RSS&ID=509077&GUID=FEA0F02F-C707-4700-915D-2CB2EF247F9F",
    "location": "Long Beach Gas & Oil Department\r\n2400 E. Spring St., LB 90806",
    "minutes": "http://longbeach.legistar.com/View.ashx?M=M&ID=509077&GUID=FEA0F02F-C707-4700-915D-2CB2EF247F9F",
    "name": "Airport Advisory Commission",
    "summary": "",
    "title": "Airport Advisory Commission - 10/20/2016 - 6:30 PM"
}
```