import sys
from workflow import Workflow3, ICON_WEB, web, ICON_ACCOUNT, ICON_INFO, ICON_WARNING

GITHUB_UPDATE_CONF = {'github_slug': 'kinabalu/alfred-chess.com'}
# GitHub Issues
HELP_URL = 'https://github.com/kinabalu/alfred-chess.com/issues'

log = None


def main(wf):
    r = web.get('https://api.chess.com/pub/player/%s' % wf.args[0])

    if r.status_code == 200:
        data = r.json()
        log.debug(data)
        # wf.add_item(title=)
        wf.add_item(title='Username', subtitle=data['username'],
                    valid=True, icon=ICON_ACCOUNT,
                    arg=data['url'],
                    quicklookurl=data['url'])
        wf.add_item(title='Followers',
                    subtitle=data['followers'], icon=ICON_INFO)

        location_text = data['location'] if 'location' in data else 'Not specified'
        wf.add_item(title='Location',
                    subtitle=location_text, icon=ICON_INFO)
    else:
        wf.add_item(title='No user found', icon=ICON_WARNING)
    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow3()
    log = wf.logger
    sys.exit(wf.run(main))
