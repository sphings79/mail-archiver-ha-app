# Mail Archiver

Backs up IMAP mailboxes to plain `.eml` files on your own storage — read only,
incremental, and with the folder tree preserved. Nothing on the server is
deleted, nothing is marked as read.

## Installation

1. **Settings → Add-ons → Add-on store → ⋮ → Repositories**
2. Add `https://github.com/sphings79/mail-archiver-ha-app`
3. Install **Mail Archiver**
4. Set a **master password** in the configuration tab
5. Start the add-on and open it from the sidebar

## Configuration

```yaml
master_password: choose-something-long
ui_password: ""
cron: "0 3 * * *"
cron_export_attachments: false
archive_path: /share/mail-archive
log_level: info
```

### master_password

Encrypts every mailbox password the add-on stores, using scrypt and
AES-256-GCM. **Keep it.** Without it the configuration cannot be opened again,
and the mailbox passwords in it are gone.

### ui_password

Leave it empty unless you want to reach the interface from outside Home
Assistant. Empty means the add-on answers the Home Assistant sidebar and
refuses everything else, which is the safe default: Home Assistant has already
authenticated whoever gets there.

Set a password and map port `8484` in the network tab, and the interface is
also reachable at `http://<your-home-assistant>:8484` — for a browser on
another machine, or for the desktop app in remote mode.

### cron

Five fields, as usual: minute, hour, day of month, month, weekday.

| Expression | When |
| --- | --- |
| `0 3 * * *` | every night at three |
| `30 */6 * * *` | every six hours, at half past |
| `0 4 * * 0` | Sundays at four |

Empty means the add-on only backs up when you tell it to — from its own
interface, from the
[Mail Archiver integration](https://github.com/sphings79/mail-archiver-home-assistant),
or over MQTT.

### archive_path

Where the `.eml` files go. It has to be a folder Home Assistant keeps:
`/share/…`, `/media/…` or `/backup/…`. Anything else lives inside the container
and is gone with the next update.

A mailbox needs roughly as much space as it uses on the server. Check what you
have before archiving 20 GB onto a 32 GB system disk.

## What is stored where

| Path | Contents | Survives an update |
| --- | --- | --- |
| `/data/config` | encrypted configuration, index database | yes |
| `/share/mail-archive` | the archived mail, one `.eml` per message | yes |

Both are part of a Home Assistant backup, which means your archive is in it as
well. If that makes your backups too large, put the archive on a network share
mounted under `/media` and exclude it there.

## Reaching the add-on from outside

Ingress puts the interface in the sidebar and needs no open port, which is all
most installations need. It is also the reason the add-on refuses everything
that is not the supervisor: there is no login in front of an ingress interface,
so that check is the only thing protecting it.

Two settings open it up, both on the add-on's **Configuration** tab:

1. Set **ui_password** under *Options*. This is the login the interface then
   asks for.
2. Under *Network*, map port `8484` to the host.

The interface is then also at `http://homeassistant.local:8484` — for a browser
on another machine, and for the Mail Archiver desktop app.

The same thing with pictures of both settings, and what to do when it does not
work: [Reaching the add-on from outside](https://github.com/sphings79/mail-archiver-ha-app/blob/main/docs/remote-access.md)
([deutsch](https://github.com/sphings79/mail-archiver-ha-app/blob/main/docs/remote-access.de.md)).

Mapping the port without setting the password changes nothing: the add-on goes
on refusing every request that did not come from the supervisor, and the log
says `reachable through the sidebar, and only from the supervisor`.

### Moving an archive into the add-on

This is what the port is for in practice. An archive that grew up in the
desktop app moves over in three steps:

1. Set `ui_password` and map the port as above, then restart the add-on
2. In the add-on, create the account with the same address
3. In the desktop app, **Move** on that account, address
   `http://homeassistant.local:8484`, the interface password, pick the account

The files travel and the add-on rebuilds its index from the journals in them.
An interrupted transfer is harmless — run it again and only what is missing
goes over. Nothing is deleted on the desktop side.

## Home Assistant

The add-on brings the interface into the sidebar, phone included. For sensors,
automations and a Lovelace card there are two more ways:

- The [Mail Archiver integration](https://github.com/sphings79/mail-archiver-home-assistant)
  from HACS: a device per mailbox, with a backup button and a card. Point it at
  host `localhost` and port `8484` — that only works with an interface password
  and the port mapped.
- **MQTT**, configured in the add-on itself under *Home Assistant*: the same
  numbers, pushed to your broker, discovered by Home Assistant automatically.
  This needs no open port at all.

## Troubleshooting

**The add-on will not start.** Look at the log: without a master password it
refuses to do anything, because it could not open its own configuration.

**"Only reachable through Home Assistant".** That is the add-on doing its job:
without an interface password it answers the supervisor only. Set one to open
the port.

**The archive is missing after an update.** `archive_path` pointed somewhere
inside the container. Use a folder below `/share`, `/media` or `/backup`.

**PDF export is unavailable.** It needs Chromium, which the image contains — if
it fails anyway, the log says why.

## Three projects, one archive

| | What it is |
| --- | --- |
| [Mail Archiver](https://github.com/sphings79/mail-archiver) | The application: desktop app for macOS, Windows and Linux, plus the Docker container this add-on runs |
| [Mail Archiver Integration](https://github.com/sphings79/mail-archiver-home-assistant) | Home Assistant integration from HACS: a device per mailbox, sensors, a backup button and a Lovelace card |
| [Home Assistant App (Add-on)](https://github.com/sphings79/mail-archiver-ha-app) | This one: Mail Archiver on Home Assistant OS, in the sidebar through ingress |

## Support

Issues about the add-on packaging:
[mail-archiver-ha-app](https://github.com/sphings79/mail-archiver-ha-app/issues).
Issues about Mail Archiver itself:
[mail-archiver](https://github.com/sphings79/mail-archiver/issues).

If it is useful to you: a ⭐ on
[the add-on](https://github.com/sphings79/mail-archiver-ha-app) or
[Mail Archiver](https://github.com/sphings79/mail-archiver) helps, and there is
a [coffee](https://buymeacoffee.com/sphings) button as well.
