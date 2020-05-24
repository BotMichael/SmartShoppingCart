# Cloud_ComputeData.py

Position_file = "Data/Item_Region.txt"
Price_file = "Data/Price.txt"
Account_file = "Data/Account.txt"
History_file = "Data/Shopping_History.txt"




def _parser(filename: str) -> dict:
    result = dict()
    f = open(filename, "r")
    for line in f:
        l = line.strip().split("|")
        result[l[0].strip().lower()] = l[1].strip()
    return result


def getDataDict() -> ("position_dict", "price_dict", "id_dict"):
    pos_dict = _parser(Position_file)
    price_dict = _parser(Price_file)
    id_dict = _parser(Account_file)
    return (pos_dict, price_dict, id_dict)


def updateAccount(name: str, password: str) -> int:
    try:
        with open(Account_file, "a+") as f:
            f.write(name + "|" + password + "\n")
    except:
        return 1
    else:
        return 0


def getUserHistory(userID:str):
    with open(History_file) as f:
        items = []
        for line in f:
            line = line.strip().split("|")
            if line[0] == userID:
                items.append([line[i] for i in range(1,len(line),2)])
        return items


def updateUserHistory(History_file: str, hist: []):
    try:
        with open(History_file, "a+") as f:
            f.write('|'.join(hist) + "\n")
    except:
        return 1
    else:
        return 0