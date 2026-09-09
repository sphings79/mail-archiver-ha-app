# Changelog

## 2.0.0 - 2026-09-09

- Follows AmberChest 2.0.0. See the
  [release notes](https://github.com/sphings79/amberchest/releases/tag/v2.0.0) for what changed in the application.

## 1.2.1 - 2026-09-09

- Follows AmberChest 1.2.1. See the
  [release notes](https://github.com/sphings79/amberchest/releases/tag/v1.2.1) for what changed in the application.

## 1.2.0 - 2026-09-09

Follows AmberChest 1.2.0. The
[release notes](https://github.com/sphings79/amberchest/releases/tag/v1.2.0)
have the whole story; the short version:

- **OAuth for Gmail and Microsoft 365**, which no longer accept a password for
  IMAP. Microsoft is connected with a device code, Gmail through a browser.
- **Checking the archive**: every file against the checksum taken when it was
  downloaded, and every folder against the server - is anything missing?
- **Moving an archive** from another instance into this one, files only; the
  index is rebuilt here from the journals.
- **Gmail duplicates** stored once instead of twice, saving half the space on a
  Gmail account.
- **Never delete anything before a date**, for emptying a mailbox to win back
  space on the server while the archive keeps it.
- **Statistics**, a **register** written next to the messages, **disk space
  warnings** and **notifications** to ntfy, Gotify, Discord or Apprise.
- Fixed: changing one setting quietly reset the others, and on a phone the
  whole page scrolled instead of the content.

## 1.1.2 - 2026-09-08

First release of the add-on.

- Runs the published AmberChest image on Home Assistant OS, for `aarch64`
  and `amd64`.
- Ingress: the interface appears in the sidebar, without a login of its own.
- Options for the master password, an optional interface password, a schedule,
  the attachment export and the archive folder.
- Configuration in `/data/config`, archive in `/share/mail-archive`, so both
  survive an update and are part of a Home Assistant backup.
- Follows [AmberChest 1.1.2](https://github.com/sphings79/amberchest/releases/tag/v1.1.2).
