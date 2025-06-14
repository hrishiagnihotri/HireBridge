def job_info(item)->dict:
    return{
        "id":str(item["_id"]),
        "company":item["company"],
        "role":str(item["role"]),
        "cgpa_operator":str(item["cgpa_operator"]),
        "cgpa_value":str(item["cgpa_value"]),
        "backlog_allowed":str(item["Backlogs"]),
        "batch":item["batch"],
        "department_req":item["department"],
        # "skills":item["skills"],
        "skills":[item.strip() for item in item["skills"].split(sep=',')],
        "sem_completed":item["sems"],
        "apply_by":str(item["apply_by"])[:10],
        "apply_link":item["apply_link"],
        "description":item["description"],
        "posted_by":item["posted_by"],
        "posted_on":item["posted_on"],
    }

def alljobs(items):
    return [job_info(item) for item in items]
