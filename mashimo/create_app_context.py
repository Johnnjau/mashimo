from app import create_app, db

app = create_app()

# Set up application context
app.app_context().push()

# Now you can use `app` and `db` in this context
print(app)
print(db)
