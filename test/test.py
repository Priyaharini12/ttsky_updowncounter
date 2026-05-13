# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge


@cocotb.test()
async def test_project(dut):

    dut._log.info("Starting Up/Down Counter Test")

    # Create clock: 10 ns period
    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start())

    # Initialize inputs
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0

    # Apply reset
    dut.rst_n.value = 0

    # Hold reset for few cycles
    for _ in range(5):
        await RisingEdge(dut.clk)

    # Release reset
    dut.rst_n.value = 1

    dut._log.info("Testing UP counter")

    # mode = 1 → UP counter
    dut.ui_in.value = 0b00000001

    expected = 0

    # Check UP counting
    for _ in range(5):

        await RisingEdge(dut.clk)

        expected = (expected + 1) % 16

        observed = dut.uo_out.value.to_unsigned() & 0xF

        dut._log.info(
            f"UP Count Expected={expected} Observed={observed}"
        )

        assert observed == expected, \
            f"UP Counter Error: Expected {expected}, Got {observed}"

    dut._log.info("Testing DOWN counter")

    # mode = 0 → DOWN counter
    dut.ui_in.value = 0b00000000

    # Check DOWN counting
    for _ in range(5):

        await RisingEdge(dut.clk)

        expected = (expected - 1) % 16

        observed = dut.uo_out.value.to_unsigned() & 0xF

        dut._log.info(
            f"DOWN Count Expected={expected} Observed={observed}"
        )

        assert observed == expected, \
            f"DOWN Counter Error: Expected {expected}, Got {observed}"

    dut._log.info("TEST PASSED")
