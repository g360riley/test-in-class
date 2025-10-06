from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.db_connect import get_db

projects_bp = Blueprint('projects', __name__, url_prefix='/projects')

@projects_bp.route('/', methods=['GET', 'POST'])
def list_projects():
    db = get_db()
    cursor = db.cursor()

    # Handle POST request to add a new project
    if request.method == 'POST':
        name = request.form['name']
        description = request.form.get('description', '')

        cursor.execute('INSERT INTO projects (name, description) VALUES (%s, %s)', (name, description))
        db.commit()

        flash('Project created successfully!', 'success')
        return redirect(url_for('projects.list_projects'))

    cursor.execute('SELECT * FROM projects ORDER BY created_at DESC')
    projects = cursor.fetchall()
    cursor.close()
    return render_template('projects/list.html', projects=projects)

@projects_bp.route('/update/<int:id>', methods=['POST'])
def update_project(id):
    db = get_db()
    cursor = db.cursor()

    name = request.form['name']
    description = request.form.get('description', '')

    cursor.execute('UPDATE projects SET name = %s, description = %s WHERE id = %s', (name, description, id))
    db.commit()
    cursor.close()

    flash('Project updated successfully!', 'success')
    return redirect(url_for('projects.list_projects'))

@projects_bp.route('/delete/<int:id>', methods=['POST'])
def delete_project(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('DELETE FROM projects WHERE id = %s', (id,))
    db.commit()
    cursor.close()

    flash('Project deleted successfully!', 'danger')
    return redirect(url_for('projects.list_projects'))
