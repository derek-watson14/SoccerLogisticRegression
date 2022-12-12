import scrapy
from pathlib import Path

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from helpers import seasons, league_code_defs

class StadiumsSpider(scrapy.Spider):
    name = "stadiums"

    def start_requests(self):
        urls = []    
        seasons.insert(0, 2004)
        for league in league_code_defs.keys():
            for season in seasons:
                url = f"https://www.transfermarkt.com/laliga/besucherzahlen/wettbewerb/{league}/plus/1?saison_id={season}"
                urls.append(url) 
                
    
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        season = response.url[-4:]
        league = response.url.split("/")[-3]
        
        base_path = Path(__file__).parent
        file_path = (base_path / f"../../webpages/stadiums/stadiums-{league}-{season}.html").resolve()

        with open(file_path, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file at {file_path}')