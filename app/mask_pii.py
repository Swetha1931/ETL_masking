import hashlib  
from datetime import datetime  

# Define a function to mask PII (Personally Identifiable Information) data
def mask_pii_data(data):
    
    try:
        masked_data = {}      
        masked_data["user_id"] = data["user_id"]
        masked_data["device_type"] = data["device_type"]
        masked_data["masked_ip"] = hashlib.sha256(data["ip"].encode("utf-8")).hexdigest()
        masked_data["masked_device_id"] = hashlib.sha256(data["device_id"].encode("utf-8")).hexdigest()
        masked_data["locale"] = data.get("locale", "unknown")
        masked_data["app_version"] = int(data["app_version"].replace(".", ""))
        masked_data["create_date"] = datetime.now().isoformat()
        return masked_data

    except KeyError as e:
        print(f"Error masking PII data: {e}")
        return {}  # Return an empty dictionary if there's an error