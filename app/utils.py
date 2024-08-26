from typing import *
import re
import bs4
import requests
import asyncio
import requests_async

from music_api.config import ConfigRequest
config = ConfigRequest()

def extracting_urls_from_google_results(
        response:str
)-> Iterable[str]:
    "return [url, ...]"

    soup = bs4.BeautifulSoup(response, 'html.parser')
    pattern: re.Pattern = re.compile(config.regex_find_url)
    result = []
    for item in soup.find_all('a'):

        href:str = item.get('href')
        is_match = pattern.search(href)
        if is_match:
            try:
                url = is_match.group(1)
            except IndexError:
                continue
            else:
                result.append(url)

    return result


def extracting_music_url_from_page(
        response:str
)-> Tuple[str]:
    'return (music_url, ...)'
    pattern: re.Pattern = re.compile(config.regex_find_music_url)
    matches = pattern.finditer(response)
    return [
        url.group(0)
        for url in matches
    ]



def generate_search_request(query:str)-> Dict:
    return {
        'method': 'GET',
        'url': config.request_url.format(query=query),
        'headers': config.request_headers
    }



async def requests_async_request(**kwargs):
    try:
        return await requests_async.request(**kwargs)
    except requests_async.exceptions.ConnectionError:
        return None
    except requests_async.exceptions.ConnectTimeout:
        return None
    except requests_async.exceptions.ReadTimeout:
        return None
    
async def concurrent_requests(
        requests_dict:List[Dict]
)->List[requests_async.Response]:
    responses = await asyncio.gather(
        *[
            requests_async_request(**requests)
            for requests in requests_dict
        ]
    )
    return responses