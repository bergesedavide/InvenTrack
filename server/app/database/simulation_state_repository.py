from app.database.database_connection import get_supabase_client
from app.config import DbTables
from typing import Dict, Any, Optional
from datetime import datetime
from enum import Enum

class SimulationStateRepository:
    def __init__(self):
        self.db = get_supabase_client()

    class DatabaseColName(Enum):
        ID = "id"
        ATTIVA = "attiva"
        ULTIMO_AGGIORNAMENTO = "ultimo_aggiornamento"
        ORDINI_GENERATI = "ordini_generati"
        CLIENTI_GENERATI = "clienti_generati"
        MOVIMENTI_STOCK = "movimenti_stock"

    def get_state(self) -> Dict[str, Any]:
        """Recupera lo stato della simulazione"""
        response = self.db.table(DbTables.SIMULATION_STATE.value).select("*").eq(self.DatabaseColName.ID.value, 1).execute()
        
        if response.data:
            state = response.data[0]
            return {
                "attiva": state.get(self.DatabaseColName.ATTIVA.value, False),
                "ultimo_aggiornamento": state.get(self.DatabaseColName.ULTIMO_AGGIORNAMENTO.value),
                "ordini_generati": state.get(self.DatabaseColName.ORDINI_GENERATI.value, 0),
                "clienti_generati": state.get(self.DatabaseColName.CLIENTI_GENERATI.value, 0),
                "movimenti_stock": state.get(self.DatabaseColName.MOVIMENTI_STOCK.value, 0)
            }
        return {}

    def update_state(self, attiva: bool = None, ordini_generati: int = None, clienti_generati: int = None, movimenti_stock: int = None) -> Dict[str, Any]:
        """Aggiorna lo stato della simulazione"""
        update_data = {}
        
        if attiva is not None:
            update_data[self.DatabaseColName.ATTIVA.value] = attiva
        
        if ordini_generati is not None:
            update_data[self.DatabaseColName.ORDINI_GENERATI.value] = ordini_generati
        
        if clienti_generati is not None:
            update_data[self.DatabaseColName.CLIENTI_GENERATI.value] = clienti_generati
        
        if movimenti_stock is not None:
            update_data[self.DatabaseColName.MOVIMENTI_STOCK.value] = movimenti_stock
        
        if update_data:
            update_data[self.DatabaseColName.ULTIMO_AGGIORNAMENTO.value] = datetime.now().isoformat()
            self.db.table(DbTables.SIMULATION_STATE.value).update(update_data).eq(self.DatabaseColName.ID.value, 1).execute()
        
        return self.get_state()

    def increment_orders(self, increment: int = 1) -> Dict[str, Any]:
        """Incrementa il contatore degli ordini generati"""
        current = self.get_state()
        return self.update_state(ordini_generati=current.get("ordini_generati", 0) + increment)

    def increment_clients(self, increment: int = 1) -> Dict[str, Any]:
        """Incrementa il contatore dei clienti generati"""
        current = self.get_state()
        return self.update_state(clienti_generati=current.get("clienti_generati", 0) + increment)

    def increment_movements(self, increment: int = 1) -> Dict[str, Any]:
        """Incrementa il contatore dei movimenti stock"""
        current = self.get_state()
        return self.update_state(movimenti_stock=current.get("movimenti_stock", 0) + increment)

    def reset(self) -> Dict[str, Any]:
        """Resetta tutti i contatori"""
        return self.update_state(ordini_generati=0, clienti_generati=0, movimenti_stock=0)