import random
import threading
import time
from datetime import datetime, timedelta
from app.database.database_connection import get_supabase_client
from app.services.calendar_service import CalendarService
from app.services.logger_service import LoggerService
from app.config import LogFile, DbTables
from app.utils.utility_generator import generate_password, generate_card
import requests

class SimulationService:
    def __init__(self):
        self.db = get_supabase_client()
        self.calendar = CalendarService()
        self.logger = LoggerService()
        self.tables = DbTables  # Riferimento all'enum
        self.filename = LogFile.SIMULATION.value if hasattr(LogFile, 'SIMULATION') else "simulation.log"
        self._running = False
        self._thread = None
        self._interval_seconds = 600  # Intervallo tra cicli di simulazione
    
    def start_simulation(self):
        """Avvia il thread di simulazione"""
        if self._running:
            self.logger.warning(self.filename, "Simulazione già in esecuzione")
            return False
        
        self._running = True
        self._thread = threading.Thread(target=self._simulation_loop, daemon=True)
        self._thread.start()
        
        # Aggiorna stato nel database
        self._update_simulation_state(True)
        
        self.logger.info(self.filename, "Simulazione avviata")
        return True
    
    def stop_simulation(self):
        """Ferma il thread di simulazione"""
        self._running = False
        if self._thread:
            self._thread.join(timeout=5)
        
        # Aggiorna stato nel database
        self._update_simulation_state(False)
        
        self.logger.info(self.filename, "Simulazione fermata")
        return True
    
    def _update_simulation_state(self, active: bool):
        """Aggiorna lo stato della simulazione nel DB"""
        try:
            self.db.table(self.tables.SIMULATION_STATE.value).update({
                "attiva": active,
                "ultimo_aggiornamento": datetime.now().isoformat()
            }).eq("id", 1).execute()
        except Exception as e:
            self.logger.error(self.filename, f"Errore aggiornamento stato: {e}")
    
    def _simulation_loop(self):
        """Loop principale della simulazione"""
        while self._running:
            try:
                # 1. Genera ordini casuali
                orders_generated = self._generate_random_orders()
                
                # 2. Aggiorna stock in base agli ordini
                stock_updates = self._update_stock_from_orders()
                
                # 3. Genera nuovi clienti casuali (ogni 5 cicli)
                #if random.randint(1, 5) == 1:
                 #   clients_generated = self._generate_random_clients()
                
                # 4. Rifornimento automatico per stock basso
                restocks = self._auto_restock()
                
                # 5. Aggiorna statistiche
                self._update_simulation_stats(orders_generated, stock_updates)
                
                self.logger.debug(self.filename, f"Ciclo simulazione completato: {orders_generated} ordini, {stock_updates} movimenti stock")
                
            except Exception as e:
                self.logger.error(self.filename, f"Errore nel ciclo di simulazione: {e}")
            
            # Attendi il prossimo ciclo
            time.sleep(self._interval_seconds)
    
    def _generate_random_orders(self, max_orders: int = 10) -> int:
        """Genera ordini casuali"""
        try:
            # Ottieni prodotti esistenti
            products = self.db.table(self.tables.PRODUCTS.value).select("id", "prezzo", "stock").execute()
            products = products.data
            
            if not products:
                self.logger.warning(self.filename, "Nessun prodotto trovato. Esegui seed data.")
                return 0
            
            # Ottieni clienti esistenti
            clients = self.db.table(self.tables.CLIENTS.value).select("id").execute()
            clients = clients.data
            
            # Se non ci sono clienti, creane uno di default
            if not clients:
                self.logger.info(self.filename, "Nessun cliente trovato, ne creo uno di default")
                default_client = {
                    "nome": "Demo",
                    "cognome": "User",
                    "email": "demo@inventrack.com",
                    "password": generate_password(),
                    "dataNascita": "1990-01-01",
                    "tessera": False,
                    "codGenere": "M",
                    "indirizzo": "Via Roma 1",
                    "numeroCivico": "1",
                    "dataReg": self.calendar.change_style_calendar(self.calendar.get_date())
                }
                client_result = self.db.table(self.tables.CLIENTS.value).insert(default_client).execute()
                if client_result.data:
                    clients = [{"id": client_result.data[0]["id"]}]
                else:
                    return 0
            
            orders_generated = 0
            num_orders = random.randint(1, max_orders)
            
            for _ in range(num_orders):
                # Seleziona cliente casuale
                client = random.choice(clients)
                
                # Seleziona 1-3 prodotti per ordine
                num_items = random.randint(1, 3)
                selected_products = random.sample(products, min(num_items, len(products)))
                
                total = 0
                order_items = []
                
                for product in selected_products:
                    quantity = random.randint(1, 5)
                    subtotal = quantity * product["prezzo"]
                    total += subtotal
                    order_items.append({
                        "idprodotto": product["id"],
                        "quantita": quantity,
                        "prezzo_unitario": product["prezzo"],
                        "subtotale": subtotal
                    })
                
                # Crea ordine
                order_code = f"ORD-{datetime.now().strftime('%Y%m%d%H%M%S')}-{random.randint(1000, 9999)}"
                
                order_data = {
                    "codice": order_code,
                    "idCliente": client["id"],
                    "idAzienda": 1,  # TODO: gestire multi-azienda
                    "data": self.calendar.change_style_calendar(self.calendar.get_date()),
                    "totale": total,
                    "status": random.choice(["PENDING", "PROCESSING"])
                }
                
                order_result = self.db.table(self.tables.ORDERS.value).insert(order_data).execute()
                
                if order_result.data:
                    order_id = order_result.data[0]["id"]
                    
                    # Aggiungi dettagli ordine
                    for item in order_items:
                        item["idordine"] = order_id
                        self.db.table(self.tables.ORDER_DETAILS.value).insert(item).execute()
                    
                    orders_generated += 1
                    
                    # Registra movimento magazzino (uscita)
                    for item in order_items:
                        self.db.table(self.tables.MOVEMENTS.value).insert({
                            "idprodotto": item["idprodotto"],
                            "tipo": "uscita",
                            "quantita": item["quantita"],
                            "data": self.calendar.change_style_calendar(self.calendar.get_date()),
                            "note": f"Ordine {order_code}"
                        }).execute()
            
            return orders_generated
            
        except Exception as e:
            self.logger.error(self.filename, f"Errore generazione ordini: {e}")
            return 0
    
    def _update_stock_from_orders(self) -> int:
        """Aggiorna lo stock in base agli ordini pendenti"""
        try:
            # Ottieni ordini in stato PENDING
            orders = self.db.table(self.tables.ORDERS.value).select("id", "codice").eq("status", "PENDING").execute()
            orders = orders.data
            
            updates = 0
            for order in orders:
                # Ottieni dettagli ordine
                details = self.db.table(self.tables.ORDER_DETAILS.value).select("idprodotto", "quantita").eq("idordine", order["id"]).execute()
                
                for detail in details.data:
                    # Riduci stock usando la funzione SQL
                    product_id = detail["idprodotto"]
                    quantity = detail["quantita"]
                    
                    self.db.rpc("decrement_stock", {"p_id": product_id, "p_qty": quantity}).execute()
                    updates += 1
                
                # Aggiorna stato ordine a PROCESSING
                self.db.table(self.tables.ORDERS.value).update({"status": "PROCESSING"}).eq("id", order["id"]).execute()
            
            return updates
            
        except Exception as e:
            self.logger.error(self.filename, f"Errore aggiornamento stock: {e}")
            return 0
    
    def _generate_random_clients(self, max_clients: int = 3) -> int:
        """Genera clienti casuali tramite API RandomUser"""
        try:
            url = f"https://randomuser.me/api/?nat=us&inc=gender,name,location,email,dob&results={max_clients}"
            response = requests.get(url)
            
            if response.status_code != 200:
                return 0
            
            data = response.json()
            current_date = self.calendar.get_date()
            clients_generated = 0
            
            for result in data["results"]:
                # Estrai dati
                gender = result["gender"]
                name = result["name"]["first"]
                surname = result["name"]["last"]
                email = result["email"]
                dob = result["dob"]["date"].split("T")[0]
                
                # Genera password casuale
                password = generate_password()
                
                # Inserisci cliente
                client_data = {
                    "nome": name,
                    "cognome": surname,
                    "email": email,
                    "password": password,
                    "dataNascita": dob,
                    "tessera": generate_card(),
                    "codGenere": "M" if gender == "male" else "F",
                    "indirizzo": result["location"]["street"]["name"],
                    "numeroCivico": str(result["location"]["street"]["number"]),
                    "dataReg": current_date
                }
                
                self.db.table(self.tables.CLIENTS.value).insert(client_data).execute()
                clients_generated += 1
            
            return clients_generated
            
        except Exception as e:
            self.logger.error(self.filename, f"Errore generazione clienti: {e}")
            return 0
    
    def _auto_restock(self) -> int:
        """Rifornimento automatico per prodotti con stock basso"""
        try:
            # Ottieni prodotti con stock < stock_minimo
            products = self.db.table(self.tables.PRODUCTS.value).select("id", "nome", "stock", "stock_minimo", "stock_ottimale", "prezzo").execute()
            products = products.data
            
            restocks = 0
            
            for product in products:
                if product["stock"] < product["stock_minimo"]:
                    # Calcola quantità da riordinare
                    reorder_qty = product["stock_ottimale"] - product["stock"]
                    reorder_qty = max(reorder_qty, product["stock_minimo"] * 2)
                    
                    # Aggiorna stock
                    self.db.table(self.tables.PRODUCTS.value).update({
                        "stock": product["stock"] + reorder_qty
                    }).eq("id", product["id"]).execute()
                    
                    # Registra movimento magazzino (entrata)
                    self.db.table(self.tables.MOVEMENTS.value).insert({
                        "idprodotto": product["id"],
                        "tipo": "entrata",
                        "quantita": reorder_qty,
                        "prezzo_unitario": product["prezzo"],
                        "data": self.calendar.change_style_calendar(self.calendar.get_date()),
                        "note": f"Riordino automatico (stock basso: {product['stock']} < {product['stock_minimo']})"
                    }).execute()
                    
                    restocks += 1
                    
                    self.logger.info(self.filename, f"Riordino automatico: {product['nome']} +{reorder_qty} unità")
            
            return restocks
            
        except Exception as e:
            self.logger.error(self.filename, f"Errore riordino automatico: {e}")
            return 0
    
    def _update_simulation_stats(self, orders: int, stock_updates: int):
        """Aggiorna le statistiche della simulazione"""
        try:
            # Ottieni stato corrente
            state = self.db.table(self.tables.SIMULATION_STATE.value).select("*").eq("id", 1).execute()
            
            if state.data:
                current = state.data[0]
                self.db.table(self.tables.SIMULATION_STATE.value).update({
                    "ordini_generati": current.get("ordini_generati", 0) + orders,
                    "movimenti_stock": current.get("movimenti_stock", 0) + stock_updates,
                    "ultimo_aggiornamento": datetime.now().isoformat()
                }).eq("id", 1).execute()
        except Exception as e:
            self.logger.error(self.filename, f"Errore aggiornamento statistiche: {e}")
    
    def get_simulation_stats(self) -> dict:
        """Restituisce le statistiche correnti della simulazione"""
        try:
            state = self.db.table(self.tables.SIMULATION_STATE.value).select("*").eq("id", 1).execute()
            products = self.db.table(self.tables.PRODUCTS.value).select("stock").execute()
            
            total_stock = sum(p.get("stock", 0) for p in products.data)
            
            if state.data:
                return {
                    "attiva": state.data[0].get("attiva", False),
                    "ultimo_aggiornamento": state.data[0].get("ultimo_aggiornamento"),
                    "ordini_generati": state.data[0].get("ordini_generati", 0),
                    "clienti_generati": state.data[0].get("clienti_generati", 0),
                    "movimenti_stock": state.data[0].get("movimenti_stock", 0),
                    "total_stock": total_stock
                }
            return {}
        except Exception as e:
            self.logger.error(self.filename, f"Errore recupero statistiche: {e}")
            return {}
    
    def reset_simulation(self) -> dict:
        """Resetta la simulazione (cancella ordini e resetta stock)"""
        try:
            # Cancella dettagli ordini
            self.db.table(self.tables.ORDER_DETAILS.value).delete().neq("id", 0).execute()
            
            # Cancella ordini
            self.db.table(self.tables.ORDERS.value).delete().neq("id", 0).execute()
            
            # Cancella movimenti magazzino
            self.db.table(self.tables.MOVEMENTS.value).delete().neq("id", 0).execute()
            
            # Resetta stock prodotti a valori casuali
            products = self.db.table(self.tables.PRODUCTS.value).select("id").execute()
            for product in products.data:
                random_stock = random.randint(10, 100)
                self.db.table(self.tables.PRODUCTS.value).update({"stock": random_stock}).eq("id", product["id"]).execute()
            
            # Resetta statistiche
            self.db.table(self.tables.SIMULATION_STATE.value).update({
                "ordini_generati": 0,
                "clienti_generati": 0,
                "movimenti_stock": 0,
                "ultimo_aggiornamento": datetime.now().isoformat()
            }).eq("id", 1).execute()
            
            self.logger.info(self.filename, "Simulazione resettata")
            
            return {"message": "Simulazione resettata con successo"}
            
        except Exception as e:
            self.logger.error(self.filename, f"Errore reset simulazione: {e}")
            return {"error": str(e)}