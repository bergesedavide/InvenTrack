from app.database.database_connection import get_supabase_client
from app.utils.data_types_creation import DataManipulation
from app.config import DbTables
from typing import List, Dict, Any, Optional
from enum import Enum
from datetime import datetime

class OrderRepository:
    def __init__(self):
        self.db = get_supabase_client()
        self.dataManipulator = DataManipulation()

    class DatabaseColName(Enum):
        ID = "id"
        CODICE = "codice"
        IDCLIENTE = "idCliente"
        IDAZIENDA = "idAzienda"
        DATA = "data"
        TOTALE = "totale"
        STATUS = "status"
        CREATED_AT = "created_at"

    def get_all_orders(self, status: Optional[str] = None, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """Recupera tutti gli ordini con filtri opzionali"""
        query = self.db.table(DbTables.ORDERS.value).select("*").order(self.DatabaseColName.CREATED_AT.value, desc=True)
        
        if status:
            query = query.eq(self.DatabaseColName.STATUS.value, status)
        
        response = query.range(offset, offset + limit - 1).execute()
        
        orders = response.data
        for o in orders:
            o["id_cliente"] = o.pop("idCliente", None)
            o["id_azienda"] = o.pop("idAzienda", None)
        
        return orders

    def get_order_by_id(self, order_id: int) -> Optional[Dict[str, Any]]:
        """Recupera un ordine per ID"""
        response = self.db.table(DbTables.ORDERS.value).select("*").eq(self.DatabaseColName.ID.value, order_id).execute()
        
        if response.data:
            order = response.data[0]
            order["id_cliente"] = order.pop("idCliente", None)
            order["id_azienda"] = order.pop("idAzienda", None)
            return order
        return None

    def get_order_by_code(self, codice: str) -> Optional[Dict[str, Any]]:
        """Recupera un ordine per codice"""
        response = self.db.table(DbTables.ORDERS.value).select("*").eq(self.DatabaseColName.CODICE.value, codice).execute()
        
        if response.data:
            order = response.data[0]
            order["id_cliente"] = order.pop("idCliente", None)
            order["id_azienda"] = order.pop("idAzienda", None)
            return order
        return None

    def get_orders_by_client(self, client_id: int, limit: int = 50) -> List[Dict[str, Any]]:
        """Recupera tutti gli ordini di un cliente"""
        response = self.db.table(DbTables.ORDERS.value).select("*").eq(self.DatabaseColName.IDCLIENTE.value, client_id).limit(limit).execute()
        
        orders = response.data
        for o in orders:
            o["id_cliente"] = o.pop("idCliente", None)
            o["id_azienda"] = o.pop("idAzienda", None)
        
        return orders

    def get_orders_by_company(self, company_id: int, limit: int = 100) -> List[Dict[str, Any]]:
        """Recupera tutti gli ordini di un'azienda"""
        response = self.db.table(DbTables.ORDERS.value).select("*").eq(self.DatabaseColName.IDAZIENDA.value, company_id).limit(limit).execute()
        
        orders = response.data
        for o in orders:
            o["id_cliente"] = o.pop("idCliente", None)
            o["id_azienda"] = o.pop("idAzienda", None)
        
        return orders

    def save_order(self, codice: str, id_cliente: int, id_azienda: int, data: str, status: str = "PENDING") -> Dict[str, Any]:
        """Salva un nuovo ordine"""
        order_data = {
            self.DatabaseColName.CODICE.value: codice,
            self.DatabaseColName.IDCLIENTE.value: id_cliente,
            self.DatabaseColName.IDAZIENDA.value: id_azienda,
            self.DatabaseColName.DATA.value: data,
            self.DatabaseColName.TOTALE.value: 0,
            self.DatabaseColName.STATUS.value: status
        }
        
        response = self.db.table(DbTables.ORDERS.value).insert(order_data).execute()
        
        if response.data:
            return response.data[0]
        return {}

    def update_order_status(self, order_id: int, status: str) -> bool:
        """Aggiorna lo stato di un ordine"""
        response = self.db.table(DbTables.ORDERS.value).update({
            self.DatabaseColName.STATUS.value: status
        }).eq(self.DatabaseColName.ID.value, order_id).execute()
        
        return len(response.data) > 0

    def update_order_total(self, order_id: int, total: float) -> bool:
        """Aggiorna il totale di un ordine"""
        response = self.db.table(DbTables.ORDERS.value).update({
            self.DatabaseColName.TOTALE.value: total
        }).eq(self.DatabaseColName.ID.value, order_id).execute()
        
        return len(response.data) > 0

    def get_order_stats(self, company_id: Optional[int] = None) -> Dict[str, Any]:
        """Restituisce statistiche sugli ordini"""
        query = self.db.table(DbTables.ORDERS.value).select("*")
        
        if company_id:
            query = query.eq(self.DatabaseColName.IDAZIENDA.value, company_id)
        
        response = query.execute()
        orders = response.data
        
        total_orders = len(orders)
        total_revenue = sum(o.get(self.DatabaseColName.TOTALE.value, 0) for o in orders)
        
        pending = len([o for o in orders if o.get(self.DatabaseColName.STATUS.value) == "PENDING"])
        processing = len([o for o in orders if o.get(self.DatabaseColName.STATUS.value) == "PROCESSING"])
        shipped = len([o for o in orders if o.get(self.DatabaseColName.STATUS.value) == "SHIPPED"])
        delivered = len([o for o in orders if o.get(self.DatabaseColName.STATUS.value) == "DELIVERED"])
        cancelled = len([o for o in orders if o.get(self.DatabaseColName.STATUS.value) == "CANCELLED"])
        
        return {
            "total": total_orders,
            "total_revenue": round(total_revenue, 2),
            "pending": pending,
            "processing": processing,
            "shipped": shipped,
            "delivered": delivered,
            "cancelled": cancelled
        }

    def get_sales_by_month(self, year: int = None, company_id: int = None) -> List[Dict[str, Any]]:
        """
        Restituisce vendite aggregate per mese tramite GROUP BY SQL
        """
        # Mappe mesi
        months_map = ['Gen', 'Feb', 'Mar', 'Apr', 'Mag', 'Giu', 'Lug', 'Ago', 'Set', 'Ott', 'Nov', 'Dic']
        
        # Query con Supabase RPC (funzione SQL personalizzata) o GROUP BY
        # Supabase non supporta GROUP BY diretto, quindi usiamo RPC
        
        # Opzione 1: Se hai una funzione SQL nel database
        try:
            response = self.db.rpc(
                "get_sales_by_month",
                {"p_year": year, "p_company_id": company_id}
            ).execute()
            if response.data:
                return response.data
        except:
            pass
        
        # Opzione 2: Fallback con GROUP BY via Python (ma mantenendo la logica)
        query = self.db.table(DbTables.ORDERS.value).select("data", "totale")
        
        if company_id:
            query = query.eq("idAzienda", company_id)
        
        response = query.execute()
        orders = response.data
        
        # Inizializza tutti i mesi con 0
        monthly_sales = {month: 0 for month in months_map}
        
        for order in orders:
            order_date = order.get("data")
            if order_date:
                # Estrai mese (supporta dd-mm-yyyy)
                if '-' in order_date:
                    parts = order_date.split('-')
                    if len(parts[0]) == 4:  # yyyy-mm-dd
                        month_num = int(parts[1])
                    else:  # dd-mm-yyyy
                        month_num = int(parts[1])
                else:
                    continue
                
                month_name = months_map[month_num - 1]
                monthly_sales[month_name] += order.get("totale", 0)
        
        # Restituisce tutti i mesi (anche quelli con 0)
        return [{"month": m, "sales": monthly_sales[m]} for m in months_map]