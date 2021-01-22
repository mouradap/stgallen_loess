from methods.model_data import StGallen
import argparse
import os

ap = argparse.ArgumentParser()
ap.add_argument('-d', '--data', required = True,
                help='Provide a CSV file containing the symptoms report by ID.')
ap.add_argument('-o', '--output', required = False,
                help='Provide the path to the output folder. Default: /output/' )

args = vars(ap.parse_args())

model = StGallen()

model.preprocess(args['data'])
if args['output']:
    model.save_data(os.path.join(args['output'], 'dashboard.html'))
else:
    model.save_data()