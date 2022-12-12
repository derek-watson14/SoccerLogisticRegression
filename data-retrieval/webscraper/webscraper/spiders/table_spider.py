import scrapy
from pathlib import Path

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from helpers import seasons, league_code_defs

# Serie A: 18 clubs 1988-2004, 20 clubs 2004 - present
# Bundesliga: 18 clubs since 1992/93
# Prem: 20 clubs since inception 92/93
# La Liga: 22 clubs 95-97, 20 clubs 97-today
# Ligue 1: 20 clubs 1970-1997, 18 clubs 1997-2002, 20 clubs 2002-2023, 18 clubs 2023-

# Example page URL
# https://www.transfermarkt.com/laliga/spieltagtabelle/wettbewerb/ES1?saison_id=1996&spieltag=42

class TableSpider(scrapy.Spider):
    name = "tables"

    # Should download 2664 web pages
    def start_requests(self):
        urls = []

        for league in league_code_defs.keys():
            for season in seasons:
                matchdays = (league_code_defs[league]["size"] - 1) * 2
                for matchday in range(1, matchdays+1):
                    url = f"https://www.transfermarkt.com/laliga/spieltagtabelle/wettbewerb/{league}?saison_id={season}&spieltag={matchday}"
                    urls.append(url) 

        requests = 0
        for url in urls:
            requests += 1
            self.log(f"Requests: {requests}")
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        u = response.url
        league = u[u.find("b/")+2:u.find("?")]
        season = u.split("&")[0][-4:]
        matchday = u.split("=")[-1]
        
        base_path = Path(__file__).parent
        file_path = (base_path / f"../../webpages/tables/table-{league}-{season}-md{matchday}.html").resolve()

        with open(file_path, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {file_path}')