from app import app, db

print('Flask app imported successfully')

with app.app_context():
    db.create_all()
    print('Database created successfully')

print('Flask app test completed successfully')
