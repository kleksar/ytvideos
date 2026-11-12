import json
from pathlib import Path
rooms = ['bedroom', 'kitchen', 'bathroom']
items = {room: [f'{room}_1', f'{room}_2'] for room in rooms}
one_at_a_time = [{'room': room, 'items': [item], 'meters': 20} for room in rooms for item in items[room]]
basket = [{'room': room, 'items': items[room], 'meters': 20} for room in rooms]
assert len(one_at_a_time) == 6 and sum(x['meters'] for x in one_at_a_time) == 120
assert len(basket) == 3 and sum(x['meters'] for x in basket) == 60
result = {'model': {'one_way_meters_per_room': 10, 'return_to_hallway_after_each_trip': True, 'basket_capacity': 6, 'room_pairs_accessible': True}, 'individual': one_at_a_time, 'basket': basket, 'individual_total_meters': 120, 'basket_total_meters': 60}
Path(__file__).with_name('events.json').write_text(json.dumps(result, indent=2) + '\n')
