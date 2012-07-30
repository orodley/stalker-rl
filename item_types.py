# All firearm types (including pistols, shotguns, rifles, etc.)
firearms ={\
# Name
"Makarov PM": ["Pistol",                        # Type (pistol, assault rifle, battle rifle, shotgun, etc.)
               ["Makarov PM 8-round magazine"], # Compatible magazine(s).
               [],                              # Supported attachments (scopes, silencer, etc.)
               [],                              # Compatible ammo (for non-magazine weapons, e.g. shotguns)
               [1],                             # Burst size(s) (0 = full-auto, 1 = semi, 3 = 3-round burst, etc)
                                                #    some firearms have multiple modes that can be cycled through
               20,                              # Reliability (lower is better). Condition (max 10000) decreases by this every shot
               15,                              # Accuracy. Range the bullet angle is offset by upon firing.
               10,                              # Damage
               730,],                           # Unloaded weight in grams.
}

magazines = {\
# Name
"Makarov PM 8-Round Magazine": [["9x18mm Makarov"], # Which rounds can be loaded into the magazine
                                8]                  # Capacity
}
