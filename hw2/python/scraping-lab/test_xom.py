import json
import yahoo_options_data

computedJson = yahoo_options_data.contractAsJson("xom.dat")
expectedJson = open("xom.json").read()

if json.loads(computedJson) != json.loads(expectedJson):
  print("Test failed!")
  print("Expected output:", expectedJson)
  print("Your output:", computedJson)
  assert False
else:
  print("Test passed")
