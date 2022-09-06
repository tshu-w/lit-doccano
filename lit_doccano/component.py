import subprocess
import os
from pathlib import Path
from string import Template
from typing import Optional, Union, List

import lightning as L

# dir where doccano python venv will be setup
doccano_venv        = "venv-doccano"

class DoccanoBuildConfig(L.BuildConfig):
  def build_commands(self) -> List[str]:
    return [
        "sudo apt-get update",
        "sudo apt-get install nginx",
        f"virtualenv ~/{doccano_venv}",
        f". ~/{doccano_venv}/bin/activate; which python; python -m pip install doccano; deactivate",
    ]

class LitDoccano(L.LightningWork):
    def __init__(self, *args, cloud_build_config=DoccanoBuildConfig(), **kwargs) -> None:
        super().__init__(*args, cloud_build_config=cloud_build_config, **kwargs)

    def run(self):
        # prepare nginx conf with host and port numbers filled in
        conf_file = os.path.join(Path(__file__).parent.absolute(), "nginx.conf")
        new_conf_file = os.path.join(Path(__file__).parent.absolute(), "nginx-new.conf")
        new_conf = open(new_conf_file, "w")
        print(f"{conf_file}")
        for l in open(conf_file).readlines():
            print(l)
            new_conf.write(Template(l).substitute(host='0.0.0.0', port=self.port, internal_port=8000))
        new_conf.close()

        # run reverse proxy on external port and remove x-frame-options
        subprocess.run(
            f"nginx -c {new_conf_file}",
            shell=True
        )

        cmd = "source ~/venv-doccano/bin/activate;doccano init;deactivate"
        subprocess.run(cmd, shell=True)

        cmd = "source ~/venv-doccano/bin/activate;doccano createuser --username admin --password pass;deactivate"
        subprocess.run(cmd, shell=True)

        cmd = f"source ~/venv-doccano/bin/activate;export USE_ENFORCE_CSRF_CHECKS=false; doccano webserver;deactivate"
        subprocess.run(cmd, shell=True)

        cmd = "source ~/venv-doccano/bin/activate;doccano task;deactivate"
        subprocess.run(cmd, shell=True)

