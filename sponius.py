#!/usr/bin/python3


import requests
import json
import logging
import dbus
import sys, getopt

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

    full_title = (title + ' ' + artist) \
            .lower() \
            .replace('by', '') \
            .replace('acoustic', '') \
            .replace('-', '') \
            .strip()
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

        hits = [
                    (
                        hit,
                        SequenceMatcher(
                            None,
                            hit['result']['full_title']
                                .lower()
                                .replace('by', '')
                                .replace('acoustic', '')
                                .replace('-', '')
                                .strip(),
                            full_title
                        ).ratio()
                    )
                for section in sections if 'hits' in section
                for hit in section['hits'] if hit['type'] == 'song'
            ]
        if len(hits) == 0:
            return 'Sorry! no lyrics found.'
        hits.sort(key=lambda hit: hit[1], reverse=True)

        top_hit = hits[0]
        if top_hit[1] < 0.5:
            return 'Sorry! no lyrics found.'

        song_url = top_hit[0]['result']['url']
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


def parse_arguments(args):
    try:
        opts, args = getopt.getopt(args, 'ha:s:', [])
    except getopt.GetoptError:
        print('Use sponius -h to find what you want')
        sys.exit(2)

    if not opts and not args:
        return (get_spotify_song_info())

    title = artist = None
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print('SpoNius = Spotify + geNius')
            print('Sponius is a CLI lyrics service which works with Spotify desktop app and genius.com')
            print('Type `sponius` in terminal and instantly get the lyrics of what you\'re listening on spotify. BOOM!')
            print('Type `sponius -s <song title> -a <song artist>` to search for song\'s lyrics')
            print('Or just Type `sponius <song tilte> by <song artist>`')
            print('If songe title or artist is more than one word, use " to surrounding them. Or don\'t! Dosn\'t matter')
            sys.exit()
        elif opt in ('-s', '--song'):
            title = arg
        elif opt in ('-a', '--artist'):
            artist = arg

    if title is None or artist is None:
        if 'by' in args:
            by_index = args.index('by')
            if title is None:
                title = ''
                try:
                    for i in range(by_index):
                        title = title + args[i] + ' '
                    title = title.strip()
                except IndexError:
                    print('You should give the songe name. Use `sponius -h` to see more')
                    sys.exit(2)
            if artist is None:
                artist = ''
                try:
                    for i in range(by_index + 1, len(args)):
                        artist = artist + args[i] + ' '
                except IndexError:
                    print('You should give the songe artist. Use `sponius -h` to see more')
                    sys.exit(2)

    return title, artist


title, artist = parse_arguments(sys.argv[1:])

print(f'\n{title} {artist}\n')

l=lyrics(title, artist)
print(l)
