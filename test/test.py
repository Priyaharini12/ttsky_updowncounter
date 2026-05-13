# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge


@cocotb.test()
async def test_project(dut):

    dut._log.info("Starting Up/Down Counter Test")

    # Start 10ns clock
    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start())

    # Initialize
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0

    # Apply reset
    dut.rst_n.value = 0

    # Hold reset
    for _ in range(5):
        await RisingEdge(dut.clk)

    # Release reset
    dut.rst_n.value = 1

    # Select UP mode
    dut.ui_in.value = 0b00000001

    # IMPORTANT:
    # Wait one FULL clock after reset release
    await RisingEdge(dut.clk)

    dut._log.info("Testing UP counter")

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

    # DOWN counter test
    dut._log.info("Testing DOWN counter")

    dut.ui_in.value = 0b00000000

    expected = (expected - 1) % 16

    await RisingEdge(dut.clk)

    for _ in range(5):

        observed = dut.uo_out.value.to_unsigned() & 0xF

        dut._log.info(
            f"DOWN Expected={expected} Observed={observed}"
        )

        assert observed == expected, \
            f"DOWN Counter Error: Expected {expected}, Got {observed}"

        await RisingEdge(dut.clk)

        expected = (expected - 1) % 16

    dut._log.info("TEST PASSED")
