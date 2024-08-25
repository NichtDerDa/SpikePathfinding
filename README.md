# SpikePathfinding

Dieses Projekt enthält einen Python-Code für die Steuerung eines LEGO SPIKE Prime Roboters. Es handelt sich um eine angepasste Version, die auf dem ursprünglichen Code von GO Robot basiert.

# Funktionen

Der Code ermöglicht verschiedene Steuerungsfunktionen für den Roboter, einschließlich:
# Gyrorotation

    Dreht, bis eine bestimmte Farbe oder ein bestimmter Winkel erreicht ist.

# Gyrostraightdrive

    Fährt in einer geraden Linie, bis eine bestimmte Distanz oder Farbe erreicht ist.
    Parallele Codeausführung für das Drehen der Motoren während der Fahrt.

# Sonstiges

    Anzeigen auf der LED-Matrix: Zeigt eine Auswahl von Funktionen auf der LED-Matrix an.
    Funktionen-Auswahl: Ermöglicht die Auswahl und Navigation durch verschiedene Funktionen über die LED-Matrix.
    Batteriestatus lesen: Überprüft die Batteriespannung und gibt eine Warnung aus, wenn diese zu niedrig ist.
    Parallele Codeausführung: Ermöglicht das gleichzeitige Ausführen von Motorsteuerungen während anderer Aktionen.

# Verwendung

    Benötigte Erweiterungen/Programme für die Verwendung in VS Code:
        Visual Studio Code
        Python
        Lego Spike Prime/Mindstorms Robot Inventor Extension von Peter Staev

    Batteriespannung bei voller Ladung:
        Wenn der Akku vollständig geladen ist, beträgt die Spannung etwa 8300 mV. Dies kann je nach Abnutzung des Akkus variieren. Wir empfehlen, den Roboter aufzuladen, wenn die Batteriespannung unter 8000 mV fällt, da dies zu einem Drehmomentverlust führt.

    So verbindest du den Hub:
        Klicke auf die Schaltfläche „LEGO Hub: Disconnected“ auf der linken Seite der blauen unteren Leiste in VS Code. Ein Dropdown-Menü wird oben auf dem Bildschirm geöffnet. Probiere alle COM-Optionen aus, bis du verbunden bist. Hinweis: Du musst den Hub zuvor in der Spike- oder Mindstorms-Software verbunden haben.

    So lädst du ein Programm auf den Hub hoch:
        Drücke CTRL + SHIFT + P und wähle „LEGO Hub: upload program“ aus dem Dropdown-Menü. Wähle „Python: regular“. Wähle den Slot aus, in dem das Programm auf dem Hub gespeichert werden soll.

    So startest du ein Programm:
        Drücke CTRL + SHIFT + P und wähle „LEGO Hub: start program“ aus dem Dropdown-Menü. Wähle den Slot des Programms aus, das du auf dem Hub starten möchtest. Hinweis: Dieser Schritt kann übersprungen werden, wenn du die Autostart-Funktion aktiviert hast.

    So aktivierst du das Precompiling:
        Um das main.py-Programm auf dem PC/Laptop vorzukompilieren, gehe zur Erweiterungsseite in VS Code, wähle die Erweiterung aus, klicke auf das Einstellungssymbol und aktiviere „Lego Spike Prime Mindstorms: Compile Before Upload“. Dadurch wird das Programm schneller gestartet.

# Credits
Veränderter Code von blockplacer4, ursprünglicher Code von GO Robot, danke dafür ^^
