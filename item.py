import libtcodpy as tcod
import entity
import constant

class Inventory(dict):

    """ The inventory of an (N)PC. Uses Items for keys, and ints for values.
    The value associated with a key represents the number of items there are.
    Items equipped are also stored here, with a reference in the corresponding
    Equipment dict

    owner         -- Reference to the entity it is the inventory of
    width, height -- Size of inventory when represented as a grid
    grid          -- 2D array storing references to each item's location in the
                     inventory grid
    weight        -- Total weight of items carried
    weight_limit  -- Maximum weight that can be carried while
    volume        -- Total area of items currently in grid.
    volume        -- Total area of grid.
    """

    def __init__(self, owner, width, height, weight_limit):
        self.owner = owner
        (self.width, self.height) = (width, height)
        self.clear_grid()
        self.volume = 0
        self.max_volume = width * height
        self.weight = 0
        self.weight_limit = weight_limit

    def clear_grid(self):
        """Resets the inventory grid to an empty state"""

        self.grid = [[None for x in xrange(self.width)] for y in xrange(self.height)]

    def get_stacks(self):
        """Iterates over the inventory, returning each item once for every stack of that item"""

        for item in self.keys():
            for instance in xrange(self[item] / item.stacks):
                yield item

    def add_item_to_grid(self, item):
        """Adds item to the grid, reordering all existing items, and returning False
        if impossible. Should not be called directly. add() should be called instead"""

        print item.dimensions
        if self.volume + item.dimensions[0] * item.dimensions[1] > self.max_volume:
            return False
        self.clear_grid()
        for _item in sorted(self.get_stacks() + [item],
                            key=lambda an_item:
                                    -an_item.dimensions[0] * an_item.dimensions[1]):
            if not self.place_item_in_grid(_item):
                return False
        self.items[repr(item)] = item
        return True

    def place_item_in_grid(self, item):
        """Attempts to place a item into the grid, returning False if impossible"""

        for y in xrange(self.height):
            for x in xrange(self.width):
                if self.can_place_item_at(item, x, y):
                    for dx in xrange(item.dimensions[0]):
                        for dy in xrange(item.dimensions[1]):
                            self.grid[y + dy][x + dx] = item
                    return True
        return False

    def can_place_item_at(self, item, x, y):
        """Returns True if item can be placed at (x, y) in the grid"""

        if (x + item.dimensions[0] - 1 >= self.width) or (y + item.dimensions[1] - 1 >= self.height):
            return False
        for dx in xrange(item.dimensions[0]):
            for dy in xrange(item.dimensions[1]):
                if self.grid[y + dy][x + dx] is not None:
                    return False
        return True

    def add(self, item):
        """Adds item to inventory, adjusting the grid and weight"""

        if item in self.keys:
            if self[item] < item.stacks or self.add_item_to_grid(item):
                self[item] += 1
                self.weight += item.weight
            else:
                return "INVENTORY_FULL" # Item cannot fit in inventory
        else:
            if self.add_item_to_grid(item):
                self[item] = 1
                self.weight += item.weight
            else:
                return "INVENTORY_FULL" # Item cannot fit in inventory

    def drop(self, item):
        """Remove item from containing inventory, and spawn a new entity with item as the item_component"""

        if self[item] == 1:
            self.pop(item)
        else:
            self[item] -= 1

        item_entity = entity.Entity(self.owner.x, self.owner.y, item.char, item.fore_color, item_component = item)
        item.owner = item_entity 
        return item_entity

class Item:

    """Represents an item in an inventory or in the map attached to a item entity
    owner              -- The owning entity if item is dropped on the map
    name               -- Name of the item. If an item has no components it is hashed by its
                          name, so this must not be changed in place while it is in a dict
                          (such as an inventory)
    stacks             -- Maximum number of this item that can stack in an inventory
    dimensions         -- An (x, y) tuple containing the size of the item in an inventory
    plural_name        -- Name to use when there are more than one of the item
    weight             -- Weight of the item in grams
    char               -- Character to represent the item when dropped
    fore_color         -- Color of the character representing the item when dropped
    inventory          -- The Inventory the Item is contained within, if it is in an inventory
    gun_component      -- If item is a gun, a Gun object representing it
    magazine_component -- If item is a magazine, a Magazine object representing it
    """

    def __init__(self, name, weight, char, owner=None, fore_color=tcod.grey, stacks=1, dimensions=(1,1),
                 plural_name=None, inventory=None, gun_component=None, magazine_component=None):
        self.name = name
        self.weight = weight
        self.char = char
        
        if owner:
            self.owner = owner

        self.fore_color = fore_color
        self.stacks = stacks
        self.dimensions = dimensions

        if not plural_name:
            plural_name = name + "s"

        if inventory:
            self.inventory = inventory
        if gun_component:
            self.gun_component = gun_component
        if magazine_component:
            self.magazine_component = magazine_component

    def __hash__(self):
        if self.gun_component:
            # All guns are considered different, and should have a stacks of 1 anyway
            return hash(self)
        if self.magazine_component:
            # Likewise, all magazines are considered different. Otherwise they could become
            # the same after rounds are loaded or unloaded
            return hash(self)
        else: # Items with no components are defined by their names
            return hash(self.name)

    def __eq__(self, other):
        if (self.gun_component  or self.magazine_component or
            other.gun_component or other.magazine_component):
            # All guns and magazines are considered different
            return False
        else:
            return self.name == other.name # Items with no components are defined by their names
            
