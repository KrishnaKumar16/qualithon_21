class Maze:
    super_list = None
    final_result = []
    single_result = []

    def __init__(self, maze_data):
        self.super_list = maze_data
        self.copy_of_super_list = self.super_list.copy()

    def is_2_down(self):
        try:
            if self.copy_of_super_list[self.position_of_4()[0] + 1][self.position_of_4()[1]] == 2:
                return True
            else:
                return False
        except:
            return False

    def is_2_up(self):
        try:
            if self.copy_of_super_list[self.position_of_4()[0] - 1][self.position_of_4()[1]] == 2:
                return True
            else:
                return False
        except:
            return False

    def is_2_left(self):
        try:
            if self.copy_of_super_list[self.position_of_4()[0]][self.position_of_4()[1] - 1] == 2:
                return True
            else:
                return False
        except:
            return False

    def is_2_right(self):
        try:
            if self.copy_of_super_list[self.position_of_4()[0]][self.position_of_4()[1] + 1] == 2:
                return True
            else:
                return False
        except:
            return False

    def directions_of_2(self):
        val = []
        if self.is_2_left():
            val.append('left')
        if self.is_2_right():
            val.append('right')
        if self.is_2_up():
            val.append('up')
        if self.is_2_down():
            val.append('down')
        return val

    def direction_to_move_attain_3(self):
        val = []
        if self.position_of_4()[0] < self.position_of_3()[0]:
            val.append('down')
        if self.position_of_4()[0] > self.position_of_3()[0]:
            val.append('up')
        if self.position_of_4()[1] < self.position_of_3()[1]:
            val.append('right')
        if self.position_of_4()[1] > self.position_of_3()[1]:
            val.append('left')
        return val

    def position_of_3(self):
        for s_index, m_list in enumerate(self.copy_of_super_list):
            if 3 in m_list:
                return s_index, m_list.index(3)

    def position_of_4(self):
        for s_index, m_list in enumerate(self.copy_of_super_list):
            if 4 in m_list:
                return s_index, m_list.index(4)

    def move_to(self, result_of_where_should_I_go, update_result=True, update_single_result = True):
        co_ordinates_of_4 = self.position_of_4()
        if type(result_of_where_should_I_go) is list:
            direction = result_of_where_should_I_go[0]
        else:
            direction = result_of_where_should_I_go
        if direction == 'left':
            self.copy_of_super_list[co_ordinates_of_4[0]][co_ordinates_of_4[1]] = 5
            self.copy_of_super_list[co_ordinates_of_4[0]][co_ordinates_of_4[1] - 1] = 4
            if update_result:
                self.final_result.append(result_of_where_should_I_go)
            if update_single_result:
                self.single_result.append(direction)
        elif direction == 'right':
            self.copy_of_super_list[co_ordinates_of_4[0]][co_ordinates_of_4[1]] = 5
            self.copy_of_super_list[co_ordinates_of_4[0]][co_ordinates_of_4[1] + 1] = 4
            if update_result:
                self.final_result.append(result_of_where_should_I_go)
            if update_single_result:
                self.single_result.append(direction)
        elif direction == 'up':
            self.copy_of_super_list[co_ordinates_of_4[0]][co_ordinates_of_4[1]] = 5
            self.copy_of_super_list[co_ordinates_of_4[0] - 1][co_ordinates_of_4[1]] = 4
            if update_result:
                self.final_result.append(result_of_where_should_I_go)
            if update_single_result:
                self.single_result.append(direction)
        elif direction == 'down':
            self.copy_of_super_list[co_ordinates_of_4[0]][co_ordinates_of_4[1]] = 5
            self.copy_of_super_list[co_ordinates_of_4[0] + 1][co_ordinates_of_4[1]] = 4
            if update_result:
                self.final_result.append(result_of_where_should_I_go)
            if update_single_result:
                self.single_result.append(direction)
        else:
            raise Exception('Invalid direction')

    def where_should_i_go(self):
        filtered_way = list(set(self.directions_of_2()).intersection(set(self.direction_to_move_attain_3())))
        # if 'right' in filtered_way:
        #     if self.copy_of_super_list[self.position_of_4()[0]][11] != 3:
        #         filtered_way.remove('right')
        # if 'left' in filtered_way:
        #     if self.copy_of_super_list[self.position_of_4()[0]][0] != 3:
        #         filtered_way.remove('right')
        # if 'up' in filtered_way:
        #     if self.copy_of_super_list[0][self.position_of_4()[1]] != 3:
        #         filtered_way.remove('up')
        # if 'down' in filtered_way:
        #     if self.copy_of_super_list[11][self.position_of_4()[1]] != 3:
        #         filtered_way.remove('down')
        if filtered_way == []:
            if self.directions_of_2() != []:
                filtered_way = self.directions_of_2()
            # else:
            #     filtered_way = direction_to_move_attain_3()
        copy_of_filtered_way = filtered_way.copy()
        for way in filtered_way:
            if self.is_5_in_the_direction(way):
                copy_of_filtered_way.remove(way)
        return filtered_way

    def is_5_in_the_direction(self, direction):
        co_ordinates_of_4 = self.position_of_4()
        if direction == 'up':
            if self.copy_of_super_list[co_ordinates_of_4[0] - 1][co_ordinates_of_4[1]] == 5:
                return True
            else:
                return False
        if direction == 'down':
            if self.copy_of_super_list[co_ordinates_of_4[0] + 1][co_ordinates_of_4[1]] == 5:
                return True
            else:
                return False
        if direction == 'left':
            if self.copy_of_super_list[co_ordinates_of_4[0]][co_ordinates_of_4[1] - 1] == 5:
                return True
            else:
                return False
        if direction == 'right':
            if self.copy_of_super_list[co_ordinates_of_4[0]][co_ordinates_of_4[1] + 1] == 5:
                return True
            else:
                return False

    def revert_direction(self, direction):
        if direction == 'left':
            return 'right'
        elif direction == 'right':
            return 'left'
        elif direction == 'up':
            return 'down'
        elif direction == 'down':
            return 'up'

    def go_back_till_multiple_result(self):
        rev_list = self.final_result.copy()
        rev_list.reverse()
        for dir in rev_list:
            if len(dir) == 1:
                self.move_to(self.revert_direction(dir[0]), update_result=False, update_single_result=False)
                # print(f"reverted {dir}")
                self.final_result = self.final_result[:-1]
                self.single_result = self.single_result[:-1]
            else:
                self.move_to(self.revert_direction(dir[0]), update_result=False, update_single_result=False)
                self.final_result = self.final_result[:-1]
                self.single_result = self.single_result[:-1]
                for d in dir:
                    if self.is_5_in_the_direction(d) is False:
                        self.final_result.append([d])
                break

    def get_direction(self):
        pos_of_3 = self.position_of_3()
        while self.position_of_4() != pos_of_3:
            val = self.where_should_i_go()
            if val == []:
                if self.is_4_next_to_3():
                    self.move_to(self.direction_to_move_attain_3())
                else:
                    self.go_back_till_multiple_result()
                    val = self.where_should_i_go()
                    self.move_to(val, update_result=False)
            else:
                self.move_to(val)
        print(self.copy_of_super_list)
        return self.single_result

    def is_4_next_to_3(self):
        x4, y4 = self.position_of_4()
        x3, y3 = self.position_of_3()
        if x3 == x4:
            dif = y4 - y3
            if dif == -1 or dif == 1:
                return True
            else:
                return False
        elif y3 == y4:
            dif = x4 - x3
            if dif == -1 or dif == 1:
                return True
            else:
                return False
        else:
            return False

