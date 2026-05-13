import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge


@cocotb.test()
async def test_project(dut):

    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start())

    dut.ena.value = 1

    # reset
    dut.rst_n.value = 0

    for _ in range(5):
        await RisingEdge(dut.clk)

    dut.rst_n.value = 1

    # UP mode
    dut.ui_in.value = 1

    # wait one cycle
    await RisingEdge(dut.clk)

    # check counting
    for expected in range(1, 6):

        observed = dut.uo_out.value.to_unsigned() & 0xF

        dut._log.info(
            f"Expected={expected} Observed={observed}"
        )

        assert observed == expected

        await RisingEdge(dut.clk)
