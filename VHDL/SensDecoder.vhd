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
-- Description: 			Entity that get the data from the sensor and decode it
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
use IEEE.std_logic_arith.all;
use IEEE.std_logic_misc.all;
use IEEE.std_logic_unsigned.all;
use IEEE.numeric_std.all;

entity SensDecoder is
	port (
		-- INS --
		clk			:	in		STD_LOGIC;
		in_ser		:	in		STD_LOGIC;	
		sigFromXem	: 	in		STD_LOGIC_VECTOR(2 downto 0);
		pcContWire	:	in		STD_LOGIC_VECTOR(15 downto 0);
		-- OUTS --
		dataSens		:	out	STD_LOGIC_VECTOR(31 downto 0);
		init_out		:	out	STD_LOGIC;
		dLoadAck		: 	out	STD_LOGIC;
		f_write		:	out	STD_LOGIC
	);
end SensDecoder;

architecture Structural of SensDecoder is
	
	type state is (
		idle, 
		scrivi1,
		scrivi0,
		contVal0,
		contVal1,
		fifoReady
	);
	
	type clkState is (
		idle, 
		trig_sig,
		cont,
		downAck
	);
	
	-- State Signal --
	signal st			:	state									:= idle;
	signal clkSt		: 	clkState								:= idle;
	
	-- Counters --
	signal cont_pix	:	STD_LOGIC_VECTOR(15 downto 0) := (others => '0');
	signal fifo_out	:  STD_LOGIC_VECTOR(15 downto 0)	:= (others => '0');
	-- Contatore 32 bit per star sicuri 
	signal cont_val	:	STD_LOGIC_VECTOR(31 downto 0)	:= (others => '0');
	signal time_cont	:	STD_LOGIC_VECTOR(23 downto 0) := (others => '0');
	signal pcContSig	: 	STD_LOGIC_VECTOR(15 downto 0) := (others => '0');
	
	signal da_idle		:	STD_LOGIC 							:= '1';
	signal init_sig	:	STD_LOGIC							:= '0';
	signal init_xem	:  STD_LOGIC							:= '0';
	signal pcDloadAck	:  STD_LOGIC							:= '0';
	
	signal reset		: STD_LOGIC;
	signal addCont		: STD_LOGIC;
	signal addFifo		: STD_LOGIC;

	
begin
	
	clkGen 	: process(clk)
	begin
		if rising_edge(clk)
		then
			if reset = '1'
			then
				-- Impostiamo il nuovo valore del pc_cont
				pcContSig <= pcContWire;
				-- Mettiamo a zero il segnale di out
				init_sig <= '0';
				-- Rimandiamo in idle, per aspettare un nuovo init
				clkSt <= idle;
			else
				case clkSt is
					----------
					-- idle --
					----------
					when idle 		=>
						if init_xem = '1' 
						then
							clkSt <= trig_sig;
						else
							clkSt <= idle;
						end if;
						
						-- Mandiamo a 0 pcDLoadAck
						pcDLoadAck <= '0';
					-------------
					-- trigSig --
					-------------
					when trig_sig 	=>
						init_sig <= '1'; -- 1
						clkSt <= cont;
					----------
					-- cont --
					----------
					when cont		=>
						-- Inviamo da PC il valore di quanti ms 
						-- vogliamo per ogni singolo trigger
						if pcContSig = STD_LOGIC_VECTOR(to_unsigned(0, 24))
						then
							-- Concludiamo il trigger di ingresso
							init_sig <= '0';
							-- Impostiamo nuovamente il valore di pc_cont
							pcContSig <= pcContWire;
							-- Inner Cont va a 0
							time_cont <= (others => '0');
							-- Mandiamo lo stato su downAck
							clkSt <= downAck;
						else 
							-- Per ogni pcContSig facciamo il conto dell'inner CLK
							if time_cont = STD_LOGIC_VECTOR(to_unsigned(100000,24))
							then
								pcContSig <= pcContSig - 1;
								time_cont <= (others => '0');
							else
								time_cont <= time_cont + 1;
							end if;
						end if;
					-------------
					-- downAck --
					-------------
					when downAck =>
							-- Attiviamo la richiesta di Download
							pcDLoadAck <= '1';
							clkSt <= idle;
					end case;
				end if;
		end if;
	end process;
	
	
	decodeProcess : process (clk)
	begin
		if rising_edge(clk) 
		then 
			case st is 
				----------
				-- idle --
				----------
				when idle =>
					-- Rimettiamo il flag da idle
					da_idle <= '1';
					cont_pix <= STD_LOGIC_VECTOR(to_unsigned(0, 16));
					
					if init_sig = '1' 
					then
						if in_ser = '1' then 
							st <= scrivi1;
						elsif in_ser = '0' then 
							st <= scrivi0;
						else
							st <= idle;
						end if;
					end if;
					
				-------------
				-- scrivi1 --
				-------------
				when scrivi1 =>
					if init_sig = '0' 
					then 
						st <= idle;
					elsif init_sig = '1'
					then
						da_idle <= '0';

						cont_pix <= cont_pix + 1;
						cont_val <= STD_LOGIC_VECTOR(to_unsigned(1,16));

						if in_ser = '1'
						then 
							st <= contVal1;
						elsif in_ser = '0'
						then 
							st <= scrivi0;
						end if;
					end if;
					
				-------------
				-- scrivi0 --
				-------------	
				when scrivi0 =>
					if init_sig = '0'
					then 	
						st <= idle;
					elsif init_sig = '1'
					then 
						da_idle <= '0';

						cont_pix <= cont_pix + 1;
						cont_val <= STD_LOGIC_VECTOR(to_unsigned(1,16));

						if in_ser = '0'
						then
							st <= contVal0;
						elsif in_ser = '1'
						then
							st <= scrivi1;
						end if;
					end if;
				
				---------------
				-- contaVal1 --
				---------------
				when contVal1 =>
					-- Controllo se il segnale di init e presente
					-- se non lo e' scarto i conteggi e mando in idle
					if init_sig = '1'
					then
						cont_val <= cont_val + 1;
						if in_ser = '1'
						then
							st <= contVal1; 
						elsif in_ser = '0'
						then	
							st <= scrivi0;
						end if;
					else
						-- Scarto i contatori e torno in idle
						cont_val <= (others => '0');
						st <= idle;
					end if;
				
				---------------
				-- contaVal0 --
				---------------
				when contVal0 =>
					-- Controllo se il segnale di init e presente
					-- se non lo e' scarto i conteggi e mando in idle
					if init_sig = '1'
					then
						cont_val <= cont_val + 1;
						if in_ser = '0' 
						then 
							st <= contVal0;
						elsif in_ser = '1' 
						then 
							st <= scrivi1;
						end if;
					else
						-- Scarto i contatori e torno in idle
						cont_val <= (others => '0');
						st <= idle;
					end if;
				
				------------
				-- others --
				------------
				when others =>
					st <= st;
			end case;
		end if;
	end process;
	
	init_xem	<=	sigFromXem(0);
	reset		<= sigFromXem(1);
	init_out	<= init_sig;

	
	dataSens <=
		cont_val when st = scrivi1 and da_idle = '0' else
		cont_val when st = scrivi0 and da_idle = '0' else
		(others => '0');

	f_write <=	
		'1' when st = scrivi1 and da_idle = '0' else
		'1' when st = scrivi0 and da_idle = '0' else
		'0';
		
	dLoadAck <= pcDLoadAck;

end Structural;

