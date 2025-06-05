from flask import Flask, render_template_string
import pandas as pd

app = Flask(__name__)

@app.route("/")
def display_dataframe():
    # File path
    file_path = r"C:\\Users\\avram\\OneDrive\\Desktop\\TRG Week 27\\jnj.us.txt"
    
    try:
        # Read the file into a DataFrame
        df = pd.read_csv(file_path, header=0,names=[
            "Date", "Open", "High", "Low", "Close", "Volume", "OpenInt"
        ])

        # Drop the "OpenInt" column
        df = df.drop(columns=["OpenInt"])
        
        # Convert DataFrame to HTML
        df_html = df.to_html(classes='table table-striped', index=False)

        # Basic HTML template
        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <link rel="stylesheet" 
                  href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css">
            <title>DataFrame Display</title>
        </head>
        <body>
            <div class="container mt-4">
                <h1 class="text-center">JNJ DataFrame</h1>
                {{ table|safe }}
            </div>
        </body>
        </html>
        """

        return render_template_string(html_template, table=df_html)

    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    app.run(debug=True)
