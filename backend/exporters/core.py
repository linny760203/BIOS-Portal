from jinja2 import Environment, FileSystemLoader
import os
from datetime import datetime

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "templates")
EXPORT_DIR = os.path.join(os.path.dirname(__file__), "../../data/exported")

jinja_env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

def export_me_xml(project_name, version, settings, user):
    os.makedirs(EXPORT_DIR, exist_ok=True)
    template = jinja_env.get_template("me_config.xml.j2")
    output = template.render(
        project_name=project_name,
        version=version,
        settings=settings,
        user=user,
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    file_path = os.path.join(EXPORT_DIR, f"{project_name}_ME_{version}.xml")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(output)
    return file_path

def export_gpio_h(project_name, gpio_settings):
    os.makedirs(EXPORT_DIR, exist_ok=True)
    template = jinja_env.get_template("gpio_cfg.h.j2")
    output = template.render(
        project_name=project_name,
        gpio_settings=gpio_settings,
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    file_path = os.path.join(EXPORT_DIR, f"{project_name}_gpio_cfg.h")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(output)
    return file_path
