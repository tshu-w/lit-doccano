import subprocess

import lightning as L

class LitDoccano(L.LightningWork):
    def run(self):
        cmd = "doccano init"
        subprocess.run(cmd, shell=True)

        cmd = "doccano createuser --username admin --password pass"
        subprocess.run(cmd, shell=True)

        cmd = f"doccano webserver --port {self.port}"
        subprocess.run(cmd, shell=True)

        cmd = "doccano task"
        subprocess.run(cmd, shell=True)
