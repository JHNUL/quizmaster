from os import path
from robot import run

script_folder = path.dirname(__file__)
parent_folder = path.join(script_folder, "..")

options = {
    'outputdir': f"{parent_folder}/test-results",
    'log': 'log.html',
    'report': 'report.html'
}

run(f"{script_folder}", **options)
