# Cloud_ComputeData.py

Position_file = "Data/Item_Region.txt"
Price_file = "Data/Price.txt"
Account_file = "Data/Account.txt"
History_file = "Data/Shopping_History.txt"




def _parser(filename: str, parse_account = False) -> dict:
    result = dict()
    f = open(filename, "r")
    for line in f:
        l = line.strip().split("|")
        if parse_account:
            result[l[0].strip().lower()] = (l[1].strip(), l[2].strip())
        else:
            result[l[0].strip().lower()] = l[1].strip()
    return result


def getDataDict() -> ("position_dict", "price_dict", "id_dict"):
    pos_dict = _parser(Position_file)
    price_dict = _parser(Price_file)
    id_dict = _parser(Account_file, True)
    return (pos_dict, price_dict, id_dict)


def updateAccount(Id: str, name: str, password: str) -> int:
    try:
        with open(Account_file, "a+") as f:
            f.write(Id + "|" + name + "|" + password + "\n")
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