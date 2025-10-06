from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.db_connect import get_db

tasks_bp = Blueprint('tasks', __name__, url_prefix='/tasks')

@tasks_bp.route('/')
def list_tasks():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        SELECT tasks.*, projects.name as project_name
        FROM tasks
        JOIN projects ON tasks.project_id = projects.id
        ORDER BY tasks.created_at DESC
    ''')
    tasks = cursor.fetchall()
    cursor.close()
    return render_template('tasks/list.html', tasks=tasks)

@tasks_bp.route('/create', methods=['GET', 'POST'])
def create_task():
    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        name = request.form['name']
        description = request.form.get('description', '')
        project_id = request.form['project_id']
        status = request.form.get('status', 'pending')

        cursor.execute('INSERT INTO tasks (name, description, project_id, status) VALUES (%s, %s, %s, %s)',
                      (name, description, project_id, status))
        db.commit()
        cursor.close()

        flash('Task created successfully!', 'success')
        return redirect(url_for('tasks.list_tasks'))

    cursor.execute('SELECT * FROM projects ORDER BY name')
    projects = cursor.fetchall()
    cursor.close()

    return render_template('tasks/create.html', projects=projects)

@tasks_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_task(id):
    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        name = request.form['name']
        description = request.form.get('description', '')
        project_id = request.form['project_id']
        status = request.form.get('status', 'pending')

        cursor.execute('UPDATE tasks SET name = %s, description = %s, project_id = %s, status = %s WHERE id = %s',
                      (name, description, project_id, status, id))
        db.commit()
        cursor.close()

        flash('Task updated successfully!', 'success')
        return redirect(url_for('tasks.list_tasks'))

    cursor.execute('SELECT * FROM tasks WHERE id = %s', (id,))
    task = cursor.fetchone()

    if not task:
        cursor.close()
        flash('Task not found!', 'error')
        return redirect(url_for('tasks.list_tasks'))

    cursor.execute('SELECT * FROM projects ORDER BY name')
    projects = cursor.fetchall()
    cursor.close()

    return render_template('tasks/edit.html', task=task, projects=projects)

@tasks_bp.route('/delete/<int:id>', methods=['POST'])
def delete_task(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = %s', (id,))
    db.commit()
    cursor.close()

    flash('Task deleted successfully!', 'success')
    return redirect(url_for('tasks.list_tasks'))
