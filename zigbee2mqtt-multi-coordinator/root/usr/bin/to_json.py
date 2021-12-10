#!/usr/bin/python3

import sys, yaml, json

yaml_arg = yaml.safe_load(sys.argv[1])
yaml_object = yaml.load(yaml_arg, yaml.Loader)
print(json.dumps(yaml_object))
