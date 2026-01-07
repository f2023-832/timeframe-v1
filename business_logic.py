import data_access
from werkzeug.security import generate_password_hash, check_password_hash

def validate_login(username, password):
    """
    Verifies user credentials using password hashing.
    Returns the user object if valid, None otherwise.
    """
    user = data_access.get_user_by_username(username)
    if not user:
        return None
        
    # Check hashed password
    # NOTE: This will fail for OLD users who have plain text passwords.
    # To support old users temporarily, we could add a fallback, strictly enforcing security now.
    if check_password_hash(user['password'], password):
        return user
    return None

def register_user(username, password):
    """
    Registers a new user with a hashed password.
    Returns:
        (True, None) on success
        (False, error_message) on failure
    """
    # Check if username already exists
    existing_user = data_access.get_user_by_username(username)
    if existing_user:
        return False, "Username taken."
    
    try:
        hashed_password = generate_password_hash(password)
        data_access.create_user(username, hashed_password)
        return True, None
    except Exception as e:
        return False, str(e)

def get_user_tasks(user_id):
    """
    Retrieves all tasks for a specific user.
    """
    try:
        return data_access.get_tasks_for_user(user_id)
    except Exception as e:
        print(f"Error fetching tasks: {e}")
        return []

def add_new_task(user_id, name, urgency, importance):
    """
    Determines task category based on urgency/importance and saves the task.
    Returns:
        (True, None) on success
        (False, error_message) on failure
    """
    # Eisenhower Matrix Logic
    if urgency == 'urgent' and importance == 'important':
        category = 'Q1'
    elif urgency == 'not_urgent' and importance == 'important':
        category = 'Q2'
    elif urgency == 'urgent' and importance == 'not_important':
        category = 'Q3'
    else:
        category = 'Q4'

    try:
        data_access.create_task(user_id, name, category)
        return True, None
    except Exception as e:
        return False, str(e)

def mark_task_complete(task_id):
    try:
        data_access.complete_task(task_id)
        return True
    except Exception as e:
        print(f"Error completing task: {e}")
        return False

def remove_task(task_id):
    try:
        data_access.delete_task(task_id)
        return True
    except Exception as e:
        print(f"Error deleting task: {e}")
        return False
