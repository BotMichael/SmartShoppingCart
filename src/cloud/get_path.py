
# Move to Cloud_DataParser.py

# Path_to_Item_Region_File = "./Data/Item_Region.txt"
# # load item-region data
# Item_Position_Dict = {}
# with open(Path_to_Item_Region_File) as f:
#     for line in f:
#         item, pos = line.rstrip().split("|")
#         Item_Position_Dict[item] = pos
#

class MarketMap():
    def __init__(self, item_region: dict):
        ## TODO: Represent market blueprint better and so do the method
        # market blueprint
        #   [A][B][C][D]
        #   [E][F][G][H]
        #   [I][J][K][L]
        self.MARKET = [["A","B","C","D"],
                      ["E","F","G","H"],
                      ["I","J","K","L"]]
        self.Letters = ["A","B","C","D","E","F","G","H","I","J","K","L"]
        # j-9
        # j%4=1, (9-1)/4=2
        self.Item_Position_Dict = item_region
     
     
    def get_item_region(self,item):
        return self.Item_Position_Dict[item]

    def path_to_item(self, current_position: str, item: str):
        '''input user current_position and item_name
            return a list of Regions'''

        target_region = self.get_item_region(item)
        return self._path_to_loc(current_position, target_region)


    def _path_to_loc(self, current_position, target_region):
        target_region_index = self.Letters.index(target_region)
        col_t = target_region_index % 4
        row_t = (target_region_index - col_t) // 4

        current_position_index = self.Letters.index(current_position)
        col_c = current_position_index % 4
        row_c = (current_position_index - col_c) // 4

        steps = [current_position]
        for i in range(abs(col_t - col_c)):
            if col_t > col_c:
                steps.append(self.MARKET[row_c][col_c + i + 1])
            else:
                steps.append(self.MARKET[row_c][col_c - i - 1])

        for i in range(abs(row_t - row_c)):
            if row_t > row_c:
                steps.append(self.MARKET[row_c + i + 1][col_t])
            else:
                steps.append(self.MARKET[row_c - i - 1][col_t])

        return steps

    def default_path_to_items(self) -> ["path"]:
        '''Assume start from A and end at A'''
        return ["A","B","C","D","H","G","F","E","I","J","K","A"]

    ## TODO: shortest path to items; it may be considered as a traveling saleman problem
    def path_to_items(self, items : ["item"]) -> ["path"]:
        '''Assume start from A and end at A; greedy, not ensure optimal'''
        target_regions = {self.get_item_region(item) for item in items}.difference_update('A')
        path = ['A']
        curr = 'A'
        while target_regions:
            p = min(self.shortest_path_to_all(curr, target_regions), key=lambda x: len(x))
            curr = p[-1]
            target_regions.remove(curr)
            path += p[1:]

        if path[-1] != 'A':
            path += self._path_to_loc(path[-1], 'A')[1:]

        return path

    def shortest_path_to_all(self, start, targets):
        path = []
        for reg in targets:
            if reg == start:
                continue
            path.append(self._path_to_loc(start, reg))
        return path

# def test1():
#     assert get_item_region("apple")=="G" , "ERROR1"
#     assert get_item_region("water")=="A" , "ERROR2"
#     return "passed"
#
# def test2():
#     assert path_to_item("G","apple")==["G"],"ERROR1"
# #    print(path_to_item("A","apple"))
#     assert path_to_item("A","apple")==["A","B","C","G"],"ERROR2"
#     assert path_to_item("G","water")==["G","F","E","A"],"ERROR3"
#     return "passed"
#
# if __name__ == "__main__":
#     num_test = 2
#     for i in range(num_test):
#         t = f"test{i+1}()"
#         print(f"Running test{i}: {eval(t)}")
