# Health-Insights-API 

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
