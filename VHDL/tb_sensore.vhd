--------------------------------------------------------------------------------
-- Company: 
-- Engineer:
--
-- Create Date:   10:44:31 10/13/2015
-- Design Name:   
-- Module Name:   C:/Users/alberini/Desktop/xem_tut/ProvaOk/tb_sensore.vhd
-- Project Name:  ProvaOk
-- Target Device:  
-- Tool versions:  
-- Description:   
-- 
-- VHDL Test Bench Created by ISE for module: Sensore
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
LIBRARY ieee;
USE ieee.std_logic_1164.ALL;
 
-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
--USE ieee.numeric_std.ALL;
 
ENTITY tb_sensore IS
END tb_sensore;
 
ARCHITECTURE behavior OF tb_sensore IS 
 
    -- Component Declaration for the Unit Under Test (UUT)
 
    COMPONENT Sensore
    PORT(
         clk : IN  std_logic;
         hi_in : IN  std_logic_vector(7 downto 0);
         hi_out : OUT  std_logic_vector(1 downto 0);
         trig_out : OUT  std_logic;
			inner_out : OUT std_logic_vector(9 downto 0);
         hi_inout : INOUT  std_logic_vector(15 downto 0);
         leds : OUT  std_logic_vector(7 downto 0)
        );
    END COMPONENT;
    

   --Inputs
   signal clk : std_logic := '0';
   signal hi_in : std_logic_vector(7 downto 0) := (others => '0');

	--BiDirs
   signal hi_inout : std_logic_vector(15 downto 0);

 	--Outputs
   signal hi_out : std_logic_vector(1 downto 0);
   signal trig_out : std_logic;
	signal inner_out : std_logic_vector(9 downto 0);
   signal leds : std_logic_vector(7 downto 0);

   -- Clock period definitions
   constant clk_period : time := 10 ns;
 
BEGIN
 
	-- Instantiate the Unit Under Test (UUT)
   uut: Sensore PORT MAP (
          clk => clk,
          hi_in => hi_in,
          hi_out => hi_out,
          trig_out => trig_out,
			 inner_out => inner_out,
          hi_inout => hi_inout,
          leds => leds
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
      -- hold reset state for 100 ns.
      wait for 100 ns;	

      wait for clk_period*10;

      -- insert stimulus here 

      wait;
   end process;

END;
