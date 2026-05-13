/*
 * Copyright (c) 2026 Priyaharini Palanisamy
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_example (
    input  wire [7:0] ui_in,
    output wire [7:0] uo_out,
    input  wire [7:0] uio_in,
    output wire [7:0] uio_out,
    output wire [7:0] uio_oe,
    input  wire       ena,
    input  wire       clk,
    input  wire       rst_n
);

    // 4-bit counter
    reg [3:0] count;

    // mode select
    // ui_in[0] = 1 → UP
    // ui_in[0] = 0 → DOWN
    wire mode;

    assign mode = ui_in[0];

    // ACTIVE LOW RESET
    always @(posedge clk or negedge rst_n)
    begin
        if (!rst_n)
            count <= 4'b0000;

        else begin

            if (mode)
                count <= count + 1'b1;

            else
                count <= count - 1'b1;
        end
    end

    // Output mapping
    assign uo_out = {4'b0000, count};

    // Unused IOs
    assign uio_out = 8'b00000000;
    assign uio_oe  = 8'b00000000;

    // Prevent warnings
    wire _unused = &{ena, uio_in, ui_in[7:1], 1'b0};

endmodule

`default_nettype wire
