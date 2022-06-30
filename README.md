# Francesco Raso - Droni

Elaborato Programmazione di reti. Traccia 1

## Informazioni personali

Nome e cognome: Francesco Raso \
Mail: francesco.raso@studio.unibo.it \
Numero matricola : 0000988122

## Specifiche e descrizione progetto

Questo progetto ha l'obiettivo di creare una simulazione in Python in cui, mediante l'utilizzo dei socket, un Client commissiona a 3 droni delle consegne su richiesta, interfacciandosi con un Gateway che funge: 
- da router per smistare le richieste
- da monitor per visualizzare i messaggi di avvenuta consegna.

La connessione tra il Client ed il Gateway viene gestita mediante un socket TCP, mentre quella tra il Gateway e i 3 droni viene gestita mediante socket UDP.

## Librerie utilizzate

* sys - per terminare i processi.
* socket - per la creazione dei socket di comunicazione.
* tkinter - per la creazione dell'interfaccia utente.
* subprocess - viene sfruttata dal file `launcher.py` per lanciare i comandi `python *.py` tramite i pulsanti dell'interfaccia grafica.
* threading - per la creazione dei vari thread con cui gli enti in gioco si mettono in ascolto e gestiscono i messaggi scambiati.
* time - per misurare il tempo impiegato per trasmettere i pacchetti UDP e TCP.

## Utilizzo

L'intera simulazione sfrutta la libreria tkinter per la creazione dell'interfaccia grafica.

E' possibile utilizzare il file `launcher.py` per lanciare tramite l'interfaccia grafica tutti gli altri file con il comando: 

```bash
python launcher.py
```

Il resto della simulazione viene gestito dall'utente mediante l'utilizzo dell'interfaccia grafica fornita da ciascun processo.

## Dettagli implementativi

Tutti gli indirizzi IP (fittizi) e le porte dei vari soggetti coinvolti sono memorizzati all'interno di dizionari nel file `utils.py`.
Tale dizionario associa per ogni ID di ciascun drone una tupla che rappresenta la coppia IP-Porta.

Ciascuna finestra dell'interfaccia grafica contiene una sezione destinata alla visualizzazione dei messaggi che funge da console per ciascun processo e un tasto per chiudere i socket e liberare le porte utilizzate per future simulazioni.

L'interfaccia del Client contiene inoltre: 
- un form per l'inserimento dell'indirizzo di consegna 
- una ComboBox per selezionare l'ID del drone a cui inviare la richiesta di consegna del pacco.
- un tasto per ritentare la connessione al Gateway (ad esempio nel caso in cui il processo fosse stato lanciato prima di quest'ultimo).

## Dimensione buffers 

**buffer socket TCP**: per la natura stessa del protocollo e la sua affidabilita', possiamo mantenere un buffer relativamente piccolo.

**buffer socket UDP**: avendo predisposto un sistema di controllo di disponibilita' dei vari dispositivi direttamente sul Gateway (che aspetta finche' l'n-esimo drone non torna disponibile), possiamo garantire che i buffer dei droni vengano svuotati in tempo dal processore e quindi mantenere un buffer relativamente piccolo.

Disponendo di una macchina con un processore performante e tanta memoria, ho deciso quindi di settare la dimensione del buffer a **1024**.

## Tempo invio pacchetti

Per calcolare il tempo impiegato dai vari socket (TCP e UDP) ad inviare i pacchetti, viene utilizzata la libreria `time`. 

All'interno delle rispettive console, il Client e il Gateway possono visualizzare il tempo trascorso per inviare ciascun pacchetto. 
Essendo una simulazione che sfrutta l'interfaccia di loopback tale frazione ti tempo e' in entrambi i casi trascurabile (~0.0001 secondi).


## Gestione errori
Si assume che ogni consegna venga effettuata senza errori anche inserendo un indirizzo non valido.

