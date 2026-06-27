import sys
sys.stdout = open('stdout.log', 'w')
sys.stderr = open('stderr.log', 'w')

print("Starting Flask app...")
print(f"Python version: {sys.version}")

try:
    from app import app
    print("App imported successfully")
    app.run(debug=True, port=5000)
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
