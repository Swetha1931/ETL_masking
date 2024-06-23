import psycopg2  
from psycopg2.extras import execute_values  


# Function to insert records into PostgreSQL
def insert_to_postgres(connection_params, records):
    
    # INSERT query with placeholders for the record values
    insert_query = """
    INSERT INTO user_logins (
        user_id,
        device_type,
        masked_ip,
        masked_device_id,
        locale,
        app_version,
        create_date
    ) VALUES %s;
    """

    # Establish a connection to the PostgreSQL database
    with psycopg2.connect(**connection_params) as conn:
        with conn.cursor() as cur:
            # Use execute_values to bulk insert the records into the user_logins table
            execute_values(cur, insert_query, [(record.user_id, record.device_type, record.masked_ip,
                                               record.masked_device_id, record.locale, record.app_version, record.create_date)
                                              for record in records])
        conn.commit()