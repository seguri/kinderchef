# kinderchef

## Architecture

```mermaid
erDiagram
Child ||--o{ Attendance : "attends on"
Child ||--o{ ChildDietaryRestriction : "has"
DietaryRestriction ||--o{ ChildDietaryRestriction : "assigned to"
DietaryRestriction ||--o{ MealRestriction : "restricts"
Meal ||--o{ MealRestriction : "has"
WeeklySchedule ||--o{ WeeklyMeal : "contains"
Meal ||--o{ WeeklyMeal : "planned in"

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
    text description
    string severity
}

ChildDietaryRestriction {
    int id PK
    int child_id FK
    int restriction_id FK
    date start_date
    date end_date
    text notes
}

Meal {
    int id PK
    string name
    text description
    string category
    bool is_vegetarian
    bool is_vegan
    text ingredients
    text preparation_notes
}

MealRestriction {
    int id PK
    int meal_id FK
    int restriction_id FK
}

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
- Make sure you can compile psycopg2 by running `apt install build-essential python3-dev libpq-dev`
- Create a database with `just createdb`
- Configure the deployment remote with `just add-remote`
- Deploy with `just deploy`
- Create a django superuser with `just createsuperuser`

## TODO

- [ ] Migrate requirements.txt to pyproject.toml
