from flask import Flask, render_template, request, redirect, url_for
import psycopg2
from datetime import datetime

app = Flask(__name__)

# Database connection function
def get_db_connection():
    connection = psycopg2.connect(
        host='db-cc.co4twflu4ebv.us-east-1.rds.amazonaws.com',
        port=5432,
        user='master',
        password='MasterPassword',
        database='lion_leftovers'
    )
    return connection

@app.route("/")
def index():
    return render_template('index.html')


@app.route('/student_reviews')
def student_reviews():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Reviews") 
    reviews = cursor.fetchall()
    # cursor.close()
    # conn.close()
    return render_template('student_reviews.html', reviews=reviews)

@app.route('/add_review', methods=['GET', 'POST'])
def add_review():
    if request.method == 'POST':
        conn = get_db_connection()
        cursor = conn.cursor()

        student_uni = request.form['student_uni']
        order_id = request.form['order_id']
        rating = request.form['rating']
        comment = request.form['comment']
        review_time = datetime.now()  

        cursor.execute("INSERT INTO Reviews (StudentUNI, OrderID, Rating, Comment, ReviewTime) VALUES (%s, %s, %s, %s, %s)",
                       (student_uni, order_id, rating, comment, review_time))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('student_reviews'))

    return render_template('add_review.html')

@app.route('/edit_review/<int:review_id>', methods=['GET', 'POST'])
def edit_review(review_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        rating = request.form['rating']
        comment = request.form['comment']
        updated_time = datetime.now()  # Get the current date and time

        cursor.execute("UPDATE Reviews SET Rating = %s, Comment = %s, ReviewTime = %s WHERE ReviewID = %s",
                       (rating, comment, updated_time, review_id))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('student_reviews'))

    cursor.execute("SELECT * FROM Reviews WHERE ReviewID = %s", (review_id,))
    review = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('edit_review.html', review=review)

@app.route('/manage_reviews')
def manage_reviews():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Reviews")
    reviews = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('manage_reviews.html', reviews=reviews)

@app.route('/delete_review/<int:review_id>', methods=['POST'])
def delete_review(review_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Reviews WHERE ReviewID = %s", (review_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('manage_reviews'))

if __name__ == '__main__':
    app.run(debug=True, port=8012)
