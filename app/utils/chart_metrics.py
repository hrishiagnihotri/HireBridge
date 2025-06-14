from config import conn3

resp = conn3.aggregate([
  { '$unwind': "$skills" },
  { '$group': { '_id': "$skills", 'count': { '$sum': 1 } } },
  { '$sort': { 'count': -1 } },
  { '$limit': 3 }
])
print(resp)