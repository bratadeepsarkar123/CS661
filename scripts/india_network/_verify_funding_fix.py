import json
from pathlib import Path
data = json.loads(Path("dashboard/data/india_network/2024_full.json").read_text(encoding="utf-8"))
tests = [
 ("IISc", "Indian Institute of Science", 197.08, 534.77),
 ("BHU", "Indian Institute of Technology (BHU) Varanasi", 35.37, 206.94),
 ("Dhanbad", "Indian Institute of Technology (ISM) Dhanbad", 12.24, 30.54),
]
for label, name, bad, good in tests:
 for n in data["nodes"]:
  if n["name"]==name:
   amt = n.get("research_funding_cr")
   status = "PASS" if amt != bad else "FAIL"
   print(label, amt, status)
