# Unit test

# Generate some options
from options import options
o = options("all_options.csv")
o.add_entry(True, True, True, "ex 1")
o.add_entry(True, True, True, "ex 2")
o.add_entry(True, True, True, "ex 3")
o.add_entry(True, True, True, "ex 4")
o.add_entry(True, True, True, "ex 5")
o.add_entry(True, True, True, "ex 6")
o.add_entry(True, False, True, "ex 7")
o.add_entry(True, False, True, "ex 8")
o.add_entry(True, True, False, "ex 9")
o.add_entry(True, True, False, "ex 10")
o.add_entry(False, True, False, "ex 11")
o.add_entry(False, True, False, "ex 12")

# Get card
from card import card
c = card("test")
c.generate_random_card(True, False, True)
c.complete_entry(15)
c.complete_entry(22)
c.print_card()
c.print_tasks()