from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.db_connect import get_db

projects_bp = Blueprint('projects', __name__, url_prefix='/projects')

@projects_bp.route('/')
def list_projects():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM projects ORDER BY created_at DESC')
    projects = cursor.fetchall()
    cursor.close()
    return render_template('projects/list.html', projects=projects)

@projects_bp.route('/create', methods=['GET', 'POST'])
def create_project():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form.get('description', '')

        db = get_db()
        cursor = db.cursor()
        cursor.execute('INSERT INTO projects (name, description) VALUES (%s, %s)', (name, description))
        db.commit()
        cursor.close()

        flash('Project created successfully!', 'success')
        return redirect(url_for('projects.list_projects'))

    return render_template('projects/create.html')

@projects_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_project(id):
    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        name = request.form['name']
        description = request.form.get('description', '')

        cursor.execute('UPDATE projects SET name = %s, description = %s WHERE id = %s', (name, description, id))
        db.commit()
        cursor.close()

        flash('Project updated successfully!', 'success')
        return redirect(url_for('projects.list_projects'))

    cursor.execute('SELECT * FROM projects WHERE id = %s', (id,))
    project = cursor.fetchone()
    cursor.close()

    if not project:
        flash('Project not found!', 'error')
        return redirect(url_for('projects.list_projects'))

    return render_template('projects/edit.html', project=project)

@projects_bp.route('/delete/<int:id>', methods=['POST'])
def delete_project(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('DELETE FROM projects WHERE id = %s', (id,))
    db.commit()
    cursor.close()

    flash('Project deleted successfully!', 'success')
    return redirect(url_for('projects.list_projects'))
