# Moses - PBSMT
Moses phrase-based statistical machine translation (Moses PBSMT) er kerfi til þess að þróa og keyra tölfræðilega vélþýðingar.
Í þessu skjali er lýst hvernig hægt er að nota (forþjálfað) Moses þýðingarkerfi og leiðbeiningar fyrir frekari þróun.

Kerfið er gefið út sem nokkrar `Docker` myndir sem hægt er að keyra með `docker` eða `singularity`. Inn í þessum myndum er Moses kerfið uppsett og python forrit til þess að forvinna texta. Gögn fyrir þjálfun er ekki deilt með myndunum (sökum stærðar) en hægt er að nálgast samhliða málheild og einhliðamálheild fyrir íslensku á malfong.is. Fyrir ensku notuðum við USENET einhliða málheildina sem er opin öllum.

Hægt er að keyra forþjálfað kerfi á einstökum setningum í gegnum HTTP (þýðingarþjónn) eða beint.

## Keyrsla
Til þess að keyra kerfið þá þarf `docker` eða `singularity` að vera uppsett.

Keyrsla (þýðing en-is) beint á einni setningu:
```
docker run -ti haukurp/moses-lvl:1.0.1-en-is /bin/bash -c "corpus sent-process-v1 'This is an English sentence.' 'en' | /opt/moses/bin/moses -f /work/moses.ini" 
```
Fyrir is-en:
```
docker run -ti haukurp/moses-lvl:1.0.1-is-en /bin/bash -c "corpus sent-process-v1 'Þetta er íslensk setning.' 'is' | /opt/moses/bin/moses -f /work/moses.ini"
```
Keyra Moses þýðingarþjón.
    # TODO

Keyrsla sem singularity geymir (dæmi):
```
singularity run docker://haukurp/moses-lvl:0.1
```
Keyrsla á Jupyter notebooks í gegnum docker geymi:
```
docker run -ti -p 8888:8888 -v $PWD:/opt/work haukurp/moses-lvl:0.3 /bin/bash -c "/opt/conda/envs/jupyter/bin/jupyter notebook --notebook-dir=/opt/work --ip='*' --port=8888 --no-browser --allow-root"
```
Keyrsla á Jupyter notebooks í gegnum singularity geymi:
```
singularity exec -B $PWD:/opt/work docker://haukurp/moses-lvl:0.4 /bin/bash -c "/opt/conda/envs/jupyter/bin/jupyter notebook --notebook-dir=/opt/work --ip='*' --port=8888 --no-browser --allow-root"
```
Keyrsla á Jupyter notebooks í gegnum slurm:
```
sbatch run-jupyter-sbatch
```
## Þróun
Það eru skilgreindar nokkrar Docker myndir í þessu verkefni.

