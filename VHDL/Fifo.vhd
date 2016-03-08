----------------------------------------------------------------------------------
-- Company: 				FBK
-- Engineer: 				Alberini Giacomo
-- 
-- Create Date:    		09:26:05 10/07/2015 
-- Design Name: 	 		SerialSensorDecoder
-- Module Name:    		OkStuff - Behavioral 
-- Project Name: 			ND
-- Target Devices: 		ND
-- Tool versions: 		ND
-- Description: 			Entity that manages the connection between USB and FIFO.
--	
-- Dependencies:			ND
--	
-- Revision:				ND 
-- Revision 				0.01 - File Created
-- Additional Comments: ND	
--
----------------------------------------------------------------------------------
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity Fifo is
	port (
		rd_clk		:	in 	STD_LOGIC;
		wr_clk		: 	in		STD_LOGIC;
		rst			:	in		STD_LOGIC;
		f_write		:	in		STD_LOGIC;
		f_read_A		:	in 	STD_LOGIC;
		f_read_B		:	in 	STD_LOGIC;
		f_count		: 	out 	STD_LOGIC_VECTOR(9 downto 0);
		dataSens		:	in		STD_LOGIC_VECTOR(31 downto 0);
		dataFifoA	:	out	STD_LOGIC_VECTOR(15 downto 0);
		dataFifoB	:	out	STD_LOGIC_VECTOR(15 downto 0)
	);
end Fifo;

architecture Structural of Fifo is

	--------------------
	-- Fifo Component --
	--------------------
	
	component fifoOut_1672
     port (
          wr_clk 			: IN 	STD_LOGIC;
			 rd_clk			: IN	STD_LOGIC;	
          rst 				: IN 	STD_LOGIC;
          din 				: IN 	STD_LOGIC_VECTOR(15 DOWNTO 0);
          wr_en			: IN 	STD_LOGIC;
          rd_en 			: IN 	STD_LOGIC;
          dout 			: OUT STD_LOGIC_VECTOR(15 DOWNTO 0);
			 wr_data_count : OUT STD_LOGIC_VECTOR(9 DOWNTO 0)
     );
	end component fifoOut_1672;
	
	signal dataSensA 	: STD_LOGIC_VECTOR(15 downto 0);
	signal dataSensB 	: STD_LOGIC_VECTOR(15 downto 0);
	
begin

	--------------------------
	-- Fifo Instantiation A --
	--------------------------
	fifoA 	: fifoOut_1672
		port map (			
			wr_clk 			=> wr_clk,
			rd_clk			=> rd_clk,
         rst				=> rst,
         din 				=> dataSensA,
         wr_en 			=> f_write,
         rd_en 			=> f_read_A,
         dout 				=> dataFifoA,
			wr_data_count	=> f_count
         --full 			=> fifo_full,
         --empty 		=> fifo_empty
		);
	
		--------------------------
		-- Fifo Instantiation B --
		--------------------------
		fifoB 	: fifoOut_1672
		port map (			
			wr_clk 			=> wr_clk,
			rd_clk			=> rd_clk,
         rst				=> rst,
         din 				=> dataSensB,
         wr_en 			=> f_write,
         rd_en 			=> f_read_B,
         dout 				=> dataFifoB
			--wr_data_count	=> f_count
         --full 			=> fifo_full,
         --empty 		=> fifo_empty
		);
		
		-- Big Part
		dataSensA <= dataSens(31 downto 16);
		-- Little Part
		dataSensB <= dataSens(15 downto 0);
end Structural;

