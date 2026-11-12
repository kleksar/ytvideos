from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow
from automation.youtube.upload import private_write

target = Path('/private/tmp/scp3008-old-channel-manage-token-v2.json')
if target.exists():
    raise SystemExit('Token already exists; do not overwrite.')
client = Path.home() / '.local/share/story-youtube/yt-videos-client.json'
flow = InstalledAppFlow.from_client_secrets_file(str(client), scopes=['https://www.googleapis.com/auth/youtube.force-ssl'], autogenerate_code_verifier=True)
creds = flow.run_local_server(host='127.0.0.1', port=0, access_type='offline', prompt='consent')
if not creds.refresh_token:
    raise SystemExit('No refresh token returned.')
import json
private_write(target, json.loads(creds.to_json()))
print('Credentials saved; verify channel identity and scope before deletion.')
