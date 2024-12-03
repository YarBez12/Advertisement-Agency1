from Models import Client, Campaign, Advertisement


def load_clients_from_db(db_manager, clients_collection):
    query = """
        SELECT company_name, phone, email, address, type, business_area, available_budget
        FROM Clients;
    """
    _, rows = db_manager.fetch_data(query)
    for row in rows:
        client = Client(
            company_name=row[0],
            phone=row[1],
            email=row[2],
            address=row[3],
            type=row[4],
            business_area=row[5],
            available_budget=row[6]
        )
        clients_collection.add(client)

def load_campaigns_from_db(db_manager, campaign_collection):
    query = """
        SELECT campaign_id, name, start_date, end_date, goal, budget, company_name
        FROM Campaigns;
    """
    _, rows = db_manager.fetch_data(query)
    for row in rows:
        campaign = Campaign(
            campaign_id=row[0],
            name=row[1],
            start_date=row[2],
            end_date=row[3],
            goal=row[4],
            budget=row[5],
            company_name=row[6],
        )
        campaign_collection.add(campaign)

def load_advertisements_from_db(db_manager, advertisement_collection):
    query = """
        SELECT advertisement_id, format, topic, text, send_time, language, 
               attachment, clicks, views, campaign_id, platform_id
        FROM Advertisements;
    """
    _, rows = db_manager.fetch_data(query)
    for row in rows:
        advertisement = Advertisement(
            advertisement_id=row[0],
            format=row[1],
            topic=row[2],
            text=row[3],
            send_time=row[4],
            language=row[5],
            attachment=row[6],
            clicks=row[7],
            views=row[8],
            campaign_id=row[9],
            platform_id=row[10],
        )
        advertisement_collection.add(advertisement)




