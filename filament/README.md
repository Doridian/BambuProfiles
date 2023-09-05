# Filament profiles

## PolyLite ASA

This profile is based on "Generic ASA".

Profile: [PolyLite ASA.json](PolyLite%20ASA.json)

Test print: [PolyLite ASA.jpg](PolyLite%20ASA.jpg)

### Differences

| Option | This | Base |
|--------|------|------|
| cool_plate_temp | 90 | 0 |
| cool_plate_temp_initial_layer | 90 | 0 |
| filament_cost | 29.99 | 20 |
| filament_density | 1.13 | 1.04 |
| filament_end_gcode | ```gcode
; filament end gcode 
;M106 P3 S0
``` | ```gcode
; filament end gcode 
M106 P3 S0
``` |
| filament_max_volumetric_speed | 20 | 12 |
| nozzle_temperature_range_high | 260 | 280 |
