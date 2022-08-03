"""
HTTP client with persistent session.

It reduces the speed of requests due to the fact that you do not need to create a session every time
"""

import aiohttp
import logging
import http
from pydantic import parse_raw_as

from typing import List
from components.common import Singleton
from models.item import ItemList, Item


class PersistentClient(object, metaclass=Singleton):
    """Client with persistent session class."""

    def __init__(self):
        """Initialize persistent client."""
        self._session: aiohttp.ClientSession | None = None

    @property
    def session(self) -> aiohttp.ClientSession:
        """Get session object if exists and create if not exists."""
        if not self._session:
            self._session = aiohttp.ClientSession()
        return self._session

    @classmethod
    def make_url(cls, base_url: str, query_params: dict) -> str:
        """Create url from base url and dict with query parameters."""
        params_list = []
        for i_key, i_val in query_params.items():
            params_list.append('{key}={value}'.format(key=i_key, value=i_val))
        params_string = '&'.join(params_list)
        return '{base}?{params}'.format(base=base_url, params=params_string)

    async def get(self, endpoint: str, query_parameters: dict | None = None) -> ItemList:
        """Get request."""
        if query_parameters:
            url = self.make_url(endpoint, query_parameters)
        else:
            url = endpoint
        fetched = await self._fetch("get", url)
        return ItemList(item_list=parse_raw_as(List[Item], fetched))

    async def close(self):
        """Close session."""
        await self.session.close()
        self._session = None

    async def _fetch(self, method: str, url: str) -> str:
        """Fetch data."""
        try:
            response = await self.session.request(method, url)
            if response.status >= http.HTTPStatus.BAD_REQUEST:
                raise Exception('Bad response. Status code: {code}'.format(code=response.status))
            return await response.text()
        except Exception as ex:
            logging.info(str(ex))
            raise
