from flask import Flask, render_template_string
import psycopg2
import pandas as pd
from credentials import PASSWORD, USER

# Initialize the Flask app
app = Flask(__name__)

# Database connection function
def get_db_connection():
    connection = psycopg2.connect(
        host='db-cc.co4twflu4ebv.us-east-1.rds.amazonaws.com',
        port=5432,
        user=USER,  # Use credentials imported from the credentials module
        password=PASSWORD,
        database='lion_leftovers'
    )
    return connection

# HTML template for rendering the reviews table
html_template = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Reviews Table</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.0/dist/css/bootstrap.min.css">
</head>
<body>
  <div class="container">
    <h1>Reviews Table</h1>
    {{ reviews_table|safe }}
  </div>
</body>
</html>
"""

@app.route("/")
def hello():
    """Return a friendly HTTP greeting."""
    return "Hello World! This is Order Management Service"

@app.route("/reviews")
def show_reviews():
    """Display the reviews in an HTML table."""
    # Get a database connection
    connection = get_db_connection()
    sql = "SELECT * FROM Reviews;"
    # Read the SQL query into a Pandas DataFrame
    reviews_df = pd.read_sql(sql, con=connection)
    # Convert the DataFrame to HTML table representation
    reviews_table = reviews_df.to_html(classes='table table-striped', index=False)
    connection.close()  # Close the database connection
    # Render the HTML page with the reviews table
    return render_template_string(html_template, reviews_table=reviews_table)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
