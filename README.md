# alpaca_game_ucll

## Eerste aanzet tot pseudo 3d

We zijn begonnen met het implementeren van raycasting en floorcasting om een pseudo 3d surface/map te renderen.
Allereerst is het belangrijk om pygame te gebruiken en te initialiseren. Dit gebeurd door de lijn code: 
```python 
pygame.init()
```
Binnen het framework pygame kunnen we ook vormen creëren en sprites inladen. In ons geval hebben we in de eerste versie enkel een statische alpaca gerendered. Later worden hier zeker nog animaties aan toegevoegd.

Een voorbeeld van het inladen van een statische sprite is: 
```python
pygame.image.load('sprites/stripes.png')
```
Zo hebben we een *player, surface en straat* ingeladen. Deze sprites werden opgeslaan in een variabele waarvan we de waarden zo manipuleren om een 3d effect te creëren. 

De game runned door een **while loop**. Deze while loop zal blijven runnen zolang zijn waarde True blijft. Als deze waarde op False gezet word dan zal het spel gesloten worden. Het doel van deze loop is om het verloop van het spel vast te leggen. Door deze loop te manipuleren kunnen we het spel stopzetten en een start menu tonen, een game over scherm tonen en verschillende andere features. 
