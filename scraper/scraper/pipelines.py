from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from scraper.items import ScraperItem, LeadsItem
from db import DB_PATH
import sqlite3


class LeadsPipeline:
    
    def open_spider(self):
       self.conn = sqlite3.connect(DB_PATH)
       
    def close_spider(self):
        self.conn.close()
        
    
    def process_item(self, item):
        if not isinstance(item, LeadsItem): return item
        cursor = self.conn.cursor()
        if item.get("vendor") is None:
            raise DropItem("No vendor found.")
        else:
            cursor.execute("SELECT id FROM leads WHERE url=?",(item.get("url"),))
            result = cursor.fetchone()
            if result:
                raise DropItem("Duplicate url found.")
            else:
                cursor.execute("INSERT INTO leads (organiser_id,url,vendor,status) VALUES ( ?,?,?,? );",
                            (item.get("organiser_id"), item.get("url"), item.get("vendor"), item.get("status")))
            self.conn.commit()
        
        
class EventsPipeline:
    
    def open_spider(self):
        self.conn = sqlite3.connect(DB_PATH)
    
    def close_spider(self):
         self.conn.close()
    
    def process_item(self, item):
        if not isinstance(item, ScraperItem): return item
        cursor = self.conn.cursor()
        
        cursor.execute("UPDATE leads SET status='scraped' WHERE url=?", (item.get("lead_url"),))
        print(f"Mylene DEBUG: lead_url = {item.get('lead_url')}")
        print(f"mylene DEBUG: rows updated = {cursor.rowcount}")
        self.conn.commit()
        
        cursor.execute("SELECT id FROM events WHERE url=?",(item.get("url"),))
        result = cursor.fetchone()
        if result:
            return item
        else:
            cursor.execute(
                                "INSERT INTO events (title, location, starts_at, ends_at, categories, price_from, url, organiser_id) VALUES (?,?,?,?,?,?,?,?)",
                                (
                                    item.get("title"),
                                    item.get("location"),
                                    item.get("starts_at"),
                                    item.get("ends_at"),
                                    item.get("categories"),
                                    item.get("price_from"),
                                    item.get("url"),
                                    item.get("organiser_id")
                                )
                            )
        