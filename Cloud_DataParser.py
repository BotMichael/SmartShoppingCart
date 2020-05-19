# Cloud_ComputeData.py

Position_file = "./Data/Position.txt"
Price_file = "./Data/Price.txt"
Account_file = "./Data/Account.txt"


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
