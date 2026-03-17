import os
import tempfile
from pathlib import Path

import pytest
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker

from backend.app import db
from backend.app.models import Base


def test_get_db_dependency():
    # Test that get_db() yields a valid session object
    gen = db.get_db()
    try:
        session = next(gen)
        assert session is not None
        assert session.is_active
    finally:
        try:
            next(gen)
        except StopIteration:
            pass


def test_get_db_exception_handling():
    # Test that get_db() handles exceptions properly
    from fastapi.testclient import TestClient
    from fastapi import FastAPI, Depends

    # Create a minimal FastAPI app to test the dependency injection
    app = FastAPI()

    @app.get("/test")
    def test_endpoint(session=Depends(db.get_db)):
        raise Exception("Test exception")

    client = TestClient(app)

    # Call the endpoint to trigger the exception handling in get_db()
    with client:
        try:
            response = client.get("/test")
            assert response.status_code == 500
        except Exception as e:
            assert "Test exception" in str(e)


def test_root_endpoint():
    # Test the root endpoint in main.py
    import os
    from pathlib import Path

    from fastapi.testclient import TestClient
    from backend.app.main import app

    # Create a dummy frontend directory to avoid error
    frontend_dir = Path(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend")))
    frontend_dir.mkdir(exist_ok=True)
    index_file = frontend_dir / "index.html"
    index_file.write_text("<html></html>")

    client = TestClient(app)

    try:
        response = client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
    finally:
        # Cleanup
        index_file.unlink()
        if not any(frontend_dir.iterdir()):
            frontend_dir.rmdir()


def test_get_session_exception_handling():
    # Test that get_session() handles exceptions properly
    try:
        with db.get_session() as session:
            raise Exception("Test exception")
    except Exception:
        pass


def test_get_session_context_manager():
    # Test that get_session() context manager works
    with db.get_session() as session:
        assert session is not None
        assert session.is_active


def test_apply_seed_if_needed_new_db():
    # Create a temporary directory for our test
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_dir = Path(tmpdir)
        data_dir = tmp_dir / "data"
        data_dir.mkdir()

        # Override DEFAULT_DB_PATH and create test engine
        original_db_path = db.DEFAULT_DB_PATH
        db.DEFAULT_DB_PATH = str(tmp_dir / "data" / "test_app.db")
        from sqlalchemy import create_engine
        test_engine = create_engine(f"sqlite:///{db.DEFAULT_DB_PATH}")

        # Override SessionLocal to use test engine
        original_session_local = db.SessionLocal
        db.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

        Base.metadata.create_all(bind=test_engine)

        try:
            # Call apply_seed_if_needed (will check if seed is needed)
            db.apply_seed_if_needed()

            # Check that database file was created
            assert Path(db.DEFAULT_DB_PATH).exists()

            # Verify no seed data was inserted (since we didn't create a seed file)
            with db.get_session() as session:
                notes_result = session.execute(text("SELECT * FROM notes")).fetchall()
                assert len(notes_result) == 0

                items_result = session.execute(text("SELECT * FROM action_items")).fetchall()
                assert len(items_result) == 0

        finally:
            # Restore original variables and clean up
            Base.metadata.drop_all(bind=test_engine)
            db.SessionLocal = original_session_local
            db.DEFAULT_DB_PATH = original_db_path


def test_apply_seed_if_needed_with_seed_file():
    # Create temporary seed.sql in ./data directory
    current_data_dir = Path("./data")
    current_data_dir.mkdir(exist_ok=True)
    temp_seed_file = current_data_dir / "seed.sql"
    temp_seed_file.write_text("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title VARCHAR(255) NOT NULL,
            content TEXT,
            created_at TIMESTAMP NOT NULL,
            updated_at TIMESTAMP NOT NULL
        );
        CREATE TABLE IF NOT EXISTS action_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description VARCHAR(255) NOT NULL,
            completed BOOLEAN NOT NULL,
            created_at TIMESTAMP NOT NULL,
            updated_at TIMESTAMP NOT NULL
        );
        INSERT INTO notes (title, content, created_at, updated_at) VALUES
        ('Test Note', 'Test Content', '2024-01-01 00:00:00', '2024-01-01 00:00:00');
        INSERT INTO action_items (description, completed, created_at, updated_at) VALUES
        ('Test Action Item', 0, '2024-01-01 00:00:00', '2024-01-01 00:00:00');
    """)

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_dir = Path(tmpdir)
        data_dir = tmp_dir / "data"
        data_dir.mkdir()

        # Override DEFAULT_DB_PATH and create test engine
        original_db_path = db.DEFAULT_DB_PATH
        db.DEFAULT_DB_PATH = str(tmp_dir / "data" / "test_app.db")
        from sqlalchemy import create_engine
        test_engine = create_engine(f"sqlite:///{db.DEFAULT_DB_PATH}")

        # Override both engine and SessionLocal in db.py
        original_engine = db.engine
        original_session_local = db.SessionLocal
        db.engine = test_engine
        db.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

        try:
            # Call apply_seed_if_needed BEFORE creating tables so it detects a new DB!
            db.apply_seed_if_needed()

            # Create tables after seed (so apply_seed_if_needed creates the DB file)
            Base.metadata.create_all(bind=test_engine)

            # Check that seed data was inserted
            with db.get_session() as session:
                notes_result = session.execute(text("SELECT * FROM notes")).fetchall()
                assert len(notes_result) == 1
                assert notes_result[0][1] == "Test Note"

                items_result = session.execute(text("SELECT * FROM action_items")).fetchall()
                assert len(items_result) == 1
                assert items_result[0][1] == "Test Action Item"
                assert items_result[0][2] == 0

        finally:
            # Restore original variables and clean up
            Base.metadata.drop_all(bind=test_engine)
            db.engine = original_engine
            db.SessionLocal = original_session_local
            db.DEFAULT_DB_PATH = original_db_path
            temp_seed_file.unlink()


def test_apply_seed_if_needed_existing_db():
    # Create a temporary directory for our test
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_dir = Path(tmpdir)
        data_dir = tmp_dir / "data"
        data_dir.mkdir()

        # Create initial database file
        db_path = tmp_dir / "data" / "test_app.db"
        db_path.touch()

        # Override DEFAULT_DB_PATH and create test engine
        original_db_path = db.DEFAULT_DB_PATH
        db.DEFAULT_DB_PATH = str(db_path)
        from sqlalchemy import create_engine
        test_engine = create_engine(f"sqlite:///{db.DEFAULT_DB_PATH}")

        # Override SessionLocal to use test engine
        original_session_local = db.SessionLocal
        db.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

        Base.metadata.create_all(bind=test_engine)

        try:
            # Call apply_seed_if_needed (should not apply seed to existing DB)
            db.apply_seed_if_needed()

            # Verify no seed data was inserted
            with db.get_session() as session:
                notes_result = session.execute(text("SELECT * FROM notes")).fetchall()
                assert len(notes_result) == 0

        finally:
            # Restore original variables and clean up
            Base.metadata.drop_all(bind=test_engine)
            db.SessionLocal = original_session_local
            db.DEFAULT_DB_PATH = original_db_path