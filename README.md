# Universalis : Génération d'un rapport Counter DB1 à partir des données piwik

Ce script utilise l'api PIWIK d'Universalis pour construire un rapport counter DB1 R4. Il s'appuie sur le rapport  **getPageUrls** qui compte le nombre de pages vue en fonction de l'URL pour produire les indicateurs  **Regular Searches** et **record Views**
## Record views
### Indicateur pris en compte 
Nombre de vue uniques (nb_visits) = Nombre de visites qui ont inclus cette page. Si une page a été vue plusieurs fois durant la visite elle ne sera comptabilisée qu'une seule fois.
### Pages prises en compte
  - encyclopedie
  - media
  - dictionnaire
  - evenement
  - datapay
## Regular Searches
### Indicateur pris en compte 
Vues (nb_hits) = Le nombre de fois que cette page a été visitée.
### Pages prises en compte
  - recherche
  - carte-mentale
  - classification
  - atlas
  - auteurs
  - chronologie