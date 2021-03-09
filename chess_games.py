import sys
import argparse
import json
from workflow import Workflow3, ICON_WEB, web, ICON_ACCOUNT, ICON_INFO, ICON_WARNING

GITHUB_UPDATE_CONF = {'github_slug': 'kinabalu/alfred-chess.com'}
# GitHub Issues
HELP_URL = 'https://github.com/kinabalu/alfred-chess.com/issues'

log = None


def main(wf):

    log.debug(wf.args)
    r = web.get('https://api.chess.com/pub/player/%s/games' % wf.args[0])
    log.debug(r.status_code)

    if r.status_code == 200:
        data = r.json()
        log.debug(json.dumps(data))

        for game in data['games']:
            log.debug(game['url'])
            log.debug(game['rated'])
            log.debug(game['turn'])
            log.debug(game['white'])
            log.debug(game['black'])

            white_player_url = game['white']
            black_player_url = game['black']
            white_player = white_player_url[white_player_url.rfind(
                '/')+1:len(white_player_url)]
            black_player = black_player_url[black_player_url.rfind(
                '/')+1:len(black_player_url)]
            wf.add_item(title='%s v %s and %s to move' %
                        (white_player, black_player, game['turn']),
                        arg=game['url'],
                        copytext=game['fen'])

            # wf.add_item(title=)
            # wf.add_item(title='Username', subtitle=data['username'],
            #             valid=True, icon=ICON_ACCOUNT,
            #             quicklookurl=data['url'])
            # wf.add_item(title='Followers',
            #             subtitle=data['followers'], icon=ICON_INFO)

            # location_text = data['location'] if 'location' in data else 'Not specified'
            # wf.add_item(title='Location',
            #             subtitle=location_text, icon=ICON_INFO)
    else:
        wf.add_item(title='No user found', icon=ICON_WARNING)
    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow3()
    log = wf.logger
    env = wf.alfred_env

    # wf = Workflow3(update_settings=GITHUB_UPDATE_CONF, help_url=HELP_URL)
    sys.exit(wf.run(main))
