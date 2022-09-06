import subprocess
import os
from pathlib import Path
from string import Template
from typing import Optional, Union, List

import lightning as L

# dir where doccano python venv will be setup
doccano_venv        = "venv-doccano"

# remove x-frame-options
nginx_conf = """
events {
  worker_connections 1024;
}
http {
    server {
      listen $port;    
      location / {
        proxy_pass http://$host:$internal_port;
        proxy_hide_header x-frame-options;
      }
  }
}
"""

class DoccanoBuildConfig(L.BuildConfig):
  def build_commands(self) -> List[str]:
    return [
        "sudo apt-get update",
        "sudo apt-get install nginx",
        "sudo touch /run/nginx.pid",
        "sudo chown -R `whoami` /etc/nginx/ /var/log/nginx/",
        "sudo chown -R `whoami` /var/lib/nginx/",
        "sudo chown `whoami` /run/nginx.pid",
        f"virtualenv ~/{doccano_venv}",
        f". ~/{doccano_venv}/bin/activate; which python; python -m pip install doccano; deactivate",
    ]

class LitDoccano(L.LightningWork):
    def __init__(self, *args, cloud_build_config=DoccanoBuildConfig(), **kwargs) -> None:
        super().__init__(*args, cloud_build_config=cloud_build_config, **kwargs)

    def run(self):
        # prepare nginx conf with host and port numbers filled in
        cwd = os.getcwd()
        new_conf_file = os.path.join(cwd, "nginx-new.conf")
        new_conf = open(new_conf_file, "w")
        for l in nginx_conf.splitlines():
            print(l)
            new_conf.write(Template(l).substitute(host='0.0.0.0', port=self.port, internal_port=8000))
        new_conf.close()

        # run reverse proxy on external port and remove x-frame-options
        cmd = f"nginx -c {new_conf_file}"
        subprocess.run(cmd, shell=True, executable="/bin/bash")

        cmd = "source ~/venv-doccano/bin/activate;doccano init;deactivate"
        subprocess.run(cmd, shell=True, executable="/bin/bash")

        cmd = "source ~/venv-doccano/bin/activate;doccano createuser --username admin --password pass;deactivate"
        subprocess.run(cmd, shell=True, executable="/bin/bash")

        cmd = f"source ~/venv-doccano/bin/activate;export USE_ENFORCE_CSRF_CHECKS=false; doccano webserver;deactivate"
        subprocess.run(cmd, shell=True, executable="/bin/bash")

        cmd = "source ~/venv-doccano/bin/activate;doccano task;deactivate"
        subprocess.run(cmd, shell=True, executable="/bin/bash")

