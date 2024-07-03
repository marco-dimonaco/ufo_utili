from dataclasses import dataclass
from model.stati import Stato


@dataclass
class Connessione:
    st1: Stato
    st2: Stato
