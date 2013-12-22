#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket
import urllib
import urllib2
import xbmcplugin
import xbmcaddon
import xbmcgui
import random
import sys
import os
import re

addon = xbmcaddon.Addon()
socket.setdefaulttimeout(60)
pluginhandle = int(sys.argv[1])
addonID = addon.getAddonInfo('id')
iconRTL = xbmc.translatePath('special://home/addons/'+addonID+'/icon.png')
iconRTL2 = xbmc.translatePath('special://home/addons/'+addonID+'/iconRTL2.png')
iconVOX = xbmc.translatePath('special://home/addons/'+addonID+'/iconVOX.png')
iconRTLNitro = xbmc.translatePath('special://home/addons/'+addonID+'/iconRTLNitro.png')
iconSuperRTL = xbmc.translatePath('special://home/addons/'+addonID+'/iconSuperRTL.png')
iconNTV = xbmc.translatePath('special://home/addons/'+addonID+'/iconNTV.png')
opener = urllib2.build_opener()
userAgent = "Mozilla/5.0 (Windows NT 5.1; rv:24.0) Gecko/20100101 Firefox/24.0"
opener.addheaders = [('User-Agent', userAgent)]

useThumbAsFanart = addon.getSetting("useThumbAsFanart") == "true"
forceView = addon.getSetting("forceView") == "true"
viewID = str(addon.getSetting("viewID"))
site1 = addon.getSetting("site1") == "true"
site2 = addon.getSetting("site2") == "true"
site3 = addon.getSetting("site3") == "true"
site4 = addon.getSetting("site4") == "true"
site5 = addon.getSetting("site5") == "true"
site6 = addon.getSetting("site6") == "true"
urlMainRTL = "http://rtl-now.rtl.de"
urlMainRTL2 = "http://rtl2now.rtl2.de"
urlMainVOX = "http://www.voxnow.de"
urlMainRTLNitro = "http://www.rtlnitronow.de"
urlMainSuperRTL = "http://www.superrtlnow.de"
urlMainNTV = "http://www.n-tvnow.de"


def index():
    if site1:
        addDir(translation(30002), urlMainRTL, "listChannel", iconRTL)
    if site2:
        addDir(translation(30003), urlMainRTL2, "listChannel", iconRTL2)
    if site3:
        addDir(translation(30004), urlMainVOX, "listChannel", iconVOX)
    if site4:
        addDir(translation(30005), urlMainRTLNitro, "listChannel", iconRTLNitro)
    if site5:
        addDir(translation(30006), urlMainSuperRTL, "listChannel", iconSuperRTL)
    if site6:
        addDir(translation(30007), urlMainNTV, "listChannel", iconNTV)
    xbmcplugin.endOfDirectory(pluginhandle)


def listChannel(urlMain, thumb):
    if urlMain == urlMainRTL:
        addDir(translation(30015), urlMain+"/sendung_a_z.php", "listShowsThumb", thumb)
        addDir(translation(30016), urlMain+"/newsuebersicht.php", "listShowsThumb", thumb)
    elif urlMain in [urlMainVOX, urlMainNTV, urlMainRTLNitro]:
        addDir(translation(30014), urlMain+"/sendung_a_z.php", "listShowsThumb", thumb)
    else:
        addDir(translation(30014), urlMain, "listShowsNoThumb", thumb)
    addDir(translation(30017), urlMain, "listVideosNew", thumb, "", "tipplist")
    addDir(translation(30018), urlMain, "listVideosNew", thumb, "", "newlist")
    addDir(translation(30019), urlMain, "listVideosNew", thumb, "", "top10list")
    addDir(translation(30020), urlMain, "listVideosNew", thumb, "", "topfloplist")
    xbmcplugin.endOfDirectory(pluginhandle)


def listShowsThumb(urlMain):
    xbmcplugin.addSortMethod(pluginhandle, xbmcplugin.SORT_METHOD_LABEL)
    content = opener.open(urlMain).read()
    spl = content.split('<div class="m03medium"')
    for i in range(1, len(spl), 1):
        entry = spl[i]
        match = re.compile('<h2>(.+?)</h2>', re.DOTALL).findall(entry)
        title = cleanTitle(match[0])
        match = re.compile('href="(.+?)"', re.DOTALL).findall(entry)
        url = match[0]
        if url.startswith("/"):
            url = url[1:]
        if "/" in url:
            url = url[:url.find("/")]+".php"
        url = urlMain[:urlMain.rfind("/")+1]+url
        match = re.compile('src="(.+?)"', re.DOTALL).findall(entry)
        thumb = match[0].replace("/216x122/", "/864x488/")
        if 'class="m03date">FREE' in entry or 'class="m03date">NEW' in entry:
            addDir(title, url, 'listVideos', thumb)
    xbmcplugin.endOfDirectory(pluginhandle)


