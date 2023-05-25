import re

def extract_err_lists():
    err_lists=[]
    with open('major_lv_log.log', 'r') as f:
        for line in f:
            match = re.search(r'at (.*)\. Error', line)
            if match:
                err_lists.append(match.group(1))
    return err_lists
