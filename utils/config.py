import logging
import os
import yaml

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def load_config_file(config_file='config.yml'):
    """
   Currently we load from YAML for the heck of it - it contains stuff for
   working with proxies buckets and queues.

   :param config_file: The path and name to our configuration YAML.
   :return: Config dictionary for other functions and methods to use.
   """
    logger.info("Loading config %s", config_file)

    try:
        with open(config_file) as config_str:
            if config_file.endswith('.tmpl'):
                import jinja2
                template = jinja2.Template(config_str.read())
                config = yaml.load(template.render(env=os.environ), Loader=yaml.Loader)
            else:
                config = yaml.load(config_str, Loader=yaml.Loader)
    except (IOError, FileNotFoundError):
        logger.exception("Failed to open config file %s", config_file)
    else:
        return config


def get_config():
    config = os.getenv('CONFIG_FILE', 'config.yml')
    return load_config_file(config)


def generate_config_yaml(tmpl_dir):
    yaml_dict = load_config_file(config_file=tmpl_dir + 'config.tmpl')
    with open(tmpl_dir + 'config.yml', 'w') as outfile:
        yaml.dump(yaml_dict, outfile, default_flow_style=False)


if __name__ == '__main__':
    generate_config_yaml("")
    config = get_config()
