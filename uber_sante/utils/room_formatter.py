class FormatRoom:

    all_rooms = {
            '101': 101,
            '102': 102,
            '103': 103,
            '104': 104,
            '105': 105,
        }

    def negate_rooms(self, value):
        rooms = {
            '101': 101,
            '102': 102,
            '103': 103,
            '104': 104,
            '105': 105,
        }

        for room in value:
            del rooms[room['room']]
        
        return rooms
