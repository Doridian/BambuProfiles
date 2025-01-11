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
| eng_plate_temp | 90 | 100 |
| eng_plate_temp_initial_layer | 90 | 100 |
| filament_cost | 29.99 | 20 |
| filament_density | 1.13 | 1.04 |
| filament_end_gcode | <pre><code>; filament end gcode </code><br><code>;M106 P3 S0</code><br><code></code></pre> | <pre><code>; filament end gcode </code><br><code>M106 P3 S0</code><br><code></code></pre> |
| filament_max_volumetric_speed | 20 | 12 |
| filament_start_gcode | <pre><code>; Filament gcode</code><br><code></code></pre> | <pre><code>; Filament gcode</code><br><code>{if activate_air_filtration[current_extruder] &amp;&amp; support_air_filtration}</code><br><code>M106 P3 S{during_print_exhaust_fan_speed_num[current_extruder]} </code><br><code>{endif}</code></pre> |
| hot_plate_temp | 90 | 100 |
| hot_plate_temp_initial_layer | 90 | 100 |
| nozzle_temperature_range_high | 260 | 280 |
| textured_plate_temp | 90 | 100 |
| textured_plate_temp_initial_layer | 90 | 100 |
