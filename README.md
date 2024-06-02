# Comparazione performance ULAB e Numpy

distribuzione consigliata: debian 12 (Bookworm)
versione Python consigliata: 3.11

## Esecuzione dei test

### Installazione dipendenze

Assicurarsi di utilizzare python 3.11.2

```bash
python3 -m venv .venv # creazione del virtual environemnt (venv)
source .venv/bin/activate # attivazione del venv
pip3 install -r requirements.txt # installazione dipendenze
ln -s $(which python3) "builds/python3.11.2"
```

### Avvio test

il seguente comando eseguirà tutti i test presenti in `performance.py` con tutti 
i firmware presenti in build

```bash
./test_with_all.sh
```

## Analisi test

per l'analisi dei test è presente il notebook `analysis.ipynb` che permette di 
analizzare i risultati

### Installazione dipendenze notebook

```bash
pip install matplotlib seaborn pandas
```