from supabase import create_client, Client
import os
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

# --- SUPABASE SETUP ---
SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY')

_supabase: Client = None

def get_client():
    global _supabase
    if _supabase:
        return _supabase
        
    if SUPABASE_URL and SUPABASE_KEY:
        try:
            _supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
            return _supabase
        except Exception as e:
            print(f"Supabase Init Error: {e}")
            return None
    return None

def get_user_by_username(username):
    client = get_client()
    if not client: raise Exception("Database connection failed")
    
    response = client.table('users').select("*").eq('username', username).execute()
    if response.data:
        return response.data[0]
    return None

def create_user(username, password):
    client = get_client()
    if not client: raise Exception("Database connection failed")
    
    client.table('users').insert({"username": username, "password": password}).execute()

def get_tasks_for_user(user_id):
    client = get_client()
    if not client: raise Exception("Database connection failed")
    
    response = client.table('tasks').select("*").eq('user_id', user_id).execute()
    return response.data

def create_task(user_id, name, category):
    client = get_client()
    if not client: raise Exception("Database connection failed")
    
    client.table('tasks').insert({
        "user_id": user_id,
        "name": name,
        "category": category,
        "status": 'pending'
    }).execute()

def complete_task(task_id):
    client = get_client()
    if not client: raise Exception("Database connection failed")
    
    client.table('tasks').update({"status": "completed"}).eq('id', task_id).execute()

def delete_task(task_id):
    client = get_client()
    if not client: raise Exception("Database connection failed")
    
    client.table('tasks').delete().eq('id', task_id).execute()
