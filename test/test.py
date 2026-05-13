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

    # Initialize
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0

    # Apply reset
    dut.rst_n.value = 0

    for _ in range(5):
        await RisingEdge(dut.clk)

    # Release reset
    dut.rst_n.value = 1

    # Wait one clock after reset
    await RisingEdge(dut.clk)

    # -------------------------
    # Test UP counter
    # -------------------------
    dut._log.info("Testing UP counter")

    dut.ui_in.value = 1

    expected = 1

    for _ in range(5):

        observed = dut.uo_out.value.to_unsigned() & 0xF

        dut._log.info(
            f"UP Expected={expected} Observed={observed}"
        )

        assert observed == expected, \
            f"UP Counter Error: Expected {expected}, Got {observed}"

        await RisingEdge(dut.clk)

        expected = (expected + 1) % 16

    # -------------------------
    # Test DOWN counter
    # -------------------------
    dut._log.info("Testing DOWN counter")

    dut.ui_in.value = 0

    for _ in range(5):

        await RisingEdge(dut.clk)

        expected = (expected - 1) % 16

        observed = dut.uo_out.value.to_unsigned() & 0xF

        dut._log.info(
            f"DOWN Expected={expected} Observed={observed}"
        )

        assert observed == expected, \
            f"DOWN Counter Error: Expected {expected}, Got {observed}"

    dut._log.info("TEST PASSED")
