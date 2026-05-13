#!/usr/bin/env python3
"""
Veelearn Server Keep-Alive Script
Run this on your Alienware M17 R1 to keep the server awake
"""

import requests
import time
import schedule
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('keep-alive.log'),
        logging.StreamHandler()
    ]
)

# Veelearn API endpoint
VEELEARN_API = "https://api.veelearn.org/api/health"

def ping_server():
    """Ping Veelearn server to keep it awake"""
    try:
        response = requests.get(VEELEARN_API, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            logging.info(f"✅ Server awake: {data.get('status', 'unknown')} - Uptime: {data.get('uptime', 'unknown')}s")
            return True
        else:
            logging.warning(f"⚠️ Server responded with HTTP {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        logging.error("❌ Ping timeout (server might be starting up)")
        return False
    except requests.exceptions.ConnectionError:
        logging.error("❌ Connection error (server might be down)")
        return False
    except Exception as e:
        logging.error(f"❌ Unexpected error: {e}")
        return False

def main():
    """Main keep-alive loop"""
    logging.info("🚀 Veelearn Keep-Alive Script Started")
    logging.info(f"🌐 Target: {VEELEARN_API}")
    logging.info("⏰ Pinging every 10 minutes")
    logging.info("🔧 Press Ctrl+C to stop")
    
    # Schedule every 10 minutes
    schedule.every(10).minutes.do(ping_server)
    
    # Initial ping
    ping_server()
    
    # Main loop
    try:
        while True:
            schedule.run_pending()
            time.sleep(30)  # Check every 30 seconds
            
    except KeyboardInterrupt:
        logging.info("⏹️ Keep-alive script stopped by user")
    except Exception as e:
        logging.error(f"💥 Script crashed: {e}")
        raise

if __name__ == "__main__":
    main()
