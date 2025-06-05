from flask import Flask, render_template_string
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

@app.route("/")
def display_dataframe():
    # File path
    file_path = r"C:\\Users\\avram\\OneDrive\\Desktop\\TRG Week 27\\jnj.us.txt"
    
    try:
        # Read the file into a DataFrame
        df = pd.read_csv(file_path, header=None, names=[
            "Date", "Open", "High", "Low", "Close", "Volume", "OpenInt"
        ], skiprows=1)

        # Drop the "OpenInt" column
        df = df.drop(columns=["OpenInt"])

        # Ensure Date is parsed correctly
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df = df.dropna(subset=['Date'])

        # Filter rows by date range
        df = df[(df['Date'] >= '1970-01-01') & (df['Date'] <= '2009-12-31')]
        
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

@app.route("/six_month_avg")
def six_month_avg():
    # File path
    file_path = r"C:\\Users\\avram\\OneDrive\\Desktop\\TRG Week 27\\jnj.us.txt"

    try:
        # Read the file into a DataFrame
        df = pd.read_csv(file_path, header=None, names=[
            "Date", "Open", "High", "Low", "Close", "Volume", "OpenInt"
        ], skiprows=1)

        # Drop the "OpenInt" column
        df = df.drop(columns=["OpenInt"])

        # Ensure Date is parsed correctly
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df = df.dropna(subset=['Date'])

        # Set Date as index
        df.set_index('Date', inplace=True)

        # Calculate 6-month rolling average for "Open" price
        df['6_Month_Avg_Open'] = df['Open'].rolling(window=6).mean()
        
        # Calculate 6-month rolling average for "Close" price
        df['6_Month_Avg_Close'] = df['Close'].rolling(window=6).mean()

        # Plot the 6-month average "Open" and "Close" prices
        plt.figure(figsize=(10, 6))
        plt.plot(df.index, df['6_Month_Avg_Open'], label='6-Month Avg Open', color='blue')
        plt.plot(df.index, df['6_Month_Avg_Close'], label='6-Month Avg Close', color='green')
        plt.title('6-Month Average Prices (Open and Close)')
        plt.xlabel('Date')
        plt.ylabel('Average Price')
        plt.legend()
        plt.grid()

        # Save the plot to a BytesIO object
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode('utf8')
        img.close()

        # Basic HTML template for the plot
        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>6-Month Average Prices</title>
        </head>
        <body>
            <div class="container mt-4">
                <h1 class="text-center">6-Month Average Prices (Open and Close)</h1>
                <img src="data:image/png;base64,{{ plot_url }}" class="img-fluid" />
            </div>
        </body>
        </html>
        """

        return render_template_string(html_template, plot_url=plot_url)

    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    app.run(debug=True)
