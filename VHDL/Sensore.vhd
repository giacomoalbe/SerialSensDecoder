----------------------------------------------------------------------------------
-- Company: 			FBK
-- Engineer: 			Giacomo Alberini
-- 
-- Create Date:    	15:56:21 10/07/2015 
-- Design Name: 		
-- Module Name:    	Sensore - Behavioral 
-- Project Name: 		SerialSensorDecoder
-- Target Devices:	XEM3001 
-- Tool versions: 
-- Description: 		Main module for the sensor decoder
--
-- Dependencies: 
--
-- Revision: 
-- Revision 			0.01 - File Created
--							1.00 - All the submodules are now working (FIFO, OK, DEMO_SENSOR)
--
----------------------------------------------------------------------------------
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.STD_LOGIC_arith.all;
use IEEE.STD_LOGIC_misc.all;
use IEEE.STD_LOGIC_unsigned.all;
use IEEE.numeric_std.all;

entity Sensore is
	port (
	
		clk 				:	in		STD_LOGIC;
		hi_in          :	in  	STD_LOGIC_VECTOR(7 downto 0);
      hi_out         : 	out 	STD_LOGIC_VECTOR(1 downto 0);
		hi_inout       : 	inout STD_LOGIC_VECTOR(15 downto 0);
		
		in_ser			:	in		STD_LOGIC;
		trig_out			:	out	STD_LOGIC;
      	
		leds 				: 	out	STD_LOGIC_VECTOR(7 downto 0)
	);
end Sensore;

architecture Structural of Sensore is
	
	-- Segnale uscita di Ok usato per lettura della PIPE
	signal ti_clk			: STD_LOGIC;
	
	signal reset 			: STD_LOGIC;
	signal fifoWrite		: STD_LOGIC;
	signal fifoReadA		: STD_LOGIC;
	signal fifoReadB		: STD_LOGIC;
	
	-- FIFO ==> PC
	signal fifoDataA		: STD_LOGIC_VECTOR(15 downto 0);
	signal fifoDataB		: STD_LOGIC_VECTOR(15 downto 0);
	
	-- SENSOR ==> FIFO
	signal sensData		: STD_LOGIC_VECTOR(31 downto 0);
	signal sensDataA		: STD_LOGIC_VECTOR(15 downto 0);
	signal sensDataB		: STD_LOGIC_VECTOR(15 downto 0);
	
	-- SENSOR ==> PC
	signal pcSig			: STD_LOGIC;
	
	-- PC ==> SENSOR
	signal pcContSignal	:	STD_LOGIC_VECTOR(15 downto 0);
	
	-- Contatore della FIFO
	signal dataCount		: STD_LOGIC_VECTOR(9 downto 0);
	
	-- Ctrl signals per il sensore dal PC
	signal sig2Sens		: STD_LOGIC_VECTOR(2 downto 0);
	
	--dbg 
	
	signal counter			: STD_LOGIC_VECTOR(23 downto 0) 	:= (others => '0');
	signal trig_sig		: STD_LOGIC 							:= '0';
	signal led_cont		: STD_LOGIC_VECTOR(7 downto 0) 	:= (others => '0');
	signal inner_cont		: STD_LOGIC_VECTOR(9 downto 0) 	:= (others => '0');
	
	-----------------
	-- Componenets --
	-----------------
	
	component OkStuff
		port (
			clk				: 	in		STD_LOGIC;
			ti_clk			: 	out 	STD_LOGIC;
			hi_in				: 	in		STD_LOGIC_VECTOR(7 downto 0);
			hi_out			:	out	STD_LOGIC_VECTOR(1 downto 0);
			hi_inout			: 	inout	STD_LOGIC_VECTOR(15 downto 0);
			dataReadFifoA	:	out 	STD_LOGIC;
			dataReadFifoB	:	out 	STD_LOGIC;
			dataFromFifoA	:	in		STD_LOGIC_VECTOR(15 downto 0);
			dataFromFifoB	:	in		STD_LOGIC_VECTOR(15 downto 0);
			fifoDataCount	: 	in		STD_LOGIC_VECTOR(9 downto 0);
			downToPc			:	in		STD_LOGIC;
			pcWireOut		:	out	STD_LOGIC_VECTOR(15 downto 0);
			sig2Xem			: 	out 	STD_LOGIC_VECTOR(2 downto 0)
		);
	end component;
	
	component Fifo
		port (
			wr_clk		: in	STD_LOGIC;
			rd_clk		: in 	STD_LOGIC;	
			rst 			: in 	STD_LOGIC;
			f_write		: in	STD_LOGIC;
			f_read_A		: in 	STD_LOGIC;
			f_read_B		: in 	STD_LOGIC;
			f_count		: out	STD_LOGIC_VECTOR(	9 downto 0);
			dataSens		: in  STD_LOGIC_VECTOR(31  downto 0);
			dataFifoA	: out STD_LOGIC_VECTOR(15 downto 0);
			dataFifoB	: out STD_LOGIC_VECTOR(15 downto 0)
		);
	end component Fifo;
	
	component SensDecoder 
		port (
			clk			:	in		STD_LOGIC;
			sigFromXem	:	in		STD_LOGIC_VECTOR(2 downto 0);
			in_ser		:	in		STD_LOGIC;
			pcContWire	: 	in		STD_LOGIC_VECTOR(15 downto 0);
			init_out		:	out	STD_LOGIC;
			dataSens		:	out	STD_LOGIC_VECTOR(31 downto 0);
			dLoadAck		:	out	STD_LOGIC;
			f_write		:	out	STD_LOGIC
		);
	end component SensDecoder;
	
begin
	-------------
	-- OkStuff --
	-------------
	okStuffComp	: OkStuff
		port map (
			ti_clk			=>	ti_clk,
			clk				=> clk,
			hi_in				=> hi_in, 
			hi_out			=> hi_out,
			hi_inout 		=> hi_inout,
			dataReadFifoA	=>	fifoReadA,
			dataReadFifoB	=> fifoReadB,
			dataFromFifoA	=>	fifoDataA,
			dataFromFifoB	=> fifoDataB,
			downToPc			=> pcSig,
			fifoDataCount  => dataCount,
			pcWireOut		=> pcContSignal,
			sig2Xem			=>	sig2Sens
		);
		
	----------
	-- Fifo --
	----------
	fifoInstance	: Fifo 
		port map (
			wr_clk			=> clk,
			rd_clk			=>	ti_clk,
			rst				=> reset, 
			f_write			=> fifoWrite,
			f_read_A			=> fifoReadA,
			f_read_B			=> fifoReadB,
			dataSens			=> sensData,
			f_count			=>	dataCount,
			dataFifoA		=>	fifoDataA,
			dataFifoB		=>	fifoDataB
		);
	
	-----------------
	-- SensDecoder --
	-----------------
	SeDc	: SensDecoder 
		port map (
			clk				=> clk,
			sigFromXem		=> sig2Sens,
			in_ser			=>	in_ser,
			pcContWire		=> pcContSignal,
			init_out			=>	trig_out,
			f_write			=> fifoWrite,
			dLoadAck			=> pcSig,
			dataSens			=>	sensData
		);
	
	-----------------
	-- CTRL && DBG --
	-----------------
	-- This reset is asserted in the moment of a new acquisition
	-- so if you don't take data, you lose 'em all!
	reset 	<= sig2Sens(0);
	leds		<= "1111111" & not pcSig;

end Structural;