1. [`moses-Dockerfile`](https://hub.docker.com/r/haukurp/moses-smt). Þetta er grunn myndin sem hefur uppsett Moses þýðingarkerfið og önnur tól nauðsynleg til þess að þjálfa og keyra þýðingarkerfið. Þessi mynd er ekki til beinnar notkunar.
1. [`corpus-Dockerfile`](https://hub.docker.com/r/haukurp/moses-lvl). Þessi mynd byggir á `moses-Dockerfile` og bætir við Python 3.7 og öðrum python pökkum til þess að forvinna gögn.
1. `model-Dockerfile`. Þessi mynd byggir á `corpus-Dockerfile` sem og forþjálfuðu Moses þýðingarkerfi. 

Einnig fylgir með Python forrit fyrir forvinnslu í skránni `corpus`. Fyrir það verkefni sjá `corpus/README.md`.

Einnig fylgja með nokkur Jupyter vélrit (e. notebook) sem notuð voru við þróun á kerfinu. Til þess að keyra vélritin þá þarf Moses kerfið að vera aðgengilegt. Auðveldast er því að keyra vélritin í gegnum `docker` eða `singularity`, annars þarf að setja kerfisbreyturnar (environment variables) `THREADS`, `MOSESDECODER` og `MOSESDECODER_TOOLS` og láta þær vísa á skrár sem innihalda nauðsynleg forrit.

Þegar búið er að þjálfa nýtt líkan þá er hægt að pakka því í nýjan docker geymi. Fyrst þarf að sækja þjálfaða líkanið á vélina. Svo þarf að setja líkanið í geyminn. Sjá "Byggja myndir" fyrir skipanir. 
### Útgáfa
Leiðbeiningar fyrir útgáfu á Docker myndum. Til þess að geta klárað útgáfuna þarf að hafa aðgang að tilheyrandi DockerHub repo og gera `docker login`.

#### Moses Docker
1. Uppfæra útgáfunúmer að neðan og keyra.
```
TAG=1.0.0; docker build -f moses-Dockerfile -t haukurp/moses-smt:$TAG . && docker push haukurp/moses-smt:$TAG
```
#### Corpus Docker
Útgáfunúmerið á `moses-lvl` er látið hanga saman við `corpus` (Python kóða).

1. Gefa út `corpus`, sjá `corpus/README.md`.
1. Uppfæra útgáfunúmer í `corpus-Docerfile` til að vísa í nýja útgáfu af `corpus`. Ef `moses-smt` var líka gefið út, þá þarf hugsanlega líka að uppfæra þá vísun.
1. Uppfæra útgáfunúmer að neðan og keyra.
```
TAG=1.0.2; docker build -f corpus-Dockerfile -t haukurp/moses-lvl:$TAG . && docker push haukurp/moses-lvl:$TAG
```
#### Model Docker
Við ýtum `model-Dockerfile` á sama DockerHub repo `corpus-Dockerfile` þ.e. `moses-lvl`.
Við látum útgáfunúmerið vera það sama og á `moses-lvl` en bætum við flöggum. Ef `moses-lvl` var líka gefið út, þá þarf hugsanlega líka að uppfæra þá vísun.
Gert er ráð fyrir að til sé þjálfað módel á `Terra`.
```
MODEL_NAME=en-is
CORPUS_VERSION=1.0.2
TAG=$CORPUS_VERSION-$MODEL_NAME
# Afrita líkanið yfir á núverandi vél í skrána sem inniheldur `model-Dockerfile`.
scp -r haukurpj@terra.hir.is:/scratch/smt/$MODEL_NAME/binarised trained_model
# Laga skráarendingar.
sed -i 's/work\/.*\/binarised/work/g' trained_model/moses.ini
docker build -f model-Dockerfile -t haukurp/moses-lvl:$TAG .
rm -rf trained_model
docker push haukurp/moses-lvl:$TAG
```
Það er gott að taka það fram að staðsetningin á líkaninu í geyminum er mikilvæg, því `moses.ini` skráin inniheldur vísanir í nauðsynlegar skrár í kerfinu. Ef staðsetningunni er breytt, þá þarf líka að breyta vísuninum í `moses.ini`. Þetta er ástæðan fyrir `sed` skipuninni.
### Keyrsla á Terra cluster (Slurm)
Fyrst þarf að fá aðgang á cluster. Hafðu samband við cluster admin.

Best er að sækja git repo á vélina þar sem allar keyrslu skipanir eru skilgreindar þar.

Panta tíma á cluster fyrir jupyter-notebook (í gegnum singularity) með 'sbatch' sem er skilgreint í SMT repo.
    
    cd SMT
    sbatch run-jupyter.sbatch

Þetta á að byrja keyrsluna á Juypter notebook. Athugaðu hvort hún keyrir.

    squeue

Þegar hún keyrir, sæktu token-ið til þess að logga inn á notebook.

    grep 'token' -m 1 server.out | awk -F '=' '{print $2}' 

Setja upp SSH tunnel (svo hægt sé að opna þetta á þinni vél). Settu inn notendanafnið þitt á Terra í stað <username>.

    ssh -N -L 127.0.0.1:8888:127.0.0.1:8888 haukurpj@10.6.11.156    

    
