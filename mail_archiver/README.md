# Mail Archiver

Backs up IMAP mailboxes to plain `.eml` files on your own storage - read only,
incremental, with the folder tree preserved. Nothing on the server is deleted,
nothing is marked as read.

- **In the sidebar.** Ingress puts the interface inside Home Assistant, so it
  works in the browser and in the Home Assistant app.
- **No second login.** Home Assistant has already authenticated whoever gets
  there; the add-on answers the supervisor and nobody else.
- **In your backups.** Configuration and archive live where the supervisor
  keeps them, so they survive updates and land in a Home Assistant backup.
- **On a schedule.** A cron expression in the options is all it needs.

Set a master password under *Configuration*, start the add-on, and open **Mail
Archiver** from the sidebar. The [documentation](DOCS.md) has the details, and
the [project page](https://github.com/sphings79/mail-archiver-ha-app) has the
rest.
