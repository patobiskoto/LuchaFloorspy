import requests
from config import config
from bs4 import BeautifulSoup
from opensea import OpenseaAPI

class OpenseaQuerries:
    async def find_a_floor(nbAttr):
        print("-- request for " + str(nbAttr) + "T")
        headers = {'X-Api-Key':str(config['opensea_api_key']),'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:94.0) Gecko/20100101 Firefox/94.0'}
        opensea_url = "https://opensea.io/collection/luchadores-io?search[numericTraits][0][name]=Attributes&search[numericTraits][0][ranges][0][max]="+nbAttr+"&search[numericTraits][0][ranges][0][min]="+nbAttr+"&search[sortAscending]=true&search[sortBy]=PRICE&search[toggles][0]=BUY_NOW"
        
        resp = requests.get(url=opensea_url, headers=headers)
        if resp.status_code != 200:
            print("Error. status_code=" + str(resp.status_code))
            return
        bswebpage = BeautifulSoup(resp.text, "html.parser")

        for assetCardFooter in bswebpage.findAll('div',{'class':'AssetCardFooter--price'}):
            for assetCardFooterPriceAmount in assetCardFooter.findAll('div', {'class':'AssetCardFooter--price-amount'}):
                floor = assetCardFooterPriceAmount.findAll('div', {'class':'Price--amount'})[0].text.strip()
                print("-- floor = " + floor)
                return floor

    async def get_collection_stats(slug):
        api = OpenseaAPI(apikey=str(config['opensea_api_key']))
        return api.collection_stats(collection_slug=slug)

