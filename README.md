# Moses - PBSMT
Moses phrase-based statistical machine translation (Moses PBSMT) er 
kerfi til þess að þróa og keyra tölfræðilega vélþýðingar.
Í þessu skjali er lýst hvernig hægt er að nota (forþjálfað) Moses þýðingarkerfi 
og leiðbeiningar fyrir frekari þróun.

Verkefninu er skipt í nokkra hluta:
1. Moses kerfið uppsett. Dreift með Docker. 
1. Föll til þess að þjálfa og dreifa Moses kerfi.
Forþjálfuðum kerfum er dreift með með Docker. 
1. Framendi fyrir þýðingarvél og forvinnslu föll í.
Dreift sem Python pakka og Docker.
1. Aukalega fylgja vélrit sem eru notuð til þess að forvinna og samhæfa gögn.

Skjölun hvers hluta:
- [moses/README.md](moses/README.md) fyrir lýsingu á hvernig hægt er að nota `moses`.
Hluti af skjöluninni er á ensku þar sem henni er dreift annars staðar.
- [moses_model/README.md](moses_model/README.md) fyrir lýsingu hvernig hægt er að þjálfa Moses kerfi og dreifa því.
- [frontend/README.md](frontend/README.md) fyrir lýsingu á þýðingarþjóni og forvinnslu föllum.

Gögn fyrir þjálfun er ekki deilt með myndunum (sökum stærðar) en 
hægt er að nálgast samhliða málheild og einhliðamálheild fyrir íslensku 
á malfong.is.

Einnig er hægt að nota `singularity` til þess að keyra `docker`.
Það er ekki sérstaklega útskýrt hér hvernig hægt er að nota `singularity` í stað `docker`.

## Keyrsla
Til þess að keyra kerfið í heild þá þarf `docker` og `docker-compose` að vera uppsett.

```shell script
docker-compose up -d
# Þýða is-en
curl -d '{"contents":["Virkilega löng setning sem ætti að koma út fyrr.", "Setning"],"sourceLanguageCode":"is","targetLanguageCode":"en","model":"is-en"}' -H "Content-Type: application/json" http://localhost:5000/translateText -v
# Þýða en-is
curl -d '{"contents":["A really long sentence which should be in the first output.", "A sentence"],"sourceLanguageCode":"en","targetLanguageCode":"is","model":"en-is"}' -H "Content-Type: application/json" http://localhost:5000/translateText -v
# stöðva
docker-compose stop
```
Kerfið sem er ræst hér er í þremur hlutum.
1. Forþjálfað Moses kerfi fyrir `en-is`
1. Forþjálfað Moses kerfi fyrir `is-en`
1. Framendi sem forvinnur setningar sem koma inn.

Fyrir lýsingu á API, sjá [frontend/README.md](frontend/README.md).
