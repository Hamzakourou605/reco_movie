import pandas as pd
from database import SessionLocal, init_db, engine
from database import Movie, Rating, Tag
import sys

def seed_data():
    print("Initializing Database tables...")
    init_db()
    
    session = SessionLocal()
    
    # Check if data already exists
    if session.query(Movie).first() is not None:
        print("Database already contains data. Exiting seeding process.")
        session.close()
        return

    print("Loading movies.csv...")
    try:
        movies_df = pd.read_csv("movies.csv")
        # Optimization for bulk insert
        movies_df.to_sql('movies', engine, if_exists='append', index=False)
        print(f"Inserted {len(movies_df)} movies.")
    except Exception as e:
        print(f"Error loading movies: {e}")

    print("Loading ratings.csv... (This might take a while)")
    try:
        # Load in chunks to avoid memory errors if ratings is huge
        chunksize = 100000
        total_ratings = 0
        for chunk in pd.read_csv("ratings.csv", chunksize=chunksize):
            chunk.to_sql('ratings', engine, if_exists='append', index=False)
            total_ratings += len(chunk)
            print(f"Inserted {total_ratings} ratings...", end='\r')
        print(f"\nCompleted inserting {total_ratings} ratings.")
    except Exception as e:
        print(f"\nError loading ratings: {e}")

    """
    print("Loading tags.csv...")
    try:
        tags_df = pd.read_csv("tags.csv")
        tags_df.to_sql('tags', engine, if_exists='append', index=False)
        print(f"Inserted {len(tags_df)} tags.")
    except Exception as e:
        print(f"Error loading tags: {e}")
    """
    
    print("Seeding finished.")
    session.close()

if __name__ == "__main__":
    seed_data()
