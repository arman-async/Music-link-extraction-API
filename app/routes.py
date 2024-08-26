import sys
import asyncio
import requests
from flask import request, jsonify, redirect, url_for
from app.utils import *
from app.config import ConfigFlask 
from app import app

flask_config = ConfigFlask()

@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('document'))


@app.route('/document', methods=['GET'])
def document():
    return f"""
    <h3 style="text-align: center;">Document</h3><ul>
    <li>GET : /search_music<ul><li>query: Google search text</li><li>
    <div>limit: Limit the number of outgoing links ; Defualt:{flask_config.limit}</div>
    </li><li><div>limit-check: Check out some website ; Defualt:{flask_config.limit_check}</div>
    </li><li>Response : JSON<br /><br /><br /></li></ul></li><li>GET: /document<ul>
    <li>Response : HTML</li></ul></li></ul>
    """


@app.route('/search_music', methods=['GET'])
def search_music():
    query = request.args.get('query', type=str)
    limit = request.args.get('limit', default=flask_config.limit, type=int)
    limit_check = request.args.get('limit-check', default=flask_config.limit_check, type=int)

    app.logger.debug(f'rule : {request.url_rule}, query: {query}, limit: {limit}, limit_check: {limit_check}')
    if not query:
        return jsonify({'error': 'Music name is required (query)'}), 400
    
    request_search_kwargs = generate_search_request(query)
    request_search = requests.request(**request_search_kwargs)
    pages_url = extracting_urls_from_google_results(request_search.text)
    coroutines_requests = concurrent_requests(
        [
            {
                'method': 'GET',
                'timeout': config.request_timeout,
                'url': url
            }
            for url in pages_url[:limit_check]
        ]
    )
    coroutines_response = asyncio.run(coroutines_requests)
    music_utls = []
    for response in coroutines_response:
        if response is None: continue
        app.logger.debug(f'URL : {response.url}, Status Code: {response.status_code}')
        urls = extracting_music_url_from_page(response.text)
        if urls: # Fillter None
            music_utls.extend(urls)
        app.logger.debug(f'URL : {response.url}, Total URLs: {len(urls)}')
    
    return jsonify(*music_utls[:limit])
    
    
    
    