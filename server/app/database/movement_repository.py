from app.database.database_connection import get_supabase_client
from app.utils.data_types_creation import DataManipulation
from app.config import DbTables
from typing import List, Dict, Any, Optional
from enum import Enum

class MovementRepository:
    def __init__(self):
        self.db = get_supabase_client()
        self.dataManipulator = DataManipulation()

    class DatabaseColName(Enum):
        ID = "id"
        IDPRODOTTO = "idProdotto"
        TIPO = "tipo"
        QUANTITA = "quantita"
        PREZZO_UNITARIO = "prezzo_unitario"
        DATA = "data"
        NOTE = "note"
        CREATED_AT = "created_at"

    def add_movement(self, id_prodotto: int, tipo: str, quantita: int, data: str, prezzo_unitario: float = None, note: str = None) -> Dict[str, Any]:
        """Aggiunge un movimento di magazzino"""
        movement_data = {
            self.DatabaseColName.IDPRODOTTO.value: id_prodotto,
            self.DatabaseColName.TIPO.value: tipo,
            self.DatabaseColName.QUANTITA.value: quantita,
            self.DatabaseColName.DATA.value: data,
            self.DatabaseColName.PREZZO_UNITARIO.value: prezzo_unitario,
            self.DatabaseColName.NOTE.value: note
        }
        
        response = self.db.table(DbTables.MOVEMENTS.value).insert(movement_data).execute()
        
        if response.data:
            return response.data[0]
        return {}

    def get_movements_by_product(self, product_id: int, limit: int = 50) -> List[Dict[str, Any]]:
        """Recupera tutti i movimenti di un prodotto"""
        response = self.db.table(DbTables.MOVEMENTS.value).select("*").eq(self.DatabaseColName.IDPRODOTTO.value, product_id).limit(limit).execute()
        
        movements = response.data
        for m in movements:
            m["id_prodotto"] = m.pop("idProdotto", None)
            m["prezzo_unitario"] = m.pop("prezzo_unitario", None)
        
        return movements

    def get_movements_by_date_range(self, from_date: str, to_date: str) -> List[Dict[str, Any]]:
        """Recupera i movimenti in un intervallo di date"""
        response = self.db.table(DbTables.MOVEMENTS.value).select("*").gte(self.DatabaseColName.DATA.value, from_date).lte(self.DatabaseColName.DATA.value, to_date).execute()
        
        return response.data

    def get_movement_stats(self) -> Dict[str, Any]:
        """Restituisce statistiche sui movimenti"""
        response = self.db.table(DbTables.MOVEMENTS.value).select("*").execute()
        movements = response.data
        
        total_in = sum(m.get(self.DatabaseColName.QUANTITA.value, 0) for m in movements if m.get(self.DatabaseColName.TIPO.value) == "entrata")
        total_out = sum(m.get(self.DatabaseColName.QUANTITA.value, 0) for m in movements if m.get(self.DatabaseColName.TIPO.value) == "uscita")
        
        return {
            "total_movements": len(movements),
            "total_in": total_in,
            "total_out": total_out,
            "net_change": total_in - total_out
        }