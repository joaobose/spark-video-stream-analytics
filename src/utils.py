import yaml

def load_config(file_path: str):
  """Loads camera stream configuration from a yaml file.
  """
  with open(file_path, 'r') as stream:
    try:
      return yaml.safe_load(stream)
    except yaml.YAMLError as exc:
      print(exc)
      return None
  