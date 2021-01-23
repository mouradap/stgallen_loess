from methods.model_data import StGallen
import argparse
import os
import warnings

warnings.filterwarnings('ignore')

ap = argparse.ArgumentParser()
ap.add_argument('-i', '--input', required = True,
                help='Provide a CSV file containing the symptoms report by ID.')
ap.add_argument('-o', '--output', required = False,
                help='Provide the path to the output folder. Default: /output/' )
ap.add_argument('-s', '--start', required = False,
                help='Provide a start date as a YYYY-MM-DD formatted string.')
ap.add_argument('-e', '--end', required = False,
                help='Provide a end date as a YYYY-MM-DD formatted string.')

args = vars(ap.parse_args())
model = StGallen()

if 'start' in args and 'end' in args:
    model.preprocess(args['input'], start_date = args['start'], end_date = args['end'])
elif 'start' in args:
    model.preprocess(args['input'], start_date = args['start'])
elif 'end' in args:
    model.preprocess(args['input'], end_date = args['end'])
else:
    model.preprocess(args['input'])

if args['output']:
    model.save_data(os.path.join(args['output'], 'dashboard.html'))
else:
    model.save_data()