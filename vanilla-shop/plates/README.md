# Vanilla plate

`de-alwis-vanilla.jpg` is a cleaned copy of *Vanilla planifolia*, a watercolour credited to
George De Alwis (Ceylon), public domain via Wikimedia Commons:
https://commons.wikimedia.org/wiki/File:Vanilla_planifolia_Andrews_-_Mon_Jardin_a_Ceylan._1._(1896).jpg

The committed file comes from the 960 px preview and is fine for screens only.
For print, download the original (5595 x 7805 px) from the link above and run:

    python3 tools/prepare_plate.py ~/Downloads/Vanilla_planifolia_Andrews_-_Mon_Jardin_a_Ceylan._1._\(1896\).jpg plates/de-alwis-vanilla.jpg 4000
    npm install && npm run export

The front panel shows the plate about 61 mm wide, so 4000 px gives well over 300 dpi.
Confirm the credit wording before print.
