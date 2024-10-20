# Suomi25

Suomi25 on keskustelusivusto, missä kuka tahansa voi keskustella mistä tahansa, kuten vaikka kissoista tai kukkasipuleista. Sivuston on tarkoitus olla parempi ja hienompi versio olemassa olevasta Suomi24-keskustelupalstasta. Tämän lisäksi Suomi25-siuvstolla on tiukka kiusaamiskielto.

Sivustolla tavalliset käyttäjät pystyvät luomaan uusia keskusteluja ja kommentoimaan muiden aloittamia keskusteluja. Tämän lisäksi tavalliset käyttäjät voivat seurata tykkäämiään keskuteluja, jolloin ne ilmestyvät käyttäjän etusivulle. 



## Sivuston toiminnallisuudet

* Tavallisten käyttäjien toiminnallisuudet
  - Käyttäjä pystyy luomaan itselleen käyttäjätilin
  - Käyttäjä pystyy kirjautumaan ulos ja sisään tililleen käyttäen käyttäjänimeä ja salasanaa
  - Käyttäjä pystyy luomaan uuden keskustelun
  - Käyttäjä pystyy kommentoida toisen tekemää keskusteluja
  - Käyttäjä pystyy seuraamaan tykkäämäänsä keskustelua, jolloin keskustelun pystyy näkemään suoraan etusivulta
  - Käyttäjä pystyy poistamaan luomiansa keskusteluja ja lähettämiään kommentteja

* Ylläpitäjän toiminnallisuudet
  - Tavallisen käyttäjän toiminnallisuuksien lisäksi ylläpitäjät voivat luomaan ja poistamaan keskustelualueita sekä poistamaan muiden käyttäjien aloittamia keskusteluita ja kommentteja

## Miten käyttää sivua

Voit joko käynnistää fly.ion kautta tai asentamalla repositorion:



# Asentamalla repositorio:

Kloonaa tämä repositorio tietokoneellesi ja siirry sen juurikansioon. 


# Aktivoi virtuaaliympäristö ja asenna sovelluksen riippuvuudet komennoilla:

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt

export DATABASE_URL='postgresql+psycopg2://'

export SECRET_KEY=90f13b356feac92e95c8e1789de91ed1
 
pip install psycopg2-binary


# Määritä tietokanta:

psql < schema.sql

# Käynnistä sovellus

flask run
