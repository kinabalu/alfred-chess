import sys
import argparse
import json
from unicodedata import numeric
from workflow import Workflow3, ICON_WEB, web, ICON_ACCOUNT, ICON_INFO, ICON_WARNING

GITHUB_UPDATE_CONF = {'github_slug': 'kinabalu/alfred-chess.com'}
# GitHub Issues
HELP_URL = 'https://github.com/kinabalu/alfred-chess.com/issues'

log = None

wf = Workflow3()


def get_user():
    return wf.args[0] if len(wf.args) == 1 else None


def main(_):
    if wf.first_run:
        wf.clear_cache()

    user = wf.cached_data('user', max_age=0) if len(
        wf.args) == 0 else None

    if user or len(wf.args) == 1:

        user = wf.args[0] if len(wf.args) == 1 else user

        r = web.get('https://api.chess.com/pub/player/%s/games' % user)

        if r.status_code == 200:
            data = r.json()

            if len(data['games']) == 0:
                wf.add_item(title='No games found for %s' % user)
            else:
                wf.cached_data('user', get_user, max_age=0)
                for game in data['games']:
                    fen = game['fen']
                    move_count = int(fen[fen.rfind(' '):len(fen)])

                    white_player_url = game['white']
                    black_player_url = game['black']
                    white_player = white_player_url[white_player_url.rfind(
                        '/')+1:len(white_player_url)]
                    black_player = black_player_url[black_player_url.rfind(
                        '/')+1:len(black_player_url)]
                    wf.add_item(title='%s v %s and %s to move' %
                                (white_player, black_player, game['turn']),
                                subtitle='A %s game with %d moves so far' % (
                                    ("rated" if game['rated'] else "non-rated"), move_count),
                                arg=game['url'],
                                valid=True,
                                icon='./%s-pawn.png' % game['turn'],
                                copytext=fen)
        else:
            wf.clear_cache()
            wf.add_item(title='No user found', icon=ICON_WARNING)
    else:
        wf.add_item(title='Please specify a user after the command',
                    icon=ICON_WARNING)
    wf.send_feedback()


if __name__ == '__main__':
    log = wf.logger
    sys.exit(wf.run(main))
