# Accountview_Typer

AV_Typer is een python tool om makkelijk excel data over te typen naar Accountview

## Installation
Installatie is erg eenvoudig. Download AV_Typer.zip en pak het uit. Zoek vervolgens in de map AV_Typer.exe en voer dit bestand uit. Het programma zou dan moeten opstarten
## Usage

![images/img.png](images/img.png)
1. *Type selectie:* Elke sheet (dus activiteiten, weekend en borrel) heeft een aparte indeling in excel. Om deze reden moet je bij het openen aangeven om welk type sheet het gaat. Als je de verkeerde sheet aangeeft werkt de tool niet, dus check dit eerst voordat je een bug report indiend!
2. *Zoeken:* Door op deze knop te drukken kan je een bestand op je laptop zoeken
3. *Locatie:* Hier komt de locatie van het geselecteerde excel workbook te staan. Je kan hier ook een locatie in typen/plakken
4. *openen:* Zodra je een workbook hebt geselcteerd kan je hierop drukken om naar de typsheet te gaan.

![images/img_1.png](images/img_1.png)
1. *Terug:* gebruik dit om een andere workbook te selecteren
2. *sheet selectie:* Gebruik dit om de sheet die je wilt uittypen te selecteren
3. *Baten uitschrijven:* Druk op deze knop om de baten uit de sheet uit te schrijven. De tool begint niet direct met typen maar wacht tot je op ',' drukt. De tool mag niet geminimaliseerd zijn als je dit doet. Je kan het typen op elk moment stoppen door op 'left-control' te drukken.
4. *Lasten uitschrijven:* Druk op deze knop om de lasten uit te schrijven. Voor meer infor zie baten

## Sheet types
Er zijn 4 sheet types
1. Activiteiten voor activiteitensheets
2. borrel voor borrel sheets
3. weekend voor weekend sheets
4. simpel voor sheets volgens een vast formaat. de contributie sheet werkt hier bijvoorbeeld ook mee.

## Verschil V1 en V2
V2 bied support voor de nieuwe activiteiten sheet (die die begint op regel 4 ipv 1, net zoals de andere sheets), en heeft een fix voor bugs waar het grootboek als float werd gezien (aka een .0 achteraan werd gezet.). Verder worden bijdragen van BP bij activiteiten sheets nu wel toegvoegd. V2 is zo mogelijk nog slechter getest dan V1 dus laat vooral weten als er iets kapot is.

## memo aan mezelf
build-command is: `pyinstaller --add-data 'src/__conf__.ini;.' ./src/AV_Typer.py`

## License
[MIT](https://choosealicense.com/licenses/mit/)