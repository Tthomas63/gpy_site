-- This module holds any type of remote execution functions (IE, 'dangerous')
local CATEGORY_NAME = "G-Py ULX"

function ulx.gpy_send_data( calling_ply, url, key )
	ulx_players = {}
	my_url = "https://gpy-gpy.herokuapp.com/key"
    my_fetched_headers = {}
    -- Http fetch to grab headers ---------------------
    http.Fetch(
        my_url,
        function( body, len, headers, code )
            -- The first argument is the HTML we asked for.
            TheReturnedHTML = body
            my_fetched_headers = headers
            print("Response code is: "..code)
        end,
        function( error )
            -- We failed. =(
        end
    )
    -- Http Post to send data --------------------------
	for steamid, table in pairs(ULib.ucl.users) do
		for attr, value in pairs(table) do
			ulx_players[steamid] = table['group']
		end
	end
	local json_ulx_players = util.TableToJSON(ulx_players)
	key = "3f440c72-cfcc-480c-981a-d1e474ad63e6"
	params = { ulx_secret_key = key,
			   ulx_ranks = json_ulx_players, }
	http.Post( my_url,
        params,
        function( result )
	        if result then
                print( "Done!" ) end
	        end,
        function( failed )
	        print( failed )
	    end,
        my_fetched_headers )
	ulx.fancyLogAdmin( calling_ply, true, "#A ran gpy_send_data command: #s", command )
end
local gpy_send_data = ulx.command( CATEGORY_NAME, "ulx gpy_send_data", ulx.gpy_send_data, "!gpy_send_data", true, false, true )
gpy_send_data:defaultAccess( ULib.ACCESS_SUPERADMIN )
gpy_send_data:help( "Send data to a G-Py Site instance." )
