# kinderchef

## Architecture

```mermaid
erDiagram
Child ||--o{ Attendance : "attends on"
Child ||--o{ DietaryRestriction : "has"
DietaryRestriction ||--o{ Meal : "restricts"
DietaryRestriction ||--o{ DietaryRestriction : "contains"
Child {
    UUID id PK
    string first_name
    string last_name
}

Attendance {
    UUID id PK
    int child_id FK
    text rrule
}

DietaryRestriction {
    int id PK
    string name
    is_group bool
    included_restrictions DietaryRestriction[]
}

Meal {
    int id PK
    string name
    link URL
    text notes
    restrictions DietaryRestriction[]
}

WeeklySchedule ||--o{ WeeklyMeal : "contains"
Meal ||--o{ WeeklyMeal : "planned in"


WeeklySchedule {
    int id PK
    date week_start_date
    text notes
}

WeeklyMeal {
    int id PK
    int schedule_id FK
    int meal_id FK
    date serve_date
    string meal_time
}
```

## Piku

### First deployment

- Create Procfile
- Create ENV
- Update settings.py
- Open port 80 in the firewall to allow the Let's Encrypt challenge
- Make sure you can compile psycopg2 and translations by running `apt install build-essential python3-dev libpq-dev gettext`
- Create a database with `just createdb`
- Configure the deployment remote with `just add-remote`
- Deploy with `just deploy`
- Create a django superuser with `just createsuperuser`

## TODO

- [ ] Migrate requirements.txt to pyproject.toml
