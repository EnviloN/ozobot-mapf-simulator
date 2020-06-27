# ESO-OzoNav Prototype

## Set-up
1. *Optional* - Use Python virtual environment:
    - `python3 -m venv .env` - Create a new python virtual environment
    - `source .env/bin/activate` - Activate the virtual environment (to install packages and run Python code)
    - `deactivate` - Deactivate the active virtual environment when done
2. Install required packages (only **pygame**):
    - `pip3 install -r requirements.txt`
3. Build the **boOX** program:
    - `cd ../boox/boOX-y/` - Go to *boox* folder
    - `make` - Build the program
    - Check and configure the path to the program in `./resources/config/simulation.ini` (also see section *Simulator Configuration*)
4. *Optional* - Configure screen parameters:
    - Modify or add screen configuration in `./resources/config/display/`

## Simulator Configuration
The simulation is configurable and all the configurable parameters can be found in is in `./resources/config/simulation.ini`. 

### Section [ozobots]
Configuration of outputs for Ozobot robots.
- `line_width` - Width of the following line in millimeters
- `wall_width` - Width of the wall line in millimeters
- `tile_border_width` - Width of the tile border line in millimeters
- `tile_size` - Size of the tile in millimeters
- `color_code_radius` - Radius of the Color Code circle in millimeters
- `intersection_width` - Width of the intersection indicator for colored paths


### Section [solver]
Path to the boOX main folder, where the executables are. Also selection of solver and algorithm.
- `path` - Path to the boOX `src/main` folder, where the solver executables are. 
- `solver` - Specified solver (`mapf_solver_boOX` or `rota_solver_boOX`)
- `algorithm` - Algorithm used for solving (One from: `cbs`, `cbs+`, `cbs++`, `smtcbs`, `smtcbs+`, `smtcbs++`)

### Section [simulator]
Configuration of the simulation animations.
- `agent_type` - Agent type implementation. Can be:
    - `dummy` - Full path (ESO-OzoNav 0)
    - `animated` - Animated path with sharp turns (ESO-OzoNav 1)
    - `ozobot` - Animated paths with curved turns, Color Codes, and ability to be colored (ESO-OzoNav 2 & 3)
- `step_time` - Time in milliseconds that should take Ozobot to go between tiles
- `tail_lag` - Time lag of the tail (effectively its length)
- `display_borders` - Flag, if tile borders should be displayed
- `display_walls` - Flag, if walls should be displayed
- `direction_preview` - Flag, if direction arrow indicator should be displayed
- `colors` - Flag, if the paths should be colored (Only for `ozobot` agent implementation, also displays intersection indicators)

## Command-line arguments
- `-m <map_file>`, `--map <map_file>` - (required) relative path to the map file from `./resources/maps/`
- `-c <cfg_file>`, `--config-file <cfg_file>` - (required) relative path to the display configuration file from `./resources/config/simulation.ini`
- `-ma <w h a>`, `--map-attributes <w h a>` - (required if attributes are not in the map name) map attributes [width, height, number of agents] 
- `-r <w h>`, `--resolution <w h>` - Resolution of the application window [default: `1920 1080`]
- `-f`, `--full-screen` - Starts application in full-screen (ignores `-r <w h>` if used)
- `-e`, `--editor` - Runs map editor instead of simulator
- `-d`, `--debug` - Runs debug mode (more logging in `./resources/logs/log.log`)

## Usage
Go to the `./resources/ozobotmapf` folder and run the program with `python3`.

### Map editor
Use `python3 ozonav.py -e -c <cfg_file> [optional_arguments]` to start the map editor mode.

### Simulator
Use `python3 ozonav.py -c <cfg_file> -m <map_file> [optional_arguments]` to start the map editor mode.