def listShowsNoThumb(urlMain, thumb):
    xbmcplugin.addSortMethod(pluginhandle, xbmcplugin.SORT_METHOD_LABEL)
    content = opener.open(urlMain).read()
    spl = content.split('<div class="seriennavi')
    for i in range(1, len(spl), 1):
        entry = spl[i]
        match = re.compile('title="(.+?)"', re.DOTALL).findall(entry)
        if match:
            title = cleanTitle(match[0]).replace(" online ansehen", "")
            match = re.compile('href="(.+?)"', re.DOTALL).findall(entry)
            url = urlMain+match[0]
            if '>FREE<' in entry or '>NEW<' in entry:
                addDir(title, url, 'listVideos', thumb)
    xbmcplugin.endOfDirectory(pluginhandle)


def listVideos(urlMain, thumb, args=""):
    ajaxUrl = ""
    if not args:
        content = opener.open(urlMain).read()
        matchUrl = re.compile('xajaxRequestUri="(.+?)"', re.DOTALL).findall(content)
        ajaxUrl = matchUrl[0]
        matchParams = re.compile("<select onchange=\"xajax_show_top_and_movies.+?'(.+?)','(.+?)','(.+?)','(.+?)','(.+?)','(.+?)','(.+?)'", re.DOTALL).findall(content)
        if matchParams:
            args = "xajax=show_top_and_movies&xajaxr=&xajaxargs[]=0&xajaxargs[]="+matchParams[0][0]+"&xajaxargs[]="+matchParams[0][1]+"&xajaxargs[]="+matchParams[0][2]+"&xajaxargs[]="+matchParams[0][3]+"&xajaxargs[]="+matchParams[0][4]+"&xajaxargs[]="+matchParams[0][5]+"&xajaxargs[]="+matchParams[0][6]
            content = opener.open(ajaxUrl, args).read()
    else:
        content = opener.open(urlMain, args).read()
    spl = content.split('<div class="line')
    for i in range(1, len(spl), 1):
        entry = spl[i]
        if 'class="minibutton">kostenlos<' in entry:
            match = re.compile('title=".+?">(.+?)<', re.DOTALL).findall(entry)
            if match:
                title = cleanTitle(match[0])
                match = re.compile('class="time"><div style=".+?">.+?</div>(.+?)<', re.DOTALL).findall(entry)
                date = ""
                if match:
                    date = match[0].strip()
                    if " " in date:
                        date = date.split(" ")[0]
                    if "." in date:
                        date = date[:date.rfind(".")]
                    title = date+" - "+title
                match = re.compile('href="(.+?)"', re.DOTALL).findall(entry)
                url = urlMain[:urlMain.rfind("/")]+match[0].replace("&amp;", "&")
                addLink(title, url, 'playVideo', thumb)
    matchParams = re.compile("<a class=\"sel\"  >.+?xajax_show_top_and_movies\\((.+?),'(.+?)','(.+?)','(.+?)','(.+?)','(.+?)','(.+?)','(.+?)'", re.DOTALL).findall(content)
    if matchParams:
        args = "xajax=show_top_and_movies&xajaxr=&xajaxargs[]="+matchParams[0][0]+"&xajaxargs[]="+matchParams[0][1]+"&xajaxargs[]="+matchParams[0][2]+"&xajaxargs[]="+matchParams[0][3]+"&xajaxargs[]="+matchParams[0][4]+"&xajaxargs[]="+matchParams[0][5]+"&xajaxargs[]="+matchParams[0][6]+"&xajaxargs[]="+matchParams[0][7]
        if ajaxUrl:
            ajaxUrlNext = ajaxUrl
        else:
            ajaxUrlNext = urlMain
        addDir(translation(30001), ajaxUrlNext, "listVideos", thumb, args)
    xbmcplugin.endOfDirectory(pluginhandle)


def listVideosNew(urlMain, type):
    xbmcplugin.addSortMethod(pluginhandle, xbmcplugin.SORT_METHOD_LABEL)
    content = opener.open(urlMain).read()
    content = content[content.find('<div id="'+type+'"'):]
    if type == "tipplist":
        if urlMain == urlMainNTV:
            content = content[:content.find("iv class=\"contentrow contentrow3\"><div class='contentrow_headline'")]
        else:
            content = content[:content.find("<div class='contentrow_headline'")]
        spl = content.split('<div class="m03medium"')
    else:
        content = content[:content.find('<div class="roundfooter"></div>')]
        spl = content.split('<div class="top10 ')
    for i in range(1, len(spl), 1):
        entry = spl[i]
        match1 = re.compile('<h2>(.+?)</h2>', re.DOTALL).findall(entry)
        match2 = re.compile('alt="(.+?)"', re.DOTALL).findall(entry)
        if match1:
            title = cleanTitle(match1[0])
        elif match2:
            title = cleanTitle(match2[0])
        title = title.replace("<br>", ": ")
        match = re.compile('href="(.+?)"', re.DOTALL).findall(entry)
        url = match[0].replace("&amp;", "&")
        if not urlMain in url:
            url = urlMain+url
        match = re.compile('src="(.+?)"', re.DOTALL).findall(entry)
        thumb = match[0].replace("/216x122/", "/864x488/")
        if 'class="m03date">FREE' in entry or 'FREE |' in entry:
            addLink(title, url, 'playVideo', thumb)
    xbmcplugin.endOfDirectory(pluginhandle)


