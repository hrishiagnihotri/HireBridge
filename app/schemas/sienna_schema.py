def user_info(item) -> dict:
    return{
        "id":str(item["_id"]),
        "sno":str(item["sno"]),
        "name":str(item["name"]),
        "email":str(item["email"]),
        "gender":str(item["gender"]),
        "usn":str(item["usn"]),
        "sem":item["sem"],
        "dept":str(item["department"]),
        "phone":item["phone"],
        "passout":item["passout"],
        "cgpa":item["cgpa"],
        "backlog":item["backlog"],
        "skills":item["skills"],
        "admin_remark":str(item["admin_remark"])
    }

def users(items) -> list :
    return [
        user_info(item) for item in items
    ]


def matchingparameters_sienna(item)->dict:
    return {
        "cgpa":item["cgpa"],
        "backlogs_exists" : int(item["backlog"]),
        "skills" : item["skills"],
        "batch" : item["passout"],
        "sem" : item["sem"],
        "department" : item["department"],
    }

def multisienna_parameters(items) -> list:
    return [
        matchingparameters_sienna(item) for item in items
    ]

def profilesienna_params(item) -> dict:
    return {
        "sno":item['sno'],
        "name":item['name'],
        "usn":item['usn'],
        "sem":item['sem'],
        "department":item['department'],
        "phone":item['phone'],
        "email":item['email'],
        "passout":item['passout'],
        "cgpa":item['cgpa'],
        "skills":item['skills'],
        "remark":item['admin_remark'],
        "messages":item.get('messages',[])
    }