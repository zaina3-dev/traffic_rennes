import json
from flask import Flask, render_template, request, flash, jsonify
from traffic_rennes_elasticsearch_utils import  read_json, Config

DEBUG = True
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

jsonFile = "param.json"


@app.route("/", methods=["GET", "POST"])
def results():
    title = "Tests"
    file_data = ""
    submission_successful = False
    if request.method == "POST":
        print(request.form)
        with open(jsonFile, "w+") as f:
            json.dump(request.form, f)
        submission_successful = True
        flash('Les paramêtres sont sauvegardés')

    #  filepath = ".run_traffic_elasticsearch.bat"
    #  p = subprocess.Popen(filepath, shell=True, stdout=subprocess.PIPE)
    #  stdout, stderr = p.communicate()
    #  print(p.returncode)  # is 0 if success

    # charge le fichier json , charge les paraméters par défauts
    try:
        with open(jsonFile) as f:
            file_data = json.load(f)
            f.close()
            flash('Configuration chargée')
    except:
        file_data = Config.query.all()
        submission_successful = "Absent de fichier . Paramétres par défaut "
    return render_template('index.html', data=file_data, submission=submission_successful)


if __name__ == "__main__":
    app.run()
