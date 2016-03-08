--------------------------------------------------------------------------------
-- Company: 
-- Engineer:
--
-- Create Date:   12:54:26 10/14/2015
-- Design Name:   
-- Module Name:   C:/Users/alberini/Desktop/xem_tut/ProvaOk/tb_sens_decoder.vhd
-- Project Name:  ProvaOk
-- Target Device:  
-- Tool versions:  
-- Description:   
-- 
-- VHDL Test Bench Created by ISE for module: SensDecoder
-- 
-- Dependencies:
-- 
-- Revision:
-- Revision 0.01 - File Created
-- Additional Comments:
--
-- Notes: 
-- This testbench has been automatically generated using types std_logic and
-- std_logic_vector for the ports of the unit under test.  Xilinx recommends
-- that these types always be used for the top-level I/O of a design in order
-- to guarantee that the testbench will bind correctly to the post-implementation 
-- simulation model.
--------------------------------------------------------------------------------
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.std_logic_arith.all;
use IEEE.std_logic_misc.all;
use IEEE.std_logic_unsigned.all;
use IEEE.numeric_std.all;
 
-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
--USE ieee.numeric_std.ALL;
 
ENTITY tb_sens_decoder IS
END tb_sens_decoder;
 
ARCHITECTURE behavior OF tb_sens_decoder IS 
 
    -- Component Declaration for the Unit Under Test (UUT)
 
    COMPONENT SensDecoder
    PORT(
			-- INS --
         clk 			: 	in  	STD_LOGIC;
         sigFromXem 	: 	in  	STD_LOGIC_VECTOR(2 downto 0);
			in_ser	  	: 	in 	STD_LOGIC;
			pcContWire	: 	in 	STD_LOGIC_VECTOR(15 downto 0);
         -- OUTS --
			dataSens 	: 	out  	STD_LOGIC_VECTOR(15 downto 0);
			dLoadAck		:	out	STD_LOGIC;
			init_out		: 	out	STD_LOGIC;
         f_write 		:	out  	STD_LOGIC
        );
    END COMPONENT;
    

   --Inputs
   signal clk 			: 	STD_LOGIC := '0';
   signal sigFromXem : 	STD_LOGIC_VECTOR(2 downto 0) := (others => '0');
	signal in_ser		: 	STD_LOGIC;
	signal pcContWire	:	STD_LOGIC_VECTOR(15 downto 0);

 	--Outputs
   signal dataSens 	: 	STD_LOGIC_VECTOR(15 downto 0);
   signal f_write 	: 	STD_LOGIC;
	signal init_out	:	STD_LOGIC;
	signal dLoadAck	:	STD_LOGIC;
	

   -- Clock period definitions
   constant clk_period : time := 10 ns;
 
BEGIN
 
	-- Instantiate the Unit Under Test (UUT)
   uut: SensDecoder PORT MAP (
			-- INS --
          clk 			=> clk,
			 in_ser 		=> in_ser,
          sigFromXem => sigFromXem,
			 pcContWire	=> pcContWire,
			 -- OUTS -- 
          dataSens 	=> dataSens,
			 init_out	=>	init_out,
			 dLoadAck	=> dLoadAck,
          f_write 	=> f_write
        );

   -- Clock process definitions
   clk_process :process
   begin
		clk <= '0';
		wait for clk_period/2;
		clk <= '1';
		wait for clk_period/2;
   end process;
 

   -- Stimulus process
   stim_proc: process
   begin		

      wait for clk_period*10;

		-- Set the pcContWire
		pcContWire <= STD_LOGIC_VECTOR(to_unsigned(2, 16));
		
		wait for clk_period;
		
		-- Reset the FSM for setting the cont
		sigFromXem <= "010";
		wait for clk_period;
		sigFromXem <= "000";
		
		-- Init the take photo signal
		sigFromXem <= "001";
		wait for clk_period;
		sigFromXem <= "000";
		
		wait for 3*clk_period;
		
		in_ser <= '1';
		
		wait for 3*clk_period;
		in_ser <= not in_ser;
		
		wait for 3*clk_period;
		in_ser <= not in_ser;
		
		wait for 3*clk_period;
		in_ser <= not in_ser;
		
		wait for 3*clk_period;
		in_ser <= not in_ser;
		
		wait for 100 ns;

      wait;
   end process;

END;
