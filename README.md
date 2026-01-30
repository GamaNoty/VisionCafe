# Objednávkový systém (Django & Docker)

Tento projekt je komplexní webová aplikace pro správu objednávek v kavárně. Zákazníci si mohou objednat přímo u stolu pomocí QR kódu, zatímco personál spravuje objednávky v dashboardu.

---

## Hlavní Funkce

* **Zabezpečené URL stolů:** Každý stůl má unikátní URL s SHA-256 hashem (tokenem). To zabraňuje útokům typu IDOR.
* **Stavy objednávek:** Systém automaticky vypočítává stav podle času a logiky:
    * **Nová:** Objednávka čeká na přijetí (do 10 minut).
    * **Propáslá:** Číšník si objednávky nevšiml a vypršel časový limit 10 minut.
    * **Přijatá:** Objednávka se připravuje.
    * **Nestihnutá:** Objednávka nebyla dokončena do 15 minut od jejího přijetí.
    * **Odmítnutá:** Objednávka byla zamítnuta.
* **Staff Dashboard:** Soukromá zóna pro personál vyžadující přihlášení (`is_staff`). Obsahuje přehlednou tabulku s rozlišenými stavy a možností archivace starých objednávek.
* **Docker:** Aplikace je plně kontejnerizovaná pro snadné a konzistentní nasazení v jakémkoliv prostředí.

---

## Instalace a spuštění

K instalaci je vyžadován **Docker** a **Docker Compose**.

1.  **Sestavení a spuštění kontejnerů:**
    ```bash
    docker-compose up --build
    ```

2.  **Provedení migrací databáze (v novém terminálu):**
    ```bash
    docker-compose exec web python manage.py migrate
    ```

3.  **Vytvoření administrátorského účtu pro personál:**
    ```bash
    docker-compose exec web python manage.py createsuperuser
    ```

4.  **Přístup k aplikaci:**
    * **Zákaznická zóna:** `http://localhost:8000/stul/#/hash/` Číslo stolu a jeho hash.
    * **Staff Dashboard:** `http://localhost:8000/zamestnanec/`
    * **Admin rozhraní:** `http://localhost:8000/admin/`