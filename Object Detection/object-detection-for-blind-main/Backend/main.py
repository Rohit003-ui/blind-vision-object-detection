import webview
import subprocess


def run_main_code():
    try:
        # Running main code
        subprocess.run(["python", "main_code.py"], check=True)
        print("main_code.py executed successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

# HTML content with a button to trigger the Python script
html_content = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Run Python Script</title>
</head>
<body>
    <h1>Click the button to run main_code.py</h1>
    <button onclick="pywebview.api.run_main_code()">Try</button>
</body>
</html>
'''

if __name__ == '__main__':
    # pywebview window
    window = webview.create_window('Run Python Script', html=html_content)

    # function to be called when the button is clicked
    webview.start(run_main_code, window)