def playVideo(urlMain):
    content = opener.open(urlMain).read()
    match = re.compile("data:'(.+?)'", re.DOTALL).findall(content)
    urlMain = urlMain[urlMain.find("//")+2:]
    urlMain = urlMain[:urlMain.find("/")]
    url = "http://"+urlMain+urllib.unquote(match[0])
    content = opener.open(url).read()
    match = re.compile('<filename.+?><(.+?)>', re.DOTALL).findall(content)
    url = match[0].replace("![CDATA[", "")
    matchRTMPE = re.compile('rtmpe://(.+?)/(.+?)/(.+?)]', re.DOTALL).findall(url)
    matchHDS = re.compile('http://(.+?)/(.+?)/(.+?)/(.+?)/(.+?)\\?', re.DOTALL).findall(url)
    finalUrl = ""
    if matchRTMPE:
        finalUrl = "rtmpe://"+matchRTMPE[0][0]+"/"+matchRTMPE[0][1]+"/ playpath=mp4:"+matchRTMPE[0][2]+" swfVfy=1 swfUrl=http://"+urlMain+"/includes/vodplayer.swf app="+matchRTMPE[0][1]+"/_definst_ pageUrl=http://"+urlMain+"/p/"
    elif matchHDS:
        finalUrl = "rtmpe://fms-fra"+str(random.randint(1, 34))+".rtl.de/"+matchHDS[0][2]+"/ playpath=mp4:"+matchHDS[0][4].replace(".f4m", "")+" swfVfy=1 swfUrl=http://"+urlMain+"/includes/vodplayer.swf app="+matchHDS[0][2]+"/_definst_ pageUrl=http://"+urlMain+"/p/"
    if finalUrl:
        listitem = xbmcgui.ListItem(path=finalUrl)
        xbmcplugin.setResolvedUrl(pluginhandle, True, listitem)


def queueVideo(url, name):
    playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    listitem = xbmcgui.ListItem(name)
    playlist.add(url, listitem)


def translation(id):
    return addon.getLocalizedString(id).encode('utf-8')


def cleanTitle(title):
    title = title.replace("u0026", "&").replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&").replace("&#039;", "'").replace("&quot;", "\"").replace("&szlig;", "ß").replace("&ndash;", "-")
    title = title.replace("&Auml;", "Ä").replace("&Uuml;", "Ü").replace("&Ouml;", "Ö").replace("&auml;", "ä").replace("&uuml;", "ü").replace("&ouml;", "ö")
    title = title.replace("\\'", "'").strip()
    return title


def parameters_string_to_dict(parameters):
    paramDict = {}
    if parameters:
        paramPairs = parameters[1:].split("&")
        for paramsPair in paramPairs:
            paramSplits = paramsPair.split('=')
            if (len(paramSplits)) == 2:
                paramDict[paramSplits[0]] = paramSplits[1]
    return paramDict


def addLink(name, url, mode, iconimage, desc="", duration="", date=""):
    u = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={"Title": name, "Plot": desc, "Aired": date, "Duration": duration, "Episode": 1})
    liz.setProperty('IsPlayable', 'true')
    if useThumbAsFanart and iconimage not in [iconRTL, iconRTL2, iconVOX, iconRTLNitro, iconSuperRTL, iconNTV]:
        liz.setProperty("fanart_image", iconimage)
    entries = []
    entries.append((translation(30021), 'RunPlugin(plugin://'+addonID+'/?mode=queueVideo&url='+urllib.quote_plus(u)+'&name='+urllib.quote_plus(name)+')',))
    liz.addContextMenuItems(entries)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz)
    return ok


def addDir(name, url, mode, iconimage, args="", type=""):
    u = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&thumb="+urllib.quote_plus(iconimage)+"&args="+urllib.quote_plus(args)+"&type="+urllib.quote_plus(type)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={"Title": name})
    if useThumbAsFanart and iconimage not in [iconRTL, iconRTL2, iconVOX, iconRTLNitro, iconSuperRTL, iconNTV]:
        liz.setProperty("fanart_image", iconimage)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
    return ok

params = parameters_string_to_dict(sys.argv[2])
mode = urllib.unquote_plus(params.get('mode', ''))
url = urllib.unquote_plus(params.get('url', ''))
name = urllib.unquote_plus(params.get('name', ''))
args = urllib.unquote_plus(params.get('args', ''))
thumb = urllib.unquote_plus(params.get('thumb', ''))
type = urllib.unquote_plus(params.get('type', ''))

if mode == 'listChannel':
    listChannel(url, thumb)
elif mode == 'listVideos':
    listVideos(url, thumb, args)
elif mode == 'listVideosNew':
    listVideosNew(url, type)
elif mode == 'listShowsThumb':
    listShowsThumb(url)
elif mode == 'listShowsNoThumb':
    listShowsNoThumb(url, thumb)
elif mode == 'playVideo':
    playVideo(url)
elif mode == "queueVideo":
    queueVideo(url, name)
else:
    index()
