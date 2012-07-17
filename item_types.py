# All firearm types (including pistols, shotguns, rifles, etc.)
firearms ={\

# Name
"Makarov PM": ["Pistol",                        # Type
               ["Makarov PM 8-round magazine"], # Compatible magazine(s).
               [1],                             # Burst size(s) (0 = full-auto, 1 = semi, 3 = 3-round burst, etc)
                                                #    some firearms have multiple modes that can be cycled through
               0,                               # Slot (0 = pistol/shotgun/SMG slot, 1 = rifle slot)
               730,                             # Unloaded weight in grams.
               20,                              # Reliability (lower is better). Condition (max 10000) decreases by this every shot
               15,                              # Accuracy. Range the bullet angle is offset by upon firing.
               10],                             # Damage
               [],                              # Supported attachments (scopes, silencer, etc.)
               []                               # Compatible ammo (for non-magazine weapons, e.g. shotguns)
}
