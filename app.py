from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient
from bson import ObjectId
app = Flask(__name__)

# MongoDB configuration
MONGO_URI = "mongodb://localhost:27017/tasksDB"
client = MongoClient(MONGO_URI)
db = client.get_database()


# Routes
@app.route('/')
def index():
    # Retrieve tasks from MongoDB
    tasks = db.tasks.find({})
    return render_template('index.html', tasks=tasks)


@app.route('/add_task', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        # Get task data from form
        title = request.form['title']
        description = request.form['description']

        # Insert task into database
        db.tasks.insert_one({'title': title, 'description': description})
        return redirect(url_for('index'))
    return render_template('add_task.html')


@app.route('/update_task/<task_id>', methods=['GET', 'POST'])
def update_task(task_id):
    task = db.tasks.find_one({'_id': task_id})
    if request.method == 'POST':
        # Get new task data from form
        new_title = request.form['title']
        new_description = request.form['description']

        # Update task in database
        db.tasks.update_one({'_id': task_id}, {'$set': {'title': new_title, 'description': new_description}})
        return redirect(url_for('index'))
    return render_template('edit_task.html', task=task)


@app.route('/delete_task/<task_id>', methods=['POST'])
def delete_task(task_id):
    try:
        # Delete task from database
        result = db.tasks.delete_one({'_id': ObjectId(task_id)})

        if result.deleted_count == 1:
            return jsonify({'message': 'Task deleted successfully'})
        else:
            return jsonify({'message': 'Task not found'}), 404  # Return 404 status code if task not found
    except Exception as e:
        return jsonify({'message': str(e)}), 500  # Return 500 status code for internal server error




if __name__ == '__main__':
    app.run(debug=True)
