# Leffasuositukset

Leffasuositukset on web-sovellus, jossa käyttäjät voivat jakaa elokuvavinkkejä ja arvioida muiden lisäämiä elokuvia.  
Sovellus on toteutettu Python-kielellä käyttäen Flask-kirjastoa, ja tiedot tallennetaan SQLite-tietokantaan.

## Sovelluksen toiminnot

- Käyttäjä voi luoda tunnuksen ja kirjautua sisään sovellukseen.
- Käyttäjä voi lisätä uusia elokuvia sovellukseen (nimi, genre, kuvaus, vuosi).
- Käyttäjä voi muokata ja poistaa itse lisäämiään elokuvia.
- Käyttäjä näkee sovellukseen lisätyt elokuvat sekä itse että muiden käyttäjien lisäämät.
- Käyttäjä voi hakea elokuvia hakusanalla (esimerkiksi elokuvan nimen tai genren perusteella).
- Käyttäjäsivulla näytetään tilastoja, kuten kuinka monta elokuvaa käyttäjä on lisännyt ja lista hänen lisäämistään elokuvista.
- Käyttäjä voi valita elokuvalle yhden tai useamman luokittelun (esim. toiminta, komedia, draama, kauhu).
- Käyttäjä voi lisätä arvosteluja (kommentin ja arvosanan) omiin ja muiden lisäämiin elokuviin.
- Elokuvasta näytetään kaikki siihen liittyvät arvostelut sekä keskimääräinen arvosana.

## Tietokohteet

- **Elokuva**  
  Pääasiallinen tietokohde, joka sisältää elokuvan perustiedot (nimi, genre, kuvaus, vuosi).
  
- **Arvostelu**  
  Toissijainen tietokohde, joka sisältää käyttäjän antaman kommentin ja arvosanan tietylle elokuvalle.

## Tekniset tiedot

- Sovellus on toteutettu Pythonilla käyttäen Flask-kirjastoa.
- Tietokantana toimii SQLite.
- Sovellus käyttää suoria SQL-komentoja tietokannan käsittelyyn.
- Käyttöliittymä koostuu HTML-sivuista ja itse toteutetusta CSS:stä.
- Sovelluksessa ei käytetä JavaScriptiä.
- Versionhallinta on toteutettu Gitillä, ja koodi on julkaistu GitHubissa.

## Käyttöohje (kehitysvaiheessa)

1. Kloonaa repositorio:  
   ```bash
   git clone https://github.com/<käyttäjänimesi>/leffasuositukset