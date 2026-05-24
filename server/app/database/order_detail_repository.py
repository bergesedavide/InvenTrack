from app.database.database_connection import get_supabase_client
from app.utils.data_types_creation import DataManipulation
from app.config import DbTables
from typing import List, Dict, Any, Optional
from enum import Enum

class OrderDetailRepository:
    def __init__(self):
        self.db = get_supabase_client()
        self.dataManipulator = DataManipulation()

    class DatabaseColName(Enum):
        ID = "id"
        IDORDINE = "idOrdine"
        IDPRODOTTO = "idProdotto"
        QUANTITA = "quantita"
        PREZZO_UNITARIO = "prezzo_unitario"
        SUBTOTALE = "subtotale"

    def get_details_by_order(self, order_id: int) -> List[Dict[str, Any]]:
        """Recupera tutti i dettagli di un ordine"""
        response = self.db.table(DbTables.ORDER_DETAILS.value).select("*").eq(self.DatabaseColName.IDORDINE.value, order_id).execute()
        
        details = response.data
        for d in details:
            d["id_ordine"] = d.pop("idOrdine", None)
            d["id_prodotto"] = d.pop("idProdotto", None)
            d["prezzo_unitario"] = d.pop("prezzo_unitario", None)
        
        return details

    def add_detail(self, id_ordine: int, id_prodotto: int, quantita: int, prezzo_unitario: float) -> Dict[str, Any]:
        """Aggiunge un prodotto a un ordine"""
        subtotale = quantita * prezzo_unitario
        
        detail_data = {
            self.DatabaseColName.IDORDINE.value: id_ordine,
            self.DatabaseColName.IDPRODOTTO.value: id_prodotto,
            self.DatabaseColName.QUANTITA.value: quantita,
            self.DatabaseColName.PREZZO_UNITARIO.value: prezzo_unitario,
            self.DatabaseColName.SUBTOTALE.value: subtotale
        }
        
        response = self.db.table(DbTables.ORDER_DETAILS.value).insert(detail_data).execute()
        
        if response.data:
            # Ricalcola il totale dell'ordine
            self._recalculate_order_total(id_ordine)
            return response.data[0]
        return {}

    def remove_detail(self, detail_id: int) -> bool:
        """Rimuove un prodotto da un ordine"""
        # Prima ottieni l'id_ordine
        detail = self.db.table(DbTables.ORDER_DETAILS.value).select(self.DatabaseColName.IDORDINE.value).eq(self.DatabaseColName.ID.value, detail_id).execute()
        
        if detail.data:
            order_id = detail.data[0].get(self.DatabaseColName.IDORDINE.value)
            
            response = self.db.table(DbTables.ORDER_DETAILS.value).delete().eq(self.DatabaseColName.ID.value, detail_id).execute()
            
            if response.data:
                self._recalculate_order_total(order_id)
                return True
        
        return False

    def _recalculate_order_total(self, order_id: int) -> None:
        """Ricalcola il totale dell'ordine chiamando la funzione SQL"""
        self.db.rpc("calcola_totale_ordine", {"p_idordine": order_id}).execute()