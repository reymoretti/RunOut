Composizione del progetto:

1 - Static folder
    
    qua ci sono le immagini di profilo e il file .css che è un file decorativo per la parte grafica (viene
    richiamato nei template che sono i file html)
 
 2 - Templates folder: ognuno dei template è richiamato nel file routes.py per creare la pagina. Ognuno di essi
                       estende il template layout che dovrebbe comprendere la parte superiore del sito e la
                       sidebar che si vedono sempre.

3 - Python files
    
    3.1 __init__ : serve solo per separare gli import e le configurazioni iniziali dal resto
    
    3.2 forms : contiene le forms per il Login, Registration e Update Account
    
    3.3 models : contiene le classi 
    
    3.4 routes : contiene le routes che creano le varie pagine nel sito
    
    3.5 run : serve solo per lanciare il sito
    
    
 in teoria c'è pure 'site.db' ma non so se te lo creerà automaticamente quando lanci oppure devi usare il mio. In ogni caso, è il database con le varie istanze.
    
