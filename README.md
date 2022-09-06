# lit_doccano component

This ⚡ [Lightning component](lightning.ai) ⚡ was generated automatically with:

```bash
lightning init component lit-doccano
```

## To run lit_doccano

First, install lit_doccano (warning: this component has not been officially approved on the lightning gallery):

```bash
lightning install component https://github.com/tshu-w/lit-doccano
```

## Setup virtualenv
  
NOTE: Use `Conda` for Lightning and use `venv` for the component. 

- setup vritual env
```bash
virtualenv ~/venv-doccano 
source ~/venv-venv-doccano/bin/activate;  python -m pip install venv-doccano; deactivate
```

- test 
```bash
source ~/venv-doccano/bin/activate; doccano --help; deactivate
```


Once the app is installed, use it in an app:

```python
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
```
