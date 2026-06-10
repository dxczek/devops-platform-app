# Task Management API

Aplikacja webowa, którą napisałem na potrzeby pracy inżynierskiej jako element platformy GitOps. To proste API do zarządzania zadaniami (typu CRUD), które służy jako aplikacja demonstracyjna do pokazania pełnego procesu wdrażania: od kodu, przez pipeline CI/CD, aż po automatyczne wdrożenie w klastrze Kubernetes przez ArgoCD.

Manifesty Kubernetes i konfiguracja wdrożenia są w osobnym repozytorium: [devops-platform-gitOps](https://github.com/dxczek/devops-platform-gitOps).  

 

API jest napisane w Pythonie z użyciem frameworka FastAPI. Wystawia kilka endpointów:

- `GET /` zwraca podstawowe informacje o aplikacji i numer wersji, przydatne do sprawdzania czy wdrożyła się nowa wersja
- `GET /health` liveness probe dla Kubernetes, mówi czy aplikacja żyje
- `GET /ready` readiness probe, sprawdza dodatkowo połączenie z bazą danych
- `GET /metrics` metryki w formacie Prometheus
- `GET /tasks` lista wszystkich zadań
- `POST /tasks` utworzenie nowego zadania
- `GET /tasks/{id}` pobranie konkretnego zadania
- `PUT /tasks/{id}` aktualizacja zadania
- `DELETE /tasks/{id}` usunięcie zadania

FastAPI sam generuje interaktywną dokumentację Swagger, dostępną pod `/docs` po uruchomieniu aplikacji.

## Technologie

- Python 3.12 i FastAPI
- PostgreSQL 16 jako baza danych
- SQLAlchemy do obsługi bazy
- Docker do konteneryzacji (multi-stage build)
- pytest do testów

## Jak uruchomić lokalnie

Najprościej przez Docker Compose, bo od razu stawia aplikację razem z bazą:

```bash
docker-compose up --build
```

Aplikacja będzie dostępna pod `http://localhost:8000`, a dokumentacja Swagger pod `http://localhost:8000/docs`.

Jeśli wolisz odpalić bez Dockera, potrzebujesz uruchomionego PostgreSQL i wtedy:

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Adres bazy aplikacja bierze ze zmiennej środowiskowej `DATABASE_URL`. Dzięki temu ta sama aplikacja działa lokalnie i w klastrze, zmienia się tylko wartość tej zmiennej.

## Testy

Testy uruchamia się przez pytest:

```bash
pytest tests/ -v
```

Do testów podpina się tymczasowa baza PostgreSQL, więc sprawdzają one nie tylko logikę, ale i operacje na bazie.

## CI/CD

W katalogu `.github/workflows` jest pipeline GitHub Actions, który po każdym pushu na gałąź `main` wykonuje po kolei:

1. uruchamia testy z tymczasową bazą PostgreSQL
2. buduje obraz Docker i wysyła go do Docker Hub z unikalnym tagiem
3. skanuje obraz pod kątem podatności narzędziem Trivy
4. aktualizuje tag obrazu w repozytorium GitOps, co uruchamia automatyczne wdrożenie przez ArgoCD

Od tego momentu sterowanie przejmuje ArgoCD, które synchronizuje klaster ze stanem opisanym w repozytorium GitOps.

## Struktura projektu

```
app/                kod aplikacji (FastAPI)
tests/              testy jednostkowe
.github/workflows/  pipeline CI/CD
Dockerfile          definicja obrazu (multi-stage build)
docker-compose.yml  lokalne uruchomienie z bazą
requirements.txt    zależności Pythona
```

## Autor

Jan Duczek
nr albumu 44682,
projekt do pracy inżynierskiej.
