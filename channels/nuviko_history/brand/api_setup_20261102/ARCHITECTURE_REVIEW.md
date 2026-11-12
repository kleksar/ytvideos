# API architecture review — 2 November 2026

Local credentials were compared by client ID without exposing credential values. Both Paper Detour upload/manage tokens and source History upload/manage tokens reference the same installed OAuth client in project `yt-videos-513009`. They remain separate per-channel credential files. This audit does not refresh tokens or prove current API validity.

The latest user screenshot shows `403 access_denied`: app Nuviko is Testing and the destination owner `glavred.journalist@gmail.com` is not developer-approved for this app. This is separate from the earlier reported temporary identity-verification rate limit.

Cloud IAM read under default signed-in account `uwilleer@gmail.com` reports missing `resourcemanager.projects.get` and `resourcemanager.projects.getIamPolicy`. Project ownership has not been established. No access request was submitted and no IAM/OAuth settings were changed.

Recommended architecture: retain the existing Cloud project and OAuth client; establish control through the user's confirmed primary Google account using IAM if necessary. Keep separate credentials and explicit channel IDs for Paper and destination Nuviko. Archiving the source YouTube channel is not itself a reason to replace the OAuth client. A new Cloud project would require fresh authorizations; do not repoint current tokens to another client.

Pending: confirm primary account, inspect project ownership, review proposed IAM change if any, add destination owner to test users with required confirmation, then reauthorize and verify channel ID/scopes. No transfer, revocation, new grant, upload or publication has been performed.

Sources: https://developers.google.com/identity/protocols/oauth2/production-readiness/overview and https://docs.cloud.google.com/resource-manager/docs/access-control-proj .

## Resolved ownership

The user confirmed `google@kleksar.me` as their primary personal Google account. After using the visible Cloud account switcher, IAM for `YT Videos` (`yt-videos-513009`) showed this same account as `Owner (Legacy)`. The earlier denial was specific to `uwilleer@gmail.com`. No project transfer or new IAM grant is required. Screenshot: `primary_account_project_owner.jpg`. No IAM or OAuth access changes were made.
