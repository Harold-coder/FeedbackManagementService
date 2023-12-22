from flask import Flask, request, jsonify
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

@app.route('/student_reviews')
def student_reviews():
    conn = get_db_connection()
    cursor = conn.cursor()
    order_id = request.args.get('order_id', default=None, type=int)
    review_id = request.args.get('review_id', default=None, type=int)
    student_uni = request.args.get('student_uni', default=None, type=str)

    # Fetch reviews based on the query parameters
    if order_id is not None:
        cursor.execute("SELECT * FROM Reviews WHERE reviews.orderid = %s", (order_id,))
    elif review_id is not None:
        cursor.execute("SELECT * FROM Reviews WHERE reviews.reviewid = %s", (review_id,))
    elif student_uni is not None:
        cursor.execute("SELECT * FROM Reviews WHERE reviews.studentuni = %s", (student_uni,))
    else:
        cursor.execute("SELECT * FROM Reviews")

    reviews = cursor.fetchall()
    cursor.close()
    conn.close()
    formatted_reviews = [
        {
            "reviewid": review[0],
            "uni": review[1],
            "orderid": review[2],
            "inventory_id": review[3],
            "review": review[4],
            "date": review[5],
        }
        for review in reviews
    ]

    return jsonify(formatted_reviews)

@app.route('/add_review', methods=['POST'])
def add_review():
    conn = get_db_connection()
    cursor = conn.cursor()

    student_uni = request.form.get('student_uni')
    order_id = request.form.get('order_id')
    rating = request.form.get('rating')
    comment = request.form.get('comment')
    review_time = datetime.now()

    cursor.execute("INSERT INTO Reviews (StudentUNI, OrderID, Rating, Comment, ReviewTime) VALUES (%s, %s, %s, %s, %s)",
                   (student_uni, order_id, rating, comment, review_time))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"success": "Review added successfully"})

@app.route('/edit_review/<int:review_id>', methods=['POST'])
def edit_review(review_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    rating = request.form.get('rating')
    comment = request.form.get('comment')
    updated_time = datetime.now()

    cursor.execute("UPDATE Reviews SET Rating = %s, Comment = %s, ReviewTime = %s WHERE ReviewID = %s",
                   (rating, comment, updated_time, review_id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"success": "Review updated successfully"})

@app.route('/delete_review/<int:review_id>', methods=['POST'])
def delete_review(review_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Reviews WHERE ReviewID = %s", (review_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"success": "Review deleted successfully"})

@app.route("/")
def index():
    return jsonify({"message": "Welcome to the FeedbackManagement API Hosted on Docker!"})

if __name__ == '__main__':
    app.run(debug=True, port=8012)
