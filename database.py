from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base

# MySQL connection
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://sql12800299:3Evh96aIyT@sql12.freesqldatabase.com:3306/sql12800299"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# ✅ Test connection
def test_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("✅ Database connected:", result.scalar())
    except Exception as e:
        print("❌ Database connection failed:", str(e))


# Run test when file loads
test_connection()
