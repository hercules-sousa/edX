import requests
res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "CMKLN6Azt2nlla5H4k4pQ", "isbns": "9781632168146"})
print(res.json())
