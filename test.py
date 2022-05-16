import re

with open('upload/test.txt') as file:
    text = file.read()

# person = [r"[А-Я].{3,10} \w\.\w\.", r"\w\.\w\. \w{3,10}"]
# for per in person:
#     print(re.findall(per, text))

person = [r"[А-Я].{3,10} \w\.\w\.", r"\w\.\w\. \w{3,10}", r"\+\d{11}", r"8\d{10}", r"8-\d{3}-\d{3}-\d{2}-\d{2}", r"\+7\(\d{3}\)\d{7}",
          r"\+7 \(\d{3}\) \d{3}-\d{2}-\d{2}"]
number = []
sums = person.append(number)
for sum in sums:
    line = re.findall(sum, text)[0]