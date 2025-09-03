from app import app, db

def init_database():
    """Initialize the database with all tables."""
    with app.app_context():
        try:
            # Create all database tables
            db.create_all()
            print("✅ Database initialized successfully!")
            print(f"📁 Database file: sanskrit_passwords.db")
            
            # Check if tables were created
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"📋 Created tables: {', '.join(tables)}")
            
            return True
        except Exception as e:
            print(f"❌ Error initializing database: {e}")
            return False

if __name__ == '__main__':
    init_database()
