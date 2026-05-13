## How it works

This project implements a 4-bit synchronous up/down counter.  
The counter increments or decrements on every positive edge of the clock depending on the mode input.

- `ui[0] = 1` → Counter counts UP
- `ui[0] = 0` → Counter counts DOWN

The 4-bit counter output is available on `uo[3:0]`.

---

## How to test

1. Apply clock signal to the design.
2. Apply active-low reset (`rst_n = 0`) to reset the counter to 0.
3. Set `ui[0] = 1` for up counting.
4. Set `ui[0] = 0` for down counting.
5. Observe counter output on `uo[3:0]`.

---

## External hardware

No external hardware is required.
