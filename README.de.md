<div align="center">
  <img src="assets/banner.svg" alt="Mail Archiver als Home-Assistant-Add-on: die Mail-Sicherung läuft auf Home Assistant OS und erscheint per Ingress in der Seitenleiste" width="100%">

  # Mail Archiver — IMAP-Mail-Sicherung als Home-Assistant-Add-on

  **Postfächer in Dateien sichern, die dir gehören — aus Home Assistant heraus.**
  Add-on-Repository für [Mail Archiver — The Mail Backup Solution](https://github.com/sphings79/mail-archiver):
  nur lesend, inkrementell, ohne auf dem Server zu löschen oder als gelesen zu markieren.

  [![Add-on](https://img.shields.io/badge/Home%20Assistant-Add--on-41BDF5?style=for-the-badge)](https://www.home-assistant.io/addons/)
  [![Version](https://img.shields.io/badge/Version-1.2.0-7C7CF5?style=for-the-badge)](https://github.com/sphings79/mail-archiver/releases)
  [![Architekturen](https://img.shields.io/badge/arch-aarch64%20%7C%20amd64-3ddc97?style=for-the-badge)](#voraussetzungen)
  [![Lizenz](https://img.shields.io/badge/Lizenz-AGPL--3.0-e0457b?style=for-the-badge)](LICENSE)

  [English](README.md) · **Deutsch**
</div>

## Inhalt

- [Was das Add-on macht](#was-das-add-on-macht)
- [Drei Projekte, ein Archiv](#drei-projekte-ein-archiv)
- [Installation](#installation)
- [Konfiguration](#konfiguration)
- [Wo die Daten liegen](#wo-die-daten-liegen)
- [In der Seitenleiste](#in-der-seitenleiste)
- [Wie Updates ablaufen](#wie-updates-ablaufen)
- [Sensoren und Automatisierungen](#sensoren-und-automatisierungen)
- [Voraussetzungen](#voraussetzungen)
- [Fehlersuche](#fehlersuche)
- [FAQ](#faq)
- [Credits](#credits)
- [Hinweis](#hinweis)
- [Lizenz](#lizenz)

## Was das Add-on macht

Mail Archiver kopiert IMAP-Postfächer in schlichte `.eml`-Dateien, eine je
Nachricht, im Ordnerbaum des Postfachs. Ordner werden nur lesend geöffnet und
Nachrichten mit `BODY.PEEK` geholt — es wird nichts gelöscht und nichts als
gelesen markiert. Dieses Add-on betreibt das auf Home Assistant OS:

- **In der Seitenleiste.** Ingress holt die Oberfläche nach Home Assistant
  hinein, im Browser und in der Home-Assistant-App auf dem Handy.
- **Kein zweiter Login.** Home Assistant authentifiziert den Benutzer, bevor die
  Anfrage ankommt; das Add-on antwortet nur dem Supervisor.
- **Mit Home Assistant gesichert.** Konfiguration und Archiv liegen dort, wo der
  Supervisor sie aufhebt — sie überleben Updates und landen im Backup.
- **Nach Zeitplan.** Ein Cron-Ausdruck in den Optionen genügt.

## Drei Projekte, ein Archiv

| | Was es ist |
| --- | --- |
| [**Mail Archiver**](https://github.com/sphings79/mail-archiver) | Die Anwendung selbst: Desktop-App für macOS, Windows und Linux, dazu der Docker-Container, den dieses Add-on betreibt |
| [**Mail Archiver Integration**](https://github.com/sphings79/mail-archiver-home-assistant) | Home-Assistant-Integration aus HACS: ein Gerät je Postfach, Sensoren, ein Knopf zum Sichern und eine Lovelace-Karte |
| **Home Assistant App (Addon)** (hier) | Dieses Repository: Mail Archiver unter Home Assistant OS, per Ingress in der Seitenleiste |

Add-on und Integration ergänzen sich: das Add-on betreibt die Instanz, die
Integration macht Entitäten daraus.

## Installation

<img src="assets/install.svg" alt="Vier Installationsschritte: Add-on-Store öffnen, dieses Repository hinzufügen, Mail Archiver installieren und Master-Passwort setzen, starten" width="100%">

1. **Einstellungen → Add-ons → Add-on-Store → ⋮ → Repositories**
2. `https://github.com/sphings79/mail-archiver-ha-app` hinzufügen
3. **Mail Archiver** installieren
4. Unter *Konfiguration* ein **Master-Passwort** setzen
5. Starten, dann **Mail Archiver** in der Seitenleiste öffnen

[![Home Assistant öffnen und den Add-on-Store mit diesem Repository anzeigen.](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Fsphings79%2Fmail-archiver-ha-app)

## Konfiguration

```yaml
master_password: irgendwas-langes
ui_password: ""
cron: "0 3 * * *"
cron_export_attachments: false
archive_path: /share/mail-archive
log_level: info
```

| Option | Bedeutung |
| --- | --- |
| `master_password` | Verschlüsselt alle gespeicherten Postfach-Passwörter, mit scrypt und AES-256-GCM. **Aufbewahren** — ohne dieses Passwort lässt sich die Konfiguration nicht mehr öffnen. |
| `ui_password` | Nur nötig, um die Oberfläche außerhalb von Home Assistant zu erreichen. Leer heißt: nur über die Seitenleiste. |
| `cron` | Fünf Felder: Minute, Stunde, Tag, Monat, Wochentag. `0 3 * * *` ist jede Nacht um drei. Leer heißt kein Zeitplan. |
| `cron_export_attachments` | Führt nach jeder geplanten Sicherung den Anhang-Export aus. |
| `archive_path` | Wohin die `.eml`-Dateien geschrieben werden. Muss unter `/share`, `/media` oder `/backup` liegen. |
| `log_level` | `debug`, `info`, `warn` oder `error`. |

## Wo die Daten liegen

<img src="assets/storage.svg" alt="Die Konfiguration liegt in /data/config, das Archiv in /share/mail-archive; alles außerhalb der eingebundenen Ordner ist nach einem Update weg" width="100%">

| Pfad | Inhalt | Überlebt ein Update |
| --- | --- | --- |
| `/data/config` | verschlüsselte Konfiguration, Index-Datenbank | ja |
| `/share/mail-archive` | die gesicherten Mails | ja |

Beides gehört zu einem Home-Assistant-Backup — das Archiv also auch. Wenn die
Backups dadurch zu groß werden: `archive_path` auf eine Netzwerkfreigabe unter
`/media` legen und die dort ausschließen.

## In der Seitenleiste

<img src="assets/sidebar.svg" alt="Home Assistant mit Mail Archiver in der Seitenleiste, die Übersicht zeigt Nachrichtenzahl und Archivgröße" width="100%">

Ingress braucht keinen offenen Port: Home Assistant reicht die Oberfläche selbst
durch, und das Add-on antwortet ausschließlich diesem Proxy. Wer sie zusätzlich
aus einem anderen Browser oder mit der Desktop-App im Fernmodus erreichen will,
setzt `ui_password` und gibt im Reiter *Netzwerk* Port `8484` frei.

## Wie Updates ablaufen

Das Add-on ist ein Zeiger auf das Mail-Archiver-Image — ein Update ist also eine
Versionsnummer und sonst nichts. Ein Workflow hier schaut stündlich nach, ob die
Anwendung ein neueres Release hat, prüft, dass das passende Image auch
veröffentlicht ist, und trägt die Version ein. Home Assistant bietet das Update
danach wie gewohnt an.

Geholt wird, nicht geschickt: Ein Workflow-Token gilt nur für sein eigenes
Repository, ein Push aus dem Anwendungs-Repository bräuchte also einen
persönlichen Zugriffstoken — so braucht es gar kein Geheimnis. Wer eine Version
sofort haben will, startet unter *Actions* **Follow Mail Archiver** von Hand.

> GitHub schaltet geplante Workflows nach 60 Tagen ohne Commit im Repository ab.
> Wenn hier zwei Monate nichts passiert ist, einmal von Hand starten.

## Sensoren und Automatisierungen

Die Oberfläche ist das eine, Entitäten das andere. Zwei Wege, die sich nicht
ausschließen:

| | [Integration](https://github.com/sphings79/mail-archiver-home-assistant) | MQTT |
| --- | --- | --- |
| Installiert über | HACS | nichts, ist eingebaut |
| Offener Port nötig | ja, plus `ui_password` | nein |
| Broker nötig | nein | ja |
| Lovelace-Karte | dabei | nein |

MQTT wird im Add-on selbst eingerichtet, unter **Home Assistant**: Broker
eintragen, und Home Assistant legt per Discovery je Postfach ein Gerät an — mit
Nachrichten, Archivgröße, letzter Sicherung, laufender Sicherung und einem Knopf.

## Voraussetzungen

- Home Assistant OS oder Supervised — bei Container und Core gibt es keine
  Add-ons. Dort läuft das
  [Docker-Image](https://github.com/sphings79/mail-archiver/blob/main/README.de.md#docker)
  direkt.
- `aarch64` oder `amd64`. Eine 32-Bit-Fassung gibt es nicht.
- Platz für das Archiv: ungefähr so viel, wie das Postfach auf dem Server belegt.

## Fehlersuche

**Es startet nicht.** Das Protokoll sagt warum. Ohne Master-Passwort hört es
auf, weil es seine eigene Konfiguration nicht öffnen kann.

**„Only reachable through Home Assistant".** Genau so soll es sein: Das Add-on
weist alles ab, was nicht der Supervisor ist. Mit `ui_password` und
freigegebenem Port geht es auch von außen.

**Nach einem Update ist das Archiv weg.** `archive_path` zeigte in den Container
hinein. Ein Ordner unter `/share`, `/media` oder `/backup` gehört dorthin.

**Meine Backups sind riesig geworden.** Das Archiv liegt in `/share` und ist
damit enthalten. Auf eine Netzwerkfreigabe unter `/media` legen und dort
ausschließen.

## FAQ

### Löscht das Add-on etwas auf meinem Mailserver?

Nein. Ordner werden nur lesend geöffnet und Nachrichten mit `BODY.PEEK` geholt,
selbst das Gelesen-Kennzeichen bleibt, wie es war. Löschen ist gar nicht erst
eingebaut.

### Komme ich ohne Mail Archiver an die gesicherten Mails?

Ja. Jede Nachricht ist eine `.eml`-Datei, die Thunderbird, Apple Mail und
Outlook direkt öffnen. Der Ordnerbaum auf der Platte entspricht dem Postfach.

### Läuft das auf einem Raspberry Pi?

Ja, auf einer 64-Bit-Installation. Auf den Speicher achten: Eine SD-Karte ist
kein guter Platz für ein 20-GB-Archiv.

### Woher kommen Updates?

Das Add-on betreibt das veröffentlichte Mail-Archiver-Image. Eine neue Version
heißt: neues Release dort, Versionssprung hier — und der gewohnte
Update-Knopf im Add-on.

### Gibt es das auch für Home Assistant Container?

Add-ons gibt es nur bei Home Assistant OS und Supervised. Bei Container läuft
dasselbe Image mit `docker compose`; die Datei liegt im
[Hauptrepository](https://github.com/sphings79/mail-archiver/blob/main/README.de.md#docker).

## Credits

[Mail Archiver — The Mail Backup Solution](https://github.com/sphings79/mail-archiver)
von [sphings79](https://github.com/sphings79). Dieses Repository verpackt das
Image als Add-on; die Anwendung selbst liegt dort.

Ein ⭐ freut mich, und einen [Kaffee](https://buymeacoffee.com/sphings) gibt es
auch.

## Hinweis

Inoffiziell und aus der Community. Weder mit der Open Home Foundation noch mit
dem Home-Assistant-Projekt verbunden oder von ihnen unterstützt.

## Lizenz

AGPL-3.0-or-later, wie Mail Archiver selbst — siehe [LICENSE](LICENSE).

<sub>home assistant add-on · imap sicherung · e-mail archiv · mail backup home assistant ·
eml archiv · selbstgehostete mailsicherung · home assistant os add-on · ingress add-on</sub>
