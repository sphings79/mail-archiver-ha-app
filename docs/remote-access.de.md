# Das Add-on von außerhalb von Home Assistant erreichen

[English version](remote-access.md) · [Add-on-README](../README.de.md)

Ab Werk ist das Add-on über die Seitenleiste erreichbar und sonst nirgends. Das
ist Absicht — und zugleich der Grund, warum einiges nicht funktioniert, bevor du
das änderst: ein Archiv aus der Mail-Archiver-Desktop-App herüberzuschieben zum
Beispiel.

Diese Seite ist der ganze Vorgang: zwei Einstellungen, ein Neustart.

## Warum es zunächst zu ist

Ingress ist der Mechanismus, der die Oberfläche in die Seitenleiste bringt.
Home Assistant meldet den Benutzer zuerst an und reicht die Seite dann durch,
das Add-on selbst hat also keine eigene Anmeldung — es braucht keine, weil nur
der Supervisor es erreichen kann.

Das ist wörtlich gemeint. Das Add-on weist jede Anfrage ab, die nicht von der
Adresse des Supervisors kommt, und schreibt das bei jedem Start ins Protokoll:

```
Running as a Home Assistant add-on: reachable through the sidebar, and only from the supervisor
```

Wer nur den Port freigibt, ändert damit nichts: die Anfragen kommen an und
werden mit `403 Only reachable through Home Assistant` beantwortet. Erst das
Passwort hebt die Sperre auf, deshalb kommt es zuerst.

## Schritt 1 — Passwort der Oberfläche setzen

**Einstellungen → Add-ons → Mail Archiver → Konfiguration**, unter *Optionen*:

<img src="../assets/remote-options.svg" alt="Die Add-on-Konfiguration mit ausgefülltem Feld für das Passwort der Oberfläche und dem Speichern-Knopf darunter" width="100%">

Das ist das Passwort, nach dem die Oberfläche später fragt. Es ist nicht das
Master-Passwort: das Master-Passwort schließt innen die verschlüsselte
Konfiguration auf, dieses hier bewacht die Tür. Nimm ein anderes.

**Speichern** drücken.

## Schritt 2 — den Port freigeben

Derselbe Reiter, weiter unten, unter *Netzwerk*:

<img src="../assets/remote-network.svg" alt="Die Netzwerkeinstellungen des Add-ons mit Host-Port 8484 neben dem Container-Port 8484/tcp" width="100%">

Als Host-Port `8484` eintragen. Jeder freie Port geht — `8484` hält die Adresse
nur leichter merkbar.

**Speichern** drücken.

## Schritt 3 — Add-on neu starten

Die Optionen werden beim Start gelesen, das Add-on muss also einmal hoch und
runter. **Neu starten** im Reiter *Info* des Add-ons.

Im Protokoll steht jetzt:

```
Running as a Home Assistant add-on with an interface password of its own
```

Diese Zeile ist die Bestätigung. Steht dort weiterhin etwas vom Supervisor,
wurde das Passwort nicht gespeichert.

## Nachsehen, ob es klappt

Im Browser auf einem anderen Rechner `http://homeassistant.local:8484` öffnen.
Es sollte die Mail-Archiver-Oberfläche kommen und nach dem Passwort fragen.

Die Seitenleiste funktioniert unverändert weiter, ohne Passwort — an Ingress
ändert das alles nichts.

## Ein Archiv aus der Desktop-App umziehen

Dafür machen die meisten den Port auf. Ein Archiv, das auf dem Laptop
angefangen hat, wandert so ins Add-on:

1. Im Add-on das Konto mit derselben Mailadresse anlegen
2. In der Desktop-App das Konto öffnen und **Umziehen** wählen
3. Adresse `http://homeassistant.local:8484`, Passwort: das der Oberfläche aus
   Schritt 1
4. Das Konto auf der Gegenseite auswählen und starten

Es wandern die Dateien, nicht der Index. Jeder Ordner trägt ein Journal, und
das Add-on baut seinen Index daraus auf — deshalb ist ein abgebrochener Umzug
harmlos. Noch einmal starten, und es geht nur hinüber, was fehlt, verglichen
nach Name und Größe.

Auf dem Laptop wird nichts gelöscht. Erst das Archiv im Add-on ansehen, dort
eine Sicherung laufen lassen, und dann die alte Kopie von Hand entfernen.

## Wenn es nicht geht

**Der Browser findet `homeassistant.local` nicht.** Der Name kommt über mDNS,
und manche Netze und manche VPNs lassen das nicht durch. Dann die IP-Adresse
deiner Home-Assistant-Maschine nehmen — `http://192.168.1.x:8484`.

**`403 Only reachable through Home Assistant`.** Das Passwort ist leer. Eine
Option, die ausgefüllt aussieht, aber nie gespeichert wurde, zählt als leer;
den Reiter *Konfiguration* noch einmal öffnen und nachsehen.

**Das Add-on startet nach dem Freigeben nicht mehr.** Auf der
Home-Assistant-Maschine hört schon etwas anderes auf `8484`. Einen anderen
Host-Port nehmen; der Container-Port bleibt `8484`.

**Die Desktop-App sagt, die Anmeldung sei fehlgeschlagen.** Sie will das
Passwort *der Oberfläche*, nicht das Master-Passwort.

## Ein Wort zur Sicherheit

Das ist ein einfacher HTTP-Port im lokalen Netz, geschützt durch ein Passwort.
Für ein Heimnetz ist das angemessen, für mehr nicht.

Gib ihn nicht im Router frei und stell ihn nicht ins Internet. Wer von unterwegs
an das Archiv will, erreicht Home Assistant so, wie er es ohnehin tut — über die
App, Nabu Casa oder das VPN — und nimmt die Seitenleiste. Ingress liegt hinter
der Anmeldung von Home Assistant, und die ist erheblich besser als ein Passwort
an einem offenen Port.

---

Wenn dir das eine Stunde gespart hat: ein ⭐ auf
[dem Add-on](https://github.com/sphings79/mail-archiver-ha-app) oder auf
[Mail Archiver](https://github.com/sphings79/mail-archiver) freut mich, und
einen [Kaffee](https://buymeacoffee.com/sphings) gibt es auch.
