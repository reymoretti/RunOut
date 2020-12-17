Composizione del progetto:

1 - Static folder
    
    qua ci sono le immagini di profilo e il file .css che è un file decorativo per la parte grafica (viene
    richiamato nei template che sono i file html)
 
 2 - Templates folder: ognuno dei template è richiamato nel file routes.py per creare la pagina. Ognuno di essi
                       estende il template layout che dovrebbe comprendere la parte superiore del sito e la
                       sidebar che si vedono sempre.
 
    2.1 about: non serve a nulla per ora. Viene richiamato dalla route '/about' per creare una pagina dove
               idealmente diciamo chi siamo
               
    2.2 account: pagina che mostra le info dell'utente
    
    2.3 article: semplice sintassi per gli articoli (Post), non ricordo se sta avendo un ruolo nel 
                 programma (mi sembra di no, ma è da controllare)
                 
    2.4 home: html per la home page
    
    2.5 layout: struttura fisica degli altri templates. Infatti è pieno di <div> <h1> <h2> <h3> che se
                opportunamente modificati/spostati possono cambiare la struttura del sito
    
    2.6 login: html per la sezione login
    
    2.7 program: non ricordo la sua funzione, non sembra importante ma è da controllare
    
    2.8 register: html per la sezione register

3 - Python files
    
    3.1 __init__ : serve solo per separare gli import e le configurazioni iniziali dal resto
    
    3.2 forms : contiene le forms per il Login, Registration e Update Account
    
    3.3 models : contiene le classi 
    
    3.4 routes : contiene le routes che creano le varie pagine nel sito
    
    3.5 run : serve solo per lanciare il sito
    
    
 in teoria c'è pure 'site.db' ma non so se lo crea automaticamente quando lanci oppure lo devo uploadare. è il database con le varie istanze.
    
