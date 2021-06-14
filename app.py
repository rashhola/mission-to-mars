# import Flask, pymongo, and scrape_mars (your python file)

from flask import Flask, render_template
from flask_pymongo import PyMongo
import scrape_mars

# Instantiate a Flask app
app = Flask(__name__)


# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/marsmission"

mongo = PyMongo(app)


# Create a base '/' route that will query your mongodb database and render the `index.html` template
@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)


# Create a '/scrape' route that will create the mars collection, run your scrape() function from scrape_mars, and update the mars collection in the database
# The route should redirect back to the base route '/' with a code 302.
@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_data = scrape_mars.scrape_all()
    mars.replace_one({}, mars_data, upsert=True)
    return "Scraping okay!"



# Run your appp
if __name__ == "__main__":
    app.run()