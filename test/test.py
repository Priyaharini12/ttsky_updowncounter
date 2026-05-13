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

    # Initialize signals
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
    dut.ui_in.value = 0b00000001

    dut._log.info("Testing UP counter")

    expected = 0

    for _ in range(5):

        # wait for counter update
        await RisingEdge(dut.clk)

        observed = dut.uo_out.value.to_unsigned() & 0xF

        expected = expected + 1

        dut._log.info(
            f"UP Expected={expected} Observed={observed}"
        )

        assert observed == expected, \
            f"UP Counter Error: Expected {expected}, Got {observed}"

    dut._log.info("Testing DOWN counter")

    # Set DOWN mode
    dut.ui_in.value = 0b00000000

    for _ in range(5):

        await RisingEdge(dut.clk)

        observed = dut.uo_out.value.to_unsigned() & 0xF

        expected = (expected - 1) % 16

        dut._log.info(
            f"DOWN Expected={expected} Observed={observed}"
        )

        assert observed == expected, \
            f"DOWN Counter Error: Expected {expected}, Got {observed}"

    dut._log.info("TEST PASSED")
