import re
text = "89245780005"
sums = [r"[А-Я].{3,10} \w\.\w\.", r"\w\.\w\. \w{3,10}", r"\+\d{11}", r"8\d{10}", r"8-\d{3}-\d{3}-\d{2}-\d{2}",
                r"\+7\(\d{3}\)\d{7}", r"\+7 \(\d{3}\) \d{3}-\d{2}-\d{2}", ]
for qwe in sums:
    try:
        line = re.findall(qwe, text)[0]
        print(line)
    except:
        pass
