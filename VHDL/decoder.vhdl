library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity SensDecoder is 
	port
	(
		
		clk 			: 	in 		std_logic;
		init_sig 		: 	in 		std_logic;
		in_ser			: 	in 		std_logic;
		fifo_write		: 	out 	std_logic
	);
end SensDecoder;

architecture behaviour of SensDecoder is 

	type   state		is 	(idle, scrivi1, scrivi0, contVal0, contVal1, fifoReady);

	signal cont_pix		: 	unsigned(7 downto 0)	:= to_unsigned(0, 8);
	signal fifo_out		: 	unsigned(7 downto 0)	:= to_unsigned(0,8);
	signal cont_val		: 	unsigned(7 downto 0)	:= x"00";
	signal st 				: 	state 					:= idle;

	signal da_idle			:	std_logic 				:= '1';

	signal dbg1				:	std_logic 				:= '0';


begin 	
	
	-- LOGIC PROCESS
	process (clk)
	begin
		if rising_edge(clk) then
			case st is 

				-- IDLE --
				when idle =>
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

				-- SCRIVI 1 --
				when scrivi1 =>
					if init_sig = '0' 
					then 
						st <= idle;
					elsif init_sig = '1'
					then
						da_idle <= '0';

						cont_pix <= cont_pix + 1;
						cont_val <= to_unsigned(1,8);

						if in_ser = '1'
						then 
							st <= contVal1;
						elsif in_ser = '0'
						then 
							st <= scrivi0;
						end if;
					end if;
					

				-- SCRIVI 0 --
				when scrivi0 =>
					if init_sig = '0'
					then 	
						st <= idle;
					elsif init_sig = '1'
					then 
						da_idle <= '0';

						cont_pix <= cont_pix + 1;
						cont_val <= to_unsigned(1,8);

						if in_ser = '0'
						then
							st <= contVal0;
						elsif in_ser = '1'
						then
							st <= scrivi1;
						end if;
					end if;

				-- CONTA VAL 1 --
				when contVal1 =>
					cont_val <= cont_val + 1;
					if in_ser = '1'
					then
						st <= contVal1; 
					elsif in_ser = '0'
					then	
						st <= scrivi0;
					end if;

				-- CONTA VAL 0 --
				when contVal0 =>
					cont_val <= cont_val + 1;
					if in_ser = '0' 
					then 
						st <= contVal0;
					elsif in_ser = '1' 
					then 
						st <= scrivi1;
					end if;
				-- OTHERS --
				when others =>
					st <= st;
			end case;
		end if;
	end process;

	-- SEQUENTIAL

	fifo_out <=
		cont_val when st = scrivi1 and da_idle = '0' else
		cont_val when st = scrivi0 and da_idle = '0' else
		(others => '0');

	fifo_write <=	
		'1' when st = scrivi1 and da_idle = '0' else
		'1' when st = scrivi0 and da_idle = '0' else
		'0';

end behaviour;