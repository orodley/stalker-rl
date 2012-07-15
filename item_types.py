# All firearm types (including pistols, shotguns, rifles, etc.)
firearms ={\

# Name
"Makarov PM": ["Pistol",                        # Type
               ["Makarov PM 8-round magazine"], # Compatible magazine(s).
               [1],                             # Burst size(s) (0 = full-auto, 1 = semi, 3 = 3-round burst, etc)
                                                #    some firearms have multiple modes that can be cycled through
               730,                             # Unloaded weight in grams.
               20,                              # Reliability (lower is better). Condition (max 10000) decreases by this every shot
               15]                              # Accuracy. Range the bullet angle is offset by upon firing.
}
