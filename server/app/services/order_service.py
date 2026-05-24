from app.database.order_repository import OrderRepository
from app.database.order_detail_repository import OrderDetailRepository
from app.database.product_repository import ProductRepository
from app.services.calendar_service import CalendarService
from typing import List, Dict, Any, Optional
from datetime import datetime

class OrderService:
    def __init__(self):
        self.orderRepo = OrderRepository()
        self.detailRepo = OrderDetailRepository()
        self.productRepo = ProductRepository()
        self.calendar = CalendarService()

    def get_all_orders(self, status: Optional[str] = None, limit: int = 365, offset: int = 0) -> List[Dict[str, Any]]:
        """Recupera tutti gli ordini"""
        return self.orderRepo.get_all_orders(status, limit, offset)

    def get_order_by_id(self, order_id: int) -> Optional[Dict[str, Any]]:
        """Recupera un ordine per ID"""
        order = self.orderRepo.get_order_by_id(order_id)
        if order:
            details = self.detailRepo.get_details_by_order(order_id)
            order["details"] = details
        return order

    def get_order_by_code(self, codice: str) -> Optional[Dict[str, Any]]:
        """Recupera un ordine per codice"""
        return self.orderRepo.get_order_by_code(codice)

    def get_orders_by_client(self, client_id: int) -> List[Dict[str, Any]]:
        """Recupera tutti gli ordini di un cliente"""
        return self.orderRepo.get_orders_by_client(client_id)

    def create_order(self, id_cliente: int, id_azienda: int, items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Crea un nuovo ordine con i suoi prodotti"""
        current_date = self.calendar.get_date()
        
        # Genera codice univoco
        codice = f"ORD-{datetime.now().strftime('%Y%m%d%H%M%S')}-{id_cliente}"
        
        # Crea l'ordine
        order = self.orderRepo.save_order(codice, id_cliente, id_azienda, current_date)
        
        if not order:
            return {}
        
        order_id = order.get("id")
        
        # Aggiungi i prodotti
        for item in items:
            product = self.productRepo.get_product_by_id(item["id_prodotto"])
            if product:
                self.detailRepo.add_detail(
                    order_id,
                    item["id_prodotto"],
                    item["quantita"],
                    product.get("prezzo", 0)
                )
        
        # Recupera l'ordine completo
        return self.get_order_by_id(order_id)

    def update_order_status(self, order_id: int, status: str) -> bool:
        """Aggiorna lo stato di un ordine"""
        valid_statuses = ["PENDING", "PROCESSING", "SHIPPED", "DELIVERED", "CANCELLED"]
        if status not in valid_statuses:
            return False
        return self.orderRepo.update_order_status(order_id, status)

    def get_order_stats(self, company_id: Optional[int] = None) -> Dict[str, Any]:
        """Restituisce statistiche sugli ordini"""
        return self.orderRepo.get_order_stats(company_id)

    def get_recent_orders(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Ordini recenti"""
        orders = self.orderRepo.get_all_orders()
        orders = sorted(orders, key=lambda x: x.get("data", ""), reverse=True)[:limit]
        return orders

    def get_orders_by_status(self, status: str) -> List[Dict[str, Any]]:
        """Ordini filtrati per stato"""
        return self.orderRepo.get_all_orders(status=status)

    def cancel_order(self, order_id: int) -> bool:
        """Annulla un ordine"""
        return self.update_order_status(order_id, "CANCELLED")

    def get_order_summary(self, order_id: int) -> Dict[str, Any]:
        """Riepilogo completo ordine con dettagli"""
        order = self.get_order_by_id(order_id)
        if order:
            details = self.detailRepo.get_details_by_order(order_id)
            order["details"] = details
            order["total_items"] = sum(d.get("quantita", 0) for d in details)
        return order