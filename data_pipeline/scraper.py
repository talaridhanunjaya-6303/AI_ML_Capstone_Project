import requests
import pandas as pd
import sqlite3
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# -----------------------------
# Base URL
# -----------------------------
BASE_URL = "https://books.toscrape.com/"


# -----------------------------
# Fetch Web Page
# -----------------------------
def fetch_page(url):
    """
    Fetch webpage and return BeautifulSoup object.
    """

    response = requests.get(url, timeout=10)

    if response.status_code != 200:
        print(f"Failed to fetch: {url}")
        return None

    return BeautifulSoup(response.text, "html.parser")


# -----------------------------
# Convert Price
# -----------------------------
def convert_price(price):

    price = price.replace("Â", "")
    price = price.replace("£", "")

    price_gbp = float(price)

    price_inr = round(price_gbp * 105.50, 2)

    return price_gbp, price_inr


# -----------------------------
# Convert Rating
# -----------------------------
def convert_rating(star_rating):

    rating_map = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5
    }

    return rating_map[star_rating]


# -----------------------------
# Get Availability
# -----------------------------
def get_availability(book):

    availability = book.find(
        "p",
        class_="instock availability"
    ).text.strip()

    return "In stock" in availability


# -----------------------------
# Get Category
# -----------------------------
def get_category(page_url, relative_link):

    full_book_url = urljoin(page_url, relative_link)

    detail_soup = fetch_page(full_book_url)

    if detail_soup is None:
        return "Unknown"

    breadcrumb = detail_soup.find(
        "ul",
        class_="breadcrumb"
    )

    items = breadcrumb.find_all("li")

    return items[2].text.strip()


# -----------------------------
# Scrape Books
# -----------------------------
def scrape_books():

    books_details = []

    for page_number in range(1, 6):

        print(f"Scraping Page {page_number}...")

        page_url = f"{BASE_URL}catalogue/page-{page_number}.html"

        soup = fetch_page(page_url)

        if soup is None:
            continue

        books = soup.find_all(
            "article",
            class_="product_pod"
        )

        for book in books:

            # Title
            title = book.h3.a["title"]

            # Price
            price = book.find(
                "p",
                class_="price_color"
            ).text.strip()

            price_gbp, price_inr = convert_price(price)

            # Rating
            star_rating = book.find(
                "p",
                class_="star-rating"
            )["class"][1]

            rating = convert_rating(star_rating)

            # Availability
            in_stock = get_availability(book)

            # Category
            relative_link = book.h3.a["href"]

            category = get_category(
                page_url,
                relative_link
            )

            # Dictionary
            book_data = {

                "title": title,

                "price_gbp": price_gbp,

                "price_inr": price_inr,

                "rating": rating,

                "in_stock": in_stock,

                "category": category

            }

            books_details.append(book_data)

    return books_details


# -----------------------------
# Create Database
# -----------------------------
def create_database():


    db_path = os.path.join("data_pipeline", "books.db")

    conn = sqlite3.connect(db_path)

    cursor = conn.cursor()

    
    cursor.execute("DROP TABLE IF EXISTS books")
    cursor.execute("DROP TABLE IF EXISTS categories")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categories(

        category_id INTEGER PRIMARY KEY AUTOINCREMENT,

        category_name TEXT UNIQUE

    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS books(

        book_id INTEGER PRIMARY KEY AUTOINCREMENT,

        title TEXT,

        price_gbp REAL,

        price_inr REAL,

        rating INTEGER,

        in_stock BOOLEAN,

        category_id INTEGER,

        FOREIGN KEY(category_id)
        REFERENCES categories(category_id)

    )
    """)

    conn.commit()

    print("Database Created Successfully.")

    return conn, cursor

# -----------------------------
# Insert Categories
# -----------------------------
def insert_categories(df, conn, cursor):

    # Get unique categories
    unique_categories = df["category"].unique()

    # Loop through each category
    for category in unique_categories:

        cursor.execute(
            """
            INSERT OR IGNORE INTO categories(category_name)
            VALUES(?)
            """,
            (category,)
        )

    conn.commit()

    print("Categories Inserted Successfully.")

# -----------------------------
# Insert Books
# -----------------------------
def insert_books(df, conn, cursor):
    # Remove old data
    cursor.execute("DELETE FROM books")
    conn.commit()

    for _, row in df.iterrows():

        # Get Category ID
        cursor.execute(
            """
            SELECT category_id
            FROM categories
            WHERE category_name = ?
            """,
            (row["category"],)
        )

        category_id = cursor.fetchone()[0]

        # Insert Book
        cursor.execute(
            """
            INSERT INTO books(
                title,
                price_gbp,
                price_inr,
                rating,
                in_stock,
                category_id
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                row["title"],
                row["price_gbp"],
                row["price_inr"],
                row["rating"],
                row["in_stock"],
                category_id
            )
        )

    conn.commit()

    print("Books Inserted Successfully.")

