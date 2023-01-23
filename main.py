from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
import pandas as pd

# initialize the is_scraping_done variable
is_scraping_done = False
app = Flask(__name__)
df = pd.DataFrame()
# specify the folder where the static files are located
app = Flask(__name__, static_folder="static")

@app.route("/", methods=["GET", "POST"])
def index():
    global df,file_name
    if request.method == "POST":
        url = request.form["url"]
        # get the file name to save the excel sheet
        file_name = request.form["file_name"]
        # send a request to the website
        page = requests.get(url)

        # parse the html content
        soup = BeautifulSoup(page.content, "html.parser")

        # find all the profile elements on the page
        profiles = soup.find_all("div", class_="/QufQ9GGSZ6PcTuRM/ZRjg==")
        total_data = request.form["total_data"] # this line will get the value of total_data from user input
        total_data=int(total_data)
        print(profiles)
        


        # initialize empty lists to store the data
        email_list = []
        first_name_list = []
        last_name_list = []
        company_name_list = []

        # loop through the profiles and extract the data
        for profile in profiles:
            email = profile.find("span", class_="email").text
            email_list.append(email)
            first_name = profile.find("span", class_="first-name").text
            first_name_list.append(first_name)
            last_name = profile.find("span", class_="last-name").text
            last_name_list.append(last_name)
            company_name = profile.find("span", class_="company-name").text
            company_name_list.append(company_name)
            data = {"email": email, "first_name": first_name,"last_name": last_name, 
                "company_name": company_name}
            df = pd.concat([df, pd.DataFrame(data)])
            # check if the length of the data is equal to the total_data
            if len(email_list) >= total_data:
                is_scraping_done = True
                break
        
        


        # remove duplicate rows
        df = df.drop_duplicates()

        # export the data to an Excel file
        df.to_excel(f"{file_name}.xlsx", index=False)
        
    return render_template("index.html")

@app.route("/status")
def status():
    if is_scraping_done:
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "scraping"})
    
@app.route("/stop", methods=["POST"])
def stop():
    global is_scraping_done
    is_scraping_done = True
    if df is not None:
        df = df.drop_duplicates()
        df.to_excel(f"{file_name}.xlsx", index=False)
    return jsonify({"status": "stopped"})



    

if __name__ == "__main__":
    app.run(debug=True)
