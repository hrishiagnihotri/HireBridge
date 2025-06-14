def get_admin_info(item):
    return {
        "id":str(item["_id"]),
        "name":str(item["name"]),
        "dept":str(item["department"]),
        "phone":item["phone"],
    }

def admins(items) -> list :
    return [
        get_admin_info(item) for item in items
    ]