from data_access import get_client
import os

print("--- Testing Supabase Connection ---")
client = get_client()

if not client:
    print("Client Init FAILED. Check credentials.")
else:
    print("Client Init SUCCESS.")
    print(f"URL: {os.environ.get('SUPABASE_URL')}")
    
    try:
        print("Checking 'users' table...")
        res = client.table('users').select("count", count='exact').execute()
        print(f"'users' table exists. Row count: {res.count}")
    except Exception as e:
        print(f"'users' table check FAILED: {e}")

    try:
        print("Checking 'tasks' table...")
        res = client.table('tasks').select("count", count='exact').execute()
        print(f"'tasks' table exists. Row count: {res.count}")
    except Exception as e:
        print(f"'tasks' table check FAILED: {e}")
