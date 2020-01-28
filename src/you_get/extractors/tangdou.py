#!/usr/bin/env python

from ..common import *
from ..extractor import VideoExtractor

import json

class TangDou(VideoExtractor):
    name = "TangDou"

    stream_types = [
        {"id": "original"}
    ]
    @staticmethod
    def encodeapiurl(h5url):
        """
        str -> str
        
        Get the api url of video.
        """
        API_ENDPOINT = "https://api-h5.tangdou.com/sample/share/main?vid={vid}"
        for entry in h5url.split("?")[1].split("&"):
            key , value = entry.split("=")
            if key == "vid":
                return API_ENDPOINT.format(vid=value)

    def prepare(self, **kwargs):
    
        self.referer = self.url
        
        content = get_content(self.encodeapiurl(self.url), headers={"Referer":self.referer})
        content_json = json.loads(content)
        
        self.title = content_json["data"]["title"]
        
        self.streams["original"] = {"url": content_json["data"]["play_url"]}
        
    def extract(self, **kwargs):
        for i in self.streams:
            # for each available stream
            s = self.streams[i]
            # fill in 'container' field and 'size' field (optional)
            _, __, s['size'] = url_info(s['url'], headers={"Referer":self.referer})
            
            # The Content-Type of response is "video/mp4;charset=UTF-8"
            # Just define it manually 
            s['container'] = "mp4"
            
            # 'src' field is a list of processed urls for direct downloading
            # usually derived from 'url'
            s['src'] = [s['url']]

site = TangDou()
download = site.download_by_url
download_playlist = playlist_not_supported('TangDou')