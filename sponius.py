#!/usr/bin/python3

import requests
import json
import logging
import dbus

from difflib import SequenceMatcher

from bs4 import BeautifulSoup as BS


def get_request(url):
    try:
        r = requests.get(url)
    except requests.exceptions.RequestException as e:
        logging.debug(e)
        raise Exception('Request exception has been occurred')
    if r.status_code != 200:
        raise Exception('Non 200 status code returned')
    return r


def lyrics(title, artist=""):

    full_title = title + ' ' + artist
    try:
        r = get_request(('https://genius.com/api/search/multi?q='
                f'{full_title}'))
    except Exception as e:
        logging.debug(e)
        return 'Request failed'

    try:
        response = json.loads(r.content)['response']
    except ValueError as e:
        logging.debug(e)
        return 'Json decode error'

    try:
        sections = response['sections']
        if len(sections) == 0:
            return 'Sorry! no lyrics found.'

        hits = [hit for hit in sections[0]['hits'] if hit['type'] == 'song']
        if len(hits) == 0:
            return 'Sorry! no lyrics found.'
        hits.sort(
                key=lambda hit:SequenceMatcher(None,
                    hit['result']['full_title'].lower(),
                    full_title.lower()).ratio(),
                reverse=True)

        top_hit = hits[0]
        top_ratio = SequenceMatcher(
                None,
                top_hit['result']['full_title'].lower(),
                full_title.lower()).ratio()
        if top_ratio < 0.7:
            return 'Sorry! no lyrics found.'

        song_url = top_hit['result']['url']
    except Exception as e:
        logging.debug(e)
        return 'Unexpected Json response!'

    try:
        r = get_request(song_url)
    except Exception as e:
        return 'Request failed'
    try:
        soup = BS(r.content, 'html.parser')
    except Exception as e:
        logging.debug(e)
        return 'Sorry! HTML parser failed.'

    try:
        result = soup.find(class_='lyrics').get_text()
    except Exception as e:
        logging.debug(e)
        return 'Unexpected HTML response!'

    return result


def get_spotify_song_info():
    try:
        bus = dbus.SessionBus()
        proxy = bus.get_object(
                    'org.mpris.MediaPlayer2.spotify',
                    '/org/mpris/MediaPlayer2')
        song_data = proxy.Get(
                'org.mpris.MediaPlayer2.Player',
                'Metadata',
                dbus_interface='org.freedesktop.DBus.Properties')
    except Exception as e:
        logging.debug(e)
        raise Exception('DBUS method call failed.')

    try:
        title = str(song_data['xesam:title'])
        artist = ''.join(song_data['xesam:artist'])
    except Exception as e:
        logging.debug(e)
        raise Exception('DBUS paramaters not found.')
    return title, artist


title, artist = get_spotify_song_info()
print('\n' + title + ' ' + artist)

l=lyrics(title, artist)
print(l)

