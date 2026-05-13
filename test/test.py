# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer


@cocotb.test()
async def test_project(dut):

    dut._log.info("Starting Test")

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

    # Set UP mode
    dut.ui_in.value = 1

    # Wait for first active clock
    await RisingEdge(dut.clk)

    expected = 1

    # Test UP counter
    for _ in range(5):

        # Wait tiny delay for <= update
        await Timer(1, unit="ns")

        observed = dut.uo_out.value.to_unsigned() & 0xF

        dut._log.info(
            f"Expected={expected} Observed={observed}"
        )

        assert observed == expected, \
            f"Expected {expected}, Got {observed}"

        expected = (expected + 1) % 16

        await RisingEdge(dut.clk)

    dut._log.info("TEST PASSED")
