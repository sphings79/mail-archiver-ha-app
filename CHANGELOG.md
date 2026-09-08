# Changelog

## 1.1.2 - 2026-09-08

First release of the add-on.

- Runs the published Mail Archiver image on Home Assistant OS, for `aarch64`
  and `amd64`.
- Ingress: the interface appears in the sidebar, without a login of its own.
- Options for the master password, an optional interface password, a schedule,
  the attachment export and the archive folder.
- Configuration in `/data/config`, archive in `/share/mail-archive`, so both
  survive an update and are part of a Home Assistant backup.
- Follows [Mail Archiver 1.1.2](https://github.com/sphings79/mail-archiver/releases/tag/v1.1.2).