class Gun:

    """Represents a gun. Always a component of an Item

    owner                 -- Reference to owning Item
    supported_magazines   -- Which magazines can be loaded into this gun
    burst_sizes           -- Integer array of supported burst sizes (e.g. [1,3,0] for
                             an assault rifle)
    reliability           -- How much a gun degrades with every shot
    accuracy              -- Max angle at which a shot can be randomly offset upon firing
    damage                -- How much damage a single bullet causes
    supported_attachments -- Which attachments can be attached to this gun (silencers,
                             scopes, etc.)
    supported_ammo        -- For non-magazine guns (shotguns, grenade launchers etc.),
                             the supported ammo types
    loaded_ammo_type      -- For non-magazine guns, the currently loaded ammo type
    loaded_ammo           -- For non-magazine guns, the amount of ammo loaded
    magazine              -- The currently loaded magazine. None if empty
    attachments           -- Which attachments are currently attached to the gun
    condition             -- Current condition of the gun. Affects selling price, damage, accuracy,
                             and jamming frequency
    """

    def __init__(self, owner, supported_magazines, burst_sizes, slot, reliability, accuracy, damage, supported_attachments,
                 supported_ammo=None, loaded_ammo_type=None, loaded_ammo=None, magazine=None, attachments=[], condition=constant.MAX_CONDITION):
        self.owner = owner
        self.supported_magazines = supported_magazines
        self.burst_sizes = burst_sizes
        self.slot = slot
        self.reliability = reliability
        self.accuracy = accuracy
        self.damage = damage
        self.supported_attachments = supported_attachments 

        self.supported_ammo = supported_ammo
        self.loaded_ammo_type = loaded_ammo_type
        self.loaded_ammo = loaded_ammo
        
        self.magazine = magazine 
        self.attachments = attachments
        self.condition =  condition

    def load_magazine(self, magazine):
        if self.supported_ammo:
            return "NON_MAG_WEAPON" # This gun does not use magazines
        if magazine.name in self.supported_magazines:
            if not self.magazine:
                self.magazine = magazine
            else:
                return "MAG_LOADED" # A magazine is already loaded
        else:
            return "MAG_UNSUPPORTED" # That magazine type is unsupported in this gun

    def unload_magazine(self):
        temp = self.magazine
        self.magazine = None
        return temp

    def load_round(self, _round):
        if not self.supported_ammo:
            return "MAG_WEAPON" # This gun uses magazines
        if not _round.name in self.supported_ammo:
            return "AMMO_UNSUPPORTED" # This ammo type is unsupported in this gun
        if self.loaded_ammo_type and self.loaded_ammo_type != _round.name:
            return "DIFFERENT_AMMO" # This ammo type is different to the currently
                                    # loaded ammo type
        if not self.loaded_ammo_type:
            self.loaded_ammo_type = _round.name
            self.loaded_ammo = 1

class Magazine:

    """A magazine. Can have ammo loaded into it, and be loaded into a gun

    owner             -- Reference to owning Item
    capacity          -- Maximum number of loaded rounds
    supported_rounds  -- Round types that can be loaded into magazine
    loaded_round_type -- Name of the type of round loaded into magazine
    loaded_rounds     -- Current number of rounds loaded into magazine
    """

    def __init__(self, owner, capacity, supported_rounds, loaded_round_type="", loaded_rounds=0):
        self.owner = owner
        self.capacity = capacity
        self.supported_rounds = supported_rounds
        self.loaded_round_type = loaded_round_type
        self.loaded_rounds = loaded_rounds

    def load_round(self, round_item):
        if not round_item.name in self.supported_rounds:
            return "ROUND_UNSUPPORTED" # This round cannot be loaded into this magazine
        if not (self.loaded_round_type and (self.loaded_round_type == round_item.name)):
            return "DIFFERENT_ROUND"   # This round is a different type to what is already loaded
        else:
            self.loaded_rounds += 1

    def unload_round(self):
        if self.loaded_rounds == 0:
            return "NO_ROUNDS" # No rounds in the magazine

        self.loaded_rounds -= 1
        if self.loaded_rounds == 0:
            self.loaded_round_type = None

        return self.loaded_round_type
