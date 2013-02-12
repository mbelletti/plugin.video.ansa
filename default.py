import os
import sys
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import urllib
import urlparse
import time
from resources.lib.ansa import Ansa


# plugin constants
__plugin__ = "plugin.video.ansa"
__author__ = "Nightflyer"

Addon = xbmcaddon.Addon(id=__plugin__)

# plugin handle
handle = int(sys.argv[1])

# utility functions
def parameters_string_to_dict(parameters):
    ''' Convert parameters encoded in a URL to a dict. '''
    paramDict = dict(urlparse.parse_qsl(parameters[1:]))
    return paramDict
 
def addDirectoryItem(parameters, li):
    url = sys.argv[0] + '?' + urllib.urlencode(parameters)
    return xbmcplugin.addDirectoryItem(handle=handle, url=url, 
        listitem=li, isFolder=True)

def addLinkItem(url, li):
    return xbmcplugin.addDirectoryItem(handle=handle, url=url, 
        listitem=li, isFolder=False)

# UI builder functions
def show_root_folder():
    ansa = Ansa()
    items = ansa.getChannels()

    for item in items:
        liStyle=xbmcgui.ListItem(item["title"])
        addDirectoryItem({"url": item["url"]}, liStyle)
    xbmcplugin.endOfDirectory(handle=handle, succeeded=True)

def show_video_files(url):
    ansa = Ansa()
    items = ansa.getVideoByChannel(url)
    for item in items:
        liStyle=xbmcgui.ListItem(item["title"], thumbnailImage=item["thumb"])
        liStyle.setInfo(type="video",
            infoLabels={"Tvshowtitle": item["channel"], 
                        "Title": item["title"],
                        "Date": time.strftime("%d.%m.%Y", item["date"])
                        })
        addLinkItem(item["url"], liStyle)
    #xbmcplugin.addSortMethod(handle, xbmcplugin.SORT_METHOD_DATE)
    xbmcplugin.endOfDirectory(handle=handle, succeeded=True)


# parameter values
params = parameters_string_to_dict(sys.argv[2])
url = str(params.get("url", ""))

if url == "":
    show_root_folder()
else:
    show_video_files(url)

