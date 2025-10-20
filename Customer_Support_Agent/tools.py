
## Tools dictionary
from Tools import Search_kb, Query_db, Ticket, Email
tools = {
    "KnowledgeBase": Search_kb.search_kb,
    "Database": Query_db.query_db,
    "TicketingSystem": Ticket.create_ticket,
    "Email": Email.send_email
}

