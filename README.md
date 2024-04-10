Nume: Alexandru-Nicolae VLĂDUȚ
Grupă: 332CA

# Tema 1 - Le Stats Sportif 

## Organizare

### Abordarea generală

Toate rutele sunt definite in fișierul 'routes.py'.

În momentul în care se face un POST request către una dintre rute, sunt executați următorii pași:
- Sunt extrase datele din request (întrebarea și/sau statul).
- Este înregistrat job-ul folosind metoda register_job() a clasei JobHandler().
    - Se asignează un nou job_id.
    - Se definește closure-ul care urmează să fie adăugat în coada de job-uri cu scopul
    unei executări ulterioare.
        - Se realizează execuția propriu-zisă a request-ului folosind parametrul execute_job().
        Acesta reprezintă funcția din fișierul 'request_methods.py' aferentă request-ului. În
        acest fișier este definită logica de execuție pentru rezolvarea fiecărui request, aceasta
        fiind implementată în mare parte folosind biblioteca 'pandas' (datele din CSV fiind
        stocate în DataIngestor sub forma unui DataFrame).
        - Se salvează rezultatul în folderul 'results/'.
    - Se adaugă job-ul în coadă utilizând metoda add_job() din clasa ThreadPool(). Job-ul este
    adăugat sub forma unui tuplu format din closure-ul și job_id-ul definite anterior. În cazul în
    care un request graceful_shutdown a fost deja inițiat, adăugarea în coadă nu se realizează.
- Se întoarce job_id-ul/eroare de 'Shutdown procedure has started', după caz.

Pentru GET request-urile de tipul get_response, job_request și num_jobs_request, logica de
implementare e destul de straight-forward, elementul principal care facilitează rezolvarea fiind
un dicționar care reține job-urile înregistrate până acum și statusul lor.

Pentru GET request-ul de tip graceful_shutdown, rezolvarea constă în apelarea metodei shutdown()
din clasa ThreadPool(). Aceasta face următorii pași:
- Se setează pe true variabila 'shutdown_flag' pentru a bloca adăugarea de noi job-uri în coadă.
- Adaugăm un obiect de tip 'None' în coadă pentru fiecare worker thread existent. În momentul în
care un thread scoate din coadă acest element 'None' cu scopul de a-l rezolva, bucla sa infinită
se va rupe. Așa mă asigur că thread-urile vor finaliza job-urile rămase în coadă după semnalul de
shutdown, știind când să se oprească.
- Având în vedere flow-ul de la linia anterioară, pot da join() thread-urilor fară să am probleme.

### Consideri că tema este utilă?

Consider că este o temă mult mai utilă decât multe altele pe care le-am avut până acum :>

Spun asta din următoarele puncte de vedere:
- Ne învață să interacționam, macar la nivel de bază, cu un server web (pentru cei care nu și-au
dat silința la PCom, cel puțin).
- Pentru prima dată în facultatea asta învățam un framework (Flask), nu doar un limbaj de
programare. Până acum s-a învățat backend folosind diverse limbaje, însă niciodată nu ni s-a
arătat cum se integrează acest backend într-o aplicație propriu-zisă și folosirea framework-urilor
în acest sens.

### Consideri implementarea naivă, eficientă, se putea mai bine?

Întotdeauna se poate mai bine, chiar daca știi sau nu cum să faci asta. Cu toate acestea o consider
o implementare eficientă și ordonată.

Spun eficientă pentru că am lucrat în mare parte cu metodele din librăria 'pandas' care mi-au permis
să rezolv request-urile destul de straight-forward, inteligibil și cu puține linii de cod.

De asemenea, m-am asigurat să am o implementare ordonată prin modularizarea constantă a codului
scris. Am scris, unde mi s-a părut cel mai intuitiv, să scriu cod orientat pe obiect (implementarea
JobHandler-ului și a Logger-ului), dar și să separ logica de execuție a request-urilor (în
'request_methods.py') pentru a evidenția doar flow-ul general în fișierul 'routes.py'.


## Implementare

* Am implementat toate endpoint-urile din enunț: nu am nici funcționalități lipsă, nici în plus.
* Am implementat partea de Logging.
* Nu am implementat partea de UnitTesting.
* Dificultăți întâmpinate:
    - Având în vedere că am încercat o modularizare constantă pe parcursul dezvoltării, m-am lovit
    frecvent de erori de cirular imports. Le-am rezolvat fie realizând import-urile la nivel de
    clase/metode (în loc de modul), fie dând ca parametru webserver-ul claselor respective pentru a
    evita linia 'from app import webserver'.
    - De asemenea, la începutul dezvoltării era un challenge testarea doar anumitor funcționalități,
    însă am rezolvat acest aspect folosind Postman.
* Lucruri interesante descoperite pe parcurs:
    - Cu siguranță toate clasele/metodele puse la dispoziție de librăria 'pandas'. Nu știam că pot fi
    handled atât de ușor datele dintr-un CSV, cu atât mai mult în volum mare (din câte am văzut este
    mult mai eficient în a realiza operații pe date din tabele de dimensiuni mari în comparație cu
    metode clasice, precum folosirea și manipularea de dicționare).


## Resurse utilizate

* https://ocw.cs.pub.ro/courses/asc/laboratoare/02
* https://ocw.cs.pub.ro/courses/asc/laboratoare/03
* https://www.geeksforgeeks.org/python-pandas-dataframe/
* https://pandas.pydata.org/docs/reference/general_functions.html
* https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html
* https://docs.python.org/3/library/logging.html

## Git

* https://github.com/alexandru-vladut/1-le-stats-sportif (nu știu cât ajută fiind privat, însă l-am
pus pentru că era în template-ul de README)
