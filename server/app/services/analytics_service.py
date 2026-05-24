from app.database.product_repository import ProductRepository
from app.database.category_repository import CategoryRepository
from app.database.order_repository import OrderRepository
from app.database.client_repository import ClientRepository
from app.services.calendar_service import CalendarService
from datetime import datetime, timedelta
from typing import List, Dict, Any

class AnalyticsService:
    def __init__(self):
        self.prodRepo = ProductRepository()
        self.catRepo = CategoryRepository()
        self.orderRepo = OrderRepository()
        self.clientRepo = ClientRepository()
        self.calendar = CalendarService()

    def get_kpi(self, company_id: int = None) -> Dict[str, Any]:
        """Calcola KPI reali dai dati del database"""
        
        # Ottieni statistiche ordini
        stats = self.orderRepo.get_order_stats(company_id)
        
        # Calcola valore medio ordine
        total_revenue = stats.get("total_revenue", 0)
        total_orders = stats.get("total", 0)
        avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
        
        # Calcola rotazione stock (costo venduto / stock medio)
        products = self.prodRepo.get_all_product()
        if products:
            total_stock_value = sum(p.get("stock", 0) * p.get("prezzo", 0) for p in products)
            stock_turnover = total_revenue / total_stock_value if total_stock_value > 0 else 0
        else:
            stock_turnover = 0
        
        # Calcola crescita rispetto al mese precedente
        current_month = datetime.now().month
        current_year = datetime.now().year
        
        # Ordini del mese corrente
        orders_current = self.orderRepo.get_all_orders()
        orders_current = [o for o in orders_current if self._get_month_from_date(o.get("data")) == current_month]
        revenue_current = sum(o.get("totale", 0) for o in orders_current)
        
        # Ordini del mese precedente
        prev_month = current_month - 1 if current_month > 1 else 12
        prev_year = current_year if current_month > 1 else current_year - 1
        orders_prev = [o for o in orders_current if self._get_month_from_date(o.get("data")) == prev_month]
        revenue_prev = sum(o.get("totale", 0) for o in orders_prev)
        
        revenue_growth = ((revenue_current - revenue_prev) / revenue_prev * 100) if revenue_prev > 0 else 0
        
        return {
            "total_revenue": round(total_revenue, 2),
            "total_orders": total_orders,
            "avg_order_value": round(avg_order_value, 2),
            "stock_turnover": round(stock_turnover, 2),
            "revenue_growth": round(revenue_growth, 1)
        }
    
    def get_sales_trend(self, period: str = "year", company_id: int = None) -> List[Dict[str, Any]]:
        """Restituisce trend vendite reali"""
        orders = self.orderRepo.get_all_orders()
        
        if company_id:
            orders = [o for o in orders if o.get("idAzienda") == company_id]
        
        if period == "month":
            # Ultimi 30 giorni
            result = []
            for i in range(30, 0, -1):
                date = (datetime.now() - timedelta(days=i)).strftime("%d/%m")
                daily_orders = [o for o in orders if o.get("data") == date]
                daily_sales = sum(o.get("totale", 0) for o in daily_orders)
                result.append({"date": date, "sales": daily_sales})
            return result
        
        elif period == "quarter":
            # Ultimi 3 mesi per settimana
            months = ['Gen', 'Feb', 'Mar', 'Apr', 'Mag', 'Giu', 'Lug', 'Ago', 'Set', 'Ott', 'Nov', 'Dic']
            current_month_idx = datetime.now().month - 1
            result = []
            for i in range(3):
                month_idx = (current_month_idx - i) % 12
                month_name = months[month_idx]
                month_orders = [o for o in orders if self._get_month_from_date(o.get("data")) == month_idx + 1]
                month_sales = sum(o.get("totale", 0) for o in month_orders)
                result.append({"month": month_name, "sales": month_sales})
            return result[::-1]  # In ordine cronologico
        
        else:  # year
            months = ['Gen', 'Feb', 'Mar', 'Apr', 'Mag', 'Giu', 'Lug', 'Ago', 'Set', 'Ott', 'Nov', 'Dic']
            result = []
            for month_idx in range(12):
                month_name = months[month_idx]
                month_orders = [o for o in orders if self._get_month_from_date(o.get("data")) == month_idx + 1]
                month_sales = sum(o.get("totale", 0) for o in month_orders)
                result.append({"month": month_name, "sales": month_sales})
            return result
    
    def get_category_distribution(self, company_id: int = None) -> List[Dict[str, Any]]:
        """Distribuzione vendite per categoria (reale)"""
        orders = self.orderRepo.get_all_orders()
        
        if company_id:
            orders = [o for o in orders if o.get("idAzienda") == company_id]
        
        # Raggruppa per categoria
        categories = {}
        
        for order in orders:
            # Ottieni dettagli ordine (dovresti avere un metodo per farlo)
            # Per ora usiamo un approccio semplificato
            cat_id = order.get("idCategoria")
            if cat_id:
                cat_name = self.catRepo.get_desc_by_id(cat_id) or "Altro"
                categories[cat_name] = categories.get(cat_name, 0) + order.get("totale", 0)
        
        if not categories:
            # Fallback: distribuzione basata sui prodotti disponibili
            products = self.prodRepo.get_all_product()
            for p in products:
                cat_id = p.get("idCategoria")
                cat_name = self.catRepo.get_desc_by_id(cat_id) or "Altro"
                price = p.get("prezzo", 0) * p.get("stock", 0)
                categories[cat_name] = categories.get(cat_name, 0) + price
        
        total = sum(categories.values())
        if total == 0:
            return []
        
        return [{"name": k, "value": v, "percentage": round(v/total*100, 1)} for k, v in categories.items()]
    
    def get_top_products(self, limit: int = 5, company_id: int = None) -> List[Dict[str, Any]]:
        """Top prodotti per vendite (reali)"""
        orders = self.orderRepo.get_all_orders()
        
        if company_id:
            orders = [o for o in orders if o.get("idAzienda") == company_id]
        
        # Raggruppa vendite per prodotto
        product_sales = {}
        
        for order in orders:
            # Qui dovresti aggregare dai dettagli ordine
            # Versione semplificata:
            product_id = order.get("idProdotto")
            if product_id:
                product_sales[product_id] = product_sales.get(product_id, 0) + order.get("totale", 0)
        
        # Ordina per vendite
        sorted_products = sorted(product_sales.items(), key=lambda x: x[1], reverse=True)[:limit]
        
        result = []
        for product_id, sales in sorted_products:
            product = self.prodRepo.get_product_by_id(product_id)
            if product:
                # Calcola crescita (rispetto al periodo precedente)
                growth = 0  # TODO: calcola crescita reale
                result.append({
                    "id": product_id,
                    "name": product.get("nome", "Sconosciuto"),
                    "sales": round(sales, 2),
                    "growth": growth,
                    "stock": product.get("stock", 0)
                })
        
        return result
    
    def get_critical_stock(self, threshold: int = 5, company_id: int = None) -> List[Dict[str, Any]]:
        """Prodotti con stock critico (dato reale)"""
        products = self.prodRepo.get_all_product()
        
        if company_id:
            products = [p for p in products if p.get("idAzienda") == company_id]
        
        critical = [p for p in products if p.get("stock", 0) <= threshold]
        
        # Calcola giorni stimati all'esaurimento
        result = []
        for p in critical:
            # Calcola vendite medie giornaliere da ordini recenti
            # Versione semplificata
            days_until_out = p.get("stock", 1)  # TODO: calcola da vendite medie
            
            result.append({
                "id": p.get("id"),
                "name": p.get("nome"),
                "stock": p.get("stock", 0),
                "threshold": threshold,
                "days_until_out": max(1, days_until_out)
            })
        
        return result
    
    def get_recent_activities(self, limit: int = 10, company_id: int = None) -> List[Dict[str, Any]]:
        """Attività recenti (ordini, stock critico, ecc.)"""
        activities = []
        
        # Ordini recenti
        orders = self.orderRepo.get_all_orders()
        if company_id:
            orders = [o for o in orders if o.get("idAzienda") == company_id]
        
        orders = sorted(orders, key=lambda x: x.get("data", ""), reverse=True)[:5]
        for order in orders:
            activities.append({
                "id": order.get("id"),
                "type": "order",
                "message": f"Nuovo ordine #{order.get('codice')} - €{order.get('totale', 0)}",
                "time": order.get("data", ""),
                "status": order.get("status", "PENDING")
            })
        
        # Stock critico
        critical = self.get_critical_stock(5, company_id)
        for prod in critical[:3]:
            activities.append({
                "id": prod.get("id"),
                "type": "stock",
                "message": f"Stock critico: {prod.get('name')} (solo {prod.get('stock')} rimasti)",
                "time": datetime.now().strftime("%Y-%m-%d"),
                "status": "warning"
            })
        
        return activities[:limit]
    
    def _get_month_from_date(self, date_str: str) -> int:
        """Estrae il mese da una stringa data"""
        if not date_str:
            return datetime.now().month
        try:
            # Supporta formato "dd-mm-yyyy"
            parts = date_str.split("-")
            if len(parts) == 3:
                return int(parts[1])
            # Supporta formato "yyyy-mm-dd"
            parts = date_str.split("-")
            if len(parts) == 3 and len(parts[0]) == 4:
                return int(parts[1])
        except:
            pass
        return datetime.now().month