# -----------------------------
# Show Books
# -----------------------------
def show_books(cursor):

    cursor.execute("""
    SELECT
        b.title,
        b.price_gbp,
        b.price_inr,
        b.rating,
        b.in_stock,
        c.category_name
    FROM books b
    JOIN categories c
    ON b.category_id = c.category_id
    LIMIT 5
    """)

    rows = cursor.fetchall()

    print("\nFirst 5 Books From Database\n")

    for row in rows:
        print(row)


# -----------------------------
# SQL Queries
# -----------------------------
def run_queries(cursor):

    print("\n========== QUERY 1 ==========")

    cursor.execute("""
    SELECT title, price_inr
    FROM books
    WHERE rating = 5
    """)

    print(cursor.fetchall())


    print("\n========== QUERY 2 ==========")

    cursor.execute("""
    SELECT title, price_gbp
    FROM books
    ORDER BY price_gbp DESC
    LIMIT 10
    """)

    print(cursor.fetchall())


    print("\n========== QUERY 3 ==========")

    cursor.execute("""
    SELECT DISTINCT rating
    FROM books
    ORDER BY rating
    """)

    print(cursor.fetchall())


    print("\n========== QUERY 4 ==========")

    cursor.execute("""
    SELECT title, price_gbp
    FROM books
    WHERE rating IN (4,5)
    """)

    print(cursor.fetchall())


    print("\n========== QUERY 5 ==========")

    cursor.execute("""
    SELECT
        b.title,
        c.category_name,
        b.rating
    FROM books b
    JOIN categories c
    ON b.category_id = c.category_id
    ORDER BY b.rating DESC
    LIMIT 10
    """)

    print(cursor.fetchall())


# -----------------------------
# Read SQL Query using Pandas
# -----------------------------
def read_sql_queries(conn):

    print("\n========== PANDAS READ_SQL QUERY 1 ==========\n")

    query1 = """
    SELECT *
    FROM books
    WHERE rating = 5
    """

    df_query1 = pd.read_sql(query1, conn)

    print(df_query1.head())

    print("\n========== PANDAS READ_SQL QUERY 2 ==========\n")

    query2 = """
    SELECT
        b.title,
        c.category_name,
        b.rating
    FROM books b
    JOIN categories c
    ON b.category_id = c.category_id
    """

    df_query2 = pd.read_sql(query2, conn)

    print(df_query2.head())

    return df_query2

# -----------------------------
# Merge using Pandas
# -----------------------------
def merge_dataframes(conn):

    print("\n========== PANDAS MERGE ==========\n")

    books_df = pd.read_sql(
        "SELECT * FROM books",
        conn
    )

    categories_df = pd.read_sql(
        "SELECT * FROM categories",
        conn
    )

    merged_df = pd.merge(
        books_df,
        categories_df,
        on="category_id"
    )

    print(
        merged_df[
            ["title", "category_name", "rating"]
        ].head()
    )

    return merged_df

# -----------------------------
# Compare Outputs
# -----------------------------
def compare_results(df_query2, merged_df):

    print("\n========== COMPARISON ==========\n")

    print("SQL JOIN Result\n")
    print(df_query2.head())

    print("\nPandas Merge Result\n")
    print(
        merged_df[
            ["title", "category_name", "rating"]
        ].head()
    )

# -----------------------------
# Export CSV
# -----------------------------
def export_csv(df):

    df.to_csv(
        "data_pipeline/books_data.csv",
        index=False
    )

    print("\nCSV Exported Successfully.")

# -----------------------------
# Main Function
# -----------------------------
def main():

    print("=" * 50)
    print("BOOK DATA PIPELINE")
    print("=" * 50)

    # Step 1
    books = scrape_books()

    # Step 2
    print("\nBooks Scraped Successfully!")
    print("Total Books:", len(books))

    # Step 3
    df = pd.DataFrame(books)

    # Step 4
    conn, cursor = create_database()

    insert_categories(df, conn, cursor)
    insert_books(df, conn, cursor)
    cursor.execute("""
       SELECT COUNT(*)
       FROM books
        """)

    print(cursor.fetchone())

    # Step 5
    show_books(cursor)
    run_queries(cursor)

    df_query2 = read_sql_queries(conn)

    merged_df = merge_dataframes(conn)

    compare_results(df_query2, merged_df)

    export_csv(df)

    print("\nFirst 5 Books")
    print(df.head())

    print("\nShape")
    print(df.shape)

    print("\nData Types")
    print(df.dtypes)

    conn.close()

# -----------------------------
# Program Starts Here
# -----------------------------
if __name__ == "__main__":
    main()
