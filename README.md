# Task Manager App

A Flask application for managing tasks, featuring:
- User Authentication (Register/Login)
- Task CRUD operations
- PostgreSQL database integration
- Docker support
- CI/CD pipeline with GitHub Actions

## Local Development

1. Create environment:
```bash
conda create -n ml_in_prod_lab4 python=3.10
conda activate ml_in_prod_lab4
pip install -r requirements.txt
```

2. Run Database Migrations:
```bash
python migrate.py
```

3. Run App:
```bash
python app.py
```

## Testing

Run unit and integration tests:
```bash
pytest tests/test_unit.py tests/test_integration.py
```
