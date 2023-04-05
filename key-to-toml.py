import toml

output_file = "secrets.toml"

with open("solar-modem-381304-firebase-adminsdk-c5f7c-ec920a0c4c.json") as json_file:
    json_text = json_file.read()

config = {"textkey": json_text}
toml_config = toml.dumps(config)

with open(output_file, "w") as target:
    target.write(toml_config)