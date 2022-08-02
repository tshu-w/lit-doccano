from lit_doccano import LitDoccano

import lightning as L


class LitApp(L.LightningFlow):
    def __init__(self) -> None:
        super().__init__()
        self.lit_doccano = LitDoccano()

    def run(self):
        self.lit_doccano.run()

    def configure_layout(self):
        return [{'name': 'doccano', 'content': self.lit_doccano}]

app = L.LightningApp(LitApp())
