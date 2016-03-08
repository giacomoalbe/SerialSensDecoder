----------------------------------------------------------------------------------
-- Company: 			FBK
-- Engineer: 			Giacomo Alberini
-- 
-- Create Date:    	15:56:21 10/07/2015 
-- Design Name: 		
-- Module Name:    	OkStuff - Structural 
-- Project Name: 		SerialSensorDecoder
-- Target Devices:	XEM3001 
-- Tool versions: 
-- Description: 		Entity taht manages the connection of the XEM to PC
--
-- Dependencies: 		OpalKelly
--					
----------------------------------------------------------------------------------
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.std_logic_arith.all;
use IEEE.std_logic_misc.all;
use IEEE.std_logic_unsigned.all;



library OpalKelly;
use OpalKelly.frontpanel.all;

entity OkStuff is
	port (
		-- OK --
		ti_clk 			:	out	STD_LOGIC;
		hi_in          :	in  	STD_LOGIC_VECTOR(7 downto 0);
      hi_out         : 	out 	STD_LOGIC_VECTOR(1 downto 0);
      hi_inout       : 	inout STD_LOGIC_VECTOR(15 downto 0);
		-- OTHER __
		clk 				:	in		STD_LOGIC;
		downToPc			: 	in		STD_LOGIC;	
		dataFromFifoA	: 	in		STD_LOGIC_VECTOR(15 downto 0);
		dataFromFifoB	: 	in		STD_LOGIC_VECTOR(15 downto 0);
		fifoDataCount	: 	in		STD_LOGIC_VECTOR(9 downto 0);
		dataReadFifoA	:	out 	STD_LOGIC;
		dataReadFifoB	:	out 	STD_LOGIC;
		pcWireOut 		:	out	STD_LOGIC_VECTOR(15 downto 0);
		sig2Xem			: 	out	STD_LOGIC_VECTOR(2 downto 0)
		);
end OkStuff;

architecture Structural of OkStuff is
	
	-- Segnali necessari per OK
	signal ok1        		: 	STD_LOGIC_VECTOR(30 downto 0);
   signal ok2        		: 	STD_LOGIC_VECTOR(17-1 downto 0);
   signal ok2s       		: 	STD_LOGIC_VECTOR(17*4-1 downto 0);

	-- Ctrl from PC
	signal trigFromPC			: 	STD_LOGIC_VECTOR(15 downto 0);
	
	-- Ctrl to PC
	signal sigToPC				: 	STD_LOGIC_VECTOR(15 downto 0);
	signal dLoadAck			: 	STD_LOGIC 				:= '0';
	signal fifoDataCountExp :	STD_LOGIC_VECTOR(15 downto 0);
	
	-- Data from PC
	signal pcContWire			:	STD_LOGIC_VECTOR(15 downto 0);
	
begin

	------------
	-- OkHost --
	------------
	okHI: okHost
   port map (
      hi_in    => hi_in,
      hi_out   => hi_out,
      hi_inout => hi_inout,
      ti_clk   => ti_clk,
      ok1      => ok1,
      ok2      => ok2
   ); 
	
	--------------
	-- OkWireOR --
	--------------
	okWO: okWireOR
   generic map (
		-- Solo 1 oggetto deve scrivere verso PC, ovvero PipeOut
      N           => 4
   )
   port map (
      ok2         => ok2,
      ok2s        => ok2s
   );
	
	---------------
	-- pcAckWire --
	---------------
	pcAckWire: okWireOut
		port map (
			ok1			=>	ok1,
			ok2			=>	ok2s(17*4-1 downto 3*17),
			ep_addr		=>	x"20",
			ep_datain	=> sigToPC
		);
	
	---------------
	-- fifoCount --
	---------------
	fifoCount: okWireOut
		port map (
			ok1			=>	ok1,
			ok2			=>	ok2s(17*3-1 downto 2*17),
			ep_addr		=>	x"21",
			ep_datain	=> fifoDataCountExp
		);
	
	-----------------
	-- OkPipeOUT-A --
	-----------------
	OkPOA	:	okPipeOut
		port map (
			ok1			=>	ok1,	
			ok2			=>	ok2s(17*2-1 downto 17*1),
			ep_addr		=> x"A0",
			ep_datain	=>	dataFromFifoA,
			ep_read		=> dataReadFifoA
	);
	
	-----------------
	-- OkPipeOUT-B --
	-----------------
	OkPOB	:	okPipeOut
		port map (
			ok1			=>	ok1,	
			ok2			=>	ok2s(17*1-1 downto 17*0),
			ep_addr		=> x"A1",
			ep_datain	=>	dataFromFifoB,
			ep_read		=> dataReadFifoB
	);
	
	--------------
	-- OkWireIN --
	--------------
	okWireIn: okWireIn
		port map (
			ok1			=>	ok1,
			ep_addr		=>	x"03",
			ep_dataout	=> pcContWire
		);
	

	
	---------------
	-- OkTrigIN ---
	---------------
	okTrigIn: okTriggerIn
   port map (
      ok1            => ok1,
      ep_addr        => x"40",
      ep_clk         => clk,
      ep_trigger     => trigFromPC
   );
	

	process (clk) 
	begin
		if rising_edge(clk)
		then
			if trigFromPC(0) = '1'
			then
				-- Init della foto --
				sig2Xem <= "001";
			elsif trigFromPC(1) = '1'
			then
				-- Cambiamo il valore del contatore --
				sig2Xem <= "010";
			elsif trigFromPC(2) = '1'
			then
				-- Reset del downAck --
				dLoadAck <= '0';
			else
				sig2Xem <= (others => '0');
			end if;
			
			-- DownToPC Handling --
			if downToPc = '1' 
			then
				-- Mettiamo a 1 il wire di 
				-- richiesta di download
				-- Questo valore 
				dLoadAck <= '1';
			end if;
		end if;
	end process;

sigToPC 				<= "000000000000000" & dLoadAck;
fifoDataCountExp 	<= "000000" & fifoDataCount(9 downto 0);

-- Out il cont da PC
pcWireOut <= pcContWire;
	
end Structural;

