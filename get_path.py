

Path_to_Item_Region_File = "./Data/Item_Region.txt"


# load item-region data
Item_Position_Dict = {}
with open(Path_to_Item_Region_File) as f:
    for line in f:
        item, pos = line.rstrip().split(",")
        Item_Position_Dict[item] = pos
    
    
# market blueprint
#   [A][B][C][D]
#   [E][F][G][H]
#   [I][J][K][L]
MARKET = [["A","B","C","D"],
          ["E","F","G","H"],
          ["I","J","K","L"]]
Letters = ["A","B","C","D","E","F","G","H","I","J","K","L"]
# j-9
# j%4=1, (9-1)/4=2

Current_Position = "F" # user will input his/her current location to RP1
     
     
def get_item_region(item):
    return Item_Position_Dict[item]

def path_to_item(current_position,item):
    '''input user current_position and item_name
        return a list of Regions'''
        
    target_region = get_item_region(item)
    target_region_index = Letters.index(target_region)
    col_t = target_region_index%4
    row_t = (target_region_index-col_t)//4
    
    current_position_index = Letters.index(current_position)
    col_c = current_position_index%4
    row_c = (current_position_index-col_c)//4
    
    steps = [current_position]
    for i in range(abs(col_t-col_c)):
        if col_t > col_c:
            steps.append(MARKET[row_c][col_c+i+1])
        else:
            steps.append(MARKET[row_c][col_c-i-1])
    
    for i in range(abs(row_t-row_c)):
        if row_t > row_c:
            steps.append(MARKET[row_c+i+1][col_t])
        else:
            steps.append(MARKET[row_c-i-1][col_t])

    return steps
    
    
def test1():
    assert get_item_region("apple")=="G" , "ERROR1"
    assert get_item_region("water")=="A" , "ERROR2"
    return "passed"
    
def test2():
    assert path_to_item("G","apple")==["G"],"ERROR1"
#    print(path_to_item("A","apple"))
    assert path_to_item("A","apple")==["A","B","C","G"],"ERROR2"
    assert path_to_item("G","water")==["G","F","E","A"],"ERROR3"
    return "passed"

if __name__ == "__main__":
    num_test = 2
    for i in range(num_test):
        t = f"test{i+1}()"
        print(f"Running test{i}: {eval(t)}")
