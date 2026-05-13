# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge


@cocotb.test()
async def test_project(dut):

    dut._log.info("Starting Up/Down Counter Test")

    # Start clock
    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start())

    # Initialize inputs
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0

    # Apply reset
    dut.rst_n.value = 0

    # Hold reset for 5 cycles
    for _ in range(5):
        await RisingEdge(dut.clk)

    # Release reset
    dut.rst_n.value = 1

    # -------------------------
    # Test UP Counter
    # -------------------------
    dut._log.info("Testing UP counter")

    # ui_in[0] = 1 -> UP mode
    dut.ui_in.value = 0b00000001

    expected = 0

    for _ in range(5):

        # Wait for clock edge
        await RisingEdge(dut.clk)

        # Expected increment
        expected = (expected + 1) % 16

        # Read counter
        observed = dut.uo_out.value.to_unsigned() & 0xF

        dut._log.info(
            f"UP Expected={expected} Observed={observed}"
        )

        assert observed == expected, \
            f"UP Counter Error: Expected {expected}, Got {observed}"

    # -------------------------
    # Test DOWN Counter
    # -------------------------
    dut._log.info("Testing DOWN counter")

    # ui_in[0] = 0 -> DOWN mode
    dut.ui_in.value = 0b00000000

    for _ in range(5):

        # Wait for clock edge
        await RisingEdge(dut.clk)

        # Expected decrement
        expected = (expected - 1) % 16

        # Read counter
        observed = dut.uo_out.value.to_unsigned() & 0xF

        dut._log.info(
            f"DOWN Expected={expected} Observed={observed}"
        )

        assert observed == expected, \
            f"DOWN Counter Error: Expected {expected}, Got {observed}"

    dut._log.info("TEST PASSED")
