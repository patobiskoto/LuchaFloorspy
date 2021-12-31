import cfscrape
from config import config
from bs4 import BeautifulSoup

class OpenseaQuerries:
    async def findAFloor(nbAttr):
        scraper = cfscrape.create_scraper()
        opensea_url = "https://opensea.io/collection/luchadores-io?search[numericTraits][0][name]=Attributes&search[numericTraits][0][ranges][0][max]="+nbAttr+"&search[numericTraits][0][ranges][0][min]="+nbAttr+"&search[sortAscending]=true&search[sortBy]=PRICE&search[toggles][0]=BUY_NOW"

        resp = scraper.get(url=opensea_url)
        bswebpage = BeautifulSoup(resp.content, "html.parser")

        for assetCardFooter in bswebpage.findAll('div',{'class':'AssetCardFooter--price'}):
            for assetCardFooterPriceAmount in assetCardFooter.findAll('div', {'class':'AssetCardFooter--price-amount'}):
                return assetCardFooterPriceAmount.findAll('div', {'class':'Price--amount'})[0].text.strip()
