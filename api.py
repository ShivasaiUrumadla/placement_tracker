# import requests

# def home():
#     url = "https://codeforces.com/api/problemset.problems"

#     response = requests.get(url)
#     data = response.json()

#     array_problems = []

#     if data["status"] == "OK":
#         problems = data["result"]["problems"]

#         for p in problems:
#             if "array" in p.get("tags", []):
#                 array_problems.append({
#                     "name": p["name"],
#                     "rating": p.get("rating", "N/A"),
#                     "link": f"https://codeforces.com/problemset/problem/{p['contestId']}/{p['index']}"
#                 })
#     return array_problems
    
# problems=home()

# print("Total length of array problems:",len(problems))





import requests

def get_array_problems():
    url = "https://codeforces.com/api/problemset.problems"

    response = requests.get(url)
    data = response.json()

    array_problems = []

    if data["status"] == "OK":
        problems = data["result"]["problems"]

        for p in problems:
            if "implementation" in p.get("tags", []):
                array_problems.append({
                    "name": p["name"],
                    "rating": p.get("rating", "N/A"),
                    "link": f"https://codeforces.com/problemset/problem/{p['contestId']}/{p['index']}"
                })

        

    print(data["status"])
    return array_problems

# 🔽 Run directly
problems = get_array_problems()

print("Total Array Problems:", len(problems))
print("\nFirst 10 Problems:\n")

for p in problems[:1]:
    print(f"Name   : {p['name']}")
    print(f"Rating : {p['rating']}")
    print(f"Link   : {p['link']}")
    print("-" * 40)
