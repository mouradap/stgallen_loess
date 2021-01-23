# stgallen_loess
A Python module to extract symptom percentage and produce an interactive html plot from it.

# Usage:
Install requirements with <br> pip install -r requirements.txt <br>

Either instantiate the class StGallen from methods.model_data and run model.preprocess(PATH_TO_CSV_FILE) <br>
Or run <br>
python main.py -i PATH_TO_CSV_FILE

Optional arguments
-o --output: Specify a folder to save the output HTML plot file. <br>
-s --start: Specify a starting date for your analysis, with the YYYY-MM-DD format. <br>
-e --end: Specify an ending date for your analysis, with the YYYY-MM-DD format.
