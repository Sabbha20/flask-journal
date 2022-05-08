import datetime
import os
# import sys
from flask import Flask, render_template, redirect, request, url_for
from pymongo import MongoClient

from dotenv import load_dotenv

load_dotenv()

def create_app():

    app = Flask(__name__)
    client = MongoClient(os.environ.get("MONGODB_URI"))

    app.db = client.microblog

    @app.route('/', methods=["GET", "POST"])
    def home():
        # print([e for e in app.db.entries.find({})])
        if request.method == 'POST':
            entry_content = request.form.get('entry')
            formatted_date = datetime.datetime.today().strftime("%b %d, %Y")
            # entries.append((entry_content, formatted_date))
            app.db.entries.insert_one({"content": entry_content , "date": formatted_date})
            return redirect(url_for('home'))
        entries_with_formatted_date = [
                (
                    entry["content"],
                    entry["date"],
                    datetime.datetime.strptime(entry["date"],"%b %d, %Y").strftime("%Y-%m-%d")
                )
                for entry in app.db.entries.find({})
            ]
        return render_template('home.html', entries=entries_with_formatted_date)

    
    return app



# if __name__=='__main__':
#     app.run(debug=True)