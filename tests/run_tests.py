from os import path
from sys import argv
from robot import run

script_folder = path.dirname(__file__)
parent_folder = path.join(script_folder, "..")

options = {
    'outputdir': f"{parent_folder}/test-results",
    'log': 'log.html',
    'report': 'report.html',
    'loglevel': 'INFO'
}

if len(argv) > 1:
    options['include'] = argv[1]


exit_code = run(f"{script_folder}", **options)
exit(exit_code)
