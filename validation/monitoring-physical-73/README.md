# Candidate 73 physical MAX4 test

On 2026-11-06, candidate73 (`c3384380cc774768cdaea58e1d41f4f7feb4fbad7d4bf6426082437fade91149`) sent a 20-layer ABS block through Orca to the MAX4 with a 0.4 mm nozzle. Printer history job 000032 reports completed, with total duration 939.6 seconds. Telemetry reached layer 20/20, and the printer returned to standby with both heater targets zero and filament unloaded.

A3 was selected and confirmed loaded. Auto bed leveling and timelapse were enabled; probing was observed and a new timelapse MP4 was rendered. Polar cooler was off. Automatic refill was not triggered in this test.

During startup Orca showed N/A. A captured screen at layer 5/20 displayed approximately 3 minutes remaining; the job finished approximately 151 seconds after that capture, including the end and unload sequence. This single small print supports the revised ETA behavior but does not establish accuracy for other jobs. Physical part quality was not independently assessed.

The firmware startup requested 280°C at the nozzle before the 250°C print target; telemetry sampled a peak of 287°C. This is separate from the ETA change.
