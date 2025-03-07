# Badge Platform Eva - hardware platform v3.0
# (2022-2024) Voor m'n lieve guppie
#
# comms.py : v1.0-refactor 0.0.0

import time
import badger2040
import badger_os
import os
from machine import UART
from machine import Pin

# 2. Logger class and initialization
class SimpleLogger:
    LEVELS = {
        'DEBUG': 10,
        'INFO': 20,
        'WARNING': 30,
        'ERROR': 40,
        'CRITICAL': 50
    }

    def __init__(self, name, log_file='badge_debug.log', console_level='INFO', file_level='DEBUG'):
        self.name = name
        self.log_file = log_file
        self.console_level = self.LEVELS.get(console_level, 20)
        self.file_level = self.LEVELS.get(file_level, 10)

    def _write_to_file(self, message):
        try:
            with open(self.log_file, 'a') as f:
                f.write(message + '\n')
        except Exception as e:
            print(f"Error writing to log file: {e}")

    def _log(self, level, message):
        timestamp = time.time()
        log_message = f"{timestamp} - {self.name} - {level} - {message}"
        
        # Console output
        if self.LEVELS.get(level, 0) >= self.console_level:
            print(log_message)
        
        # File output
        if self.LEVELS.get(level, 0) >= self.file_level:
            self._write_to_file(log_message)

    def debug(self, message):
        self._log('DEBUG', message)

    def info(self, message):
        self._log('INFO', message)

    def warning(self, message):
        self._log('WARNING', message)

    def error(self, message):
        self._log('ERROR', message)

    def critical(self, message):
        self._log('CRITICAL', message)

# Initialize logger before it's used by any other code
logger = SimpleLogger('badge_papa')

# 3. Constants
WIDTH = badger2040.WIDTH
HEIGHT = badger2040.HEIGHT
LEFT_PADDING = 5
BUTTON_PRESS_DELAY = 0.2
MENU_FONT_SIZE = 0.5
MENU_REGION = (0, 30, WIDTH, HEIGHT - 40)
STATUS_REGION = (0, HEIGHT // 2 - 15, WIDTH, 30)
BUTTON_REGION = (0, HEIGHT - 20, WIDTH, 20)

# 4. State Management Classes
class DisplayStates:
    MAIN_SCREEN = "main"
    MESSAGE_MENU = "menu"
    SENDING = "sending"
    DOWNLINK = "downlink"

class SystemMonitor:
    def __init__(self):
        self.metrics = {
            'message_sends': 0,
            'failed_sends': 0,
            'downlink_checks': 0,
            'state_changes': 0,
            'errors': []
        }
        self.max_stored_errors = 10
        logger.info("System monitor initialized")

    def log_metric(self, metric_name, value=1):
        if metric_name in self.metrics:
            self.metrics[metric_name] += value
            logger.debug(f"Metric {metric_name}: {self.metrics[metric_name]}")
        
    def log_error(self, error_message):
        timestamp = time.time()
        error_entry = (timestamp, error_message)
        self.metrics['errors'].append(error_entry)
        if len(self.metrics['errors']) > self.max_stored_errors:
            self.metrics['errors'].pop(0)
        logger.error(f"Error logged: {error_message}")

    def get_health_report(self):
        total_sends = self.metrics['message_sends']
        success_rate = 0 if total_sends == 0 else (
            (total_sends - self.metrics['failed_sends']) / total_sends
        )
        report = {
            'success_rate': success_rate,
            'total_operations': total_sends,
            'downlink_checks': self.metrics['downlink_checks'],
            'recent_errors': self.metrics['errors'][-5:]
        }
        logger.debug(f"Health report generated: {report}")
        return report

class BadgeState:
    def __init__(self):
        self.current_state = DisplayStates.MAIN_SCREEN
        self.selected_message = None
        self.selected_identifier = None
        self.is_downlink_displayed = False
        self.selected_index = 0
        logger.info("Badge state initialized")

    def transition_to(self, new_state):
        logger.debug(f"State transition: {self.current_state} -> {new_state}")
        self.current_state = new_state
        system_monitor.log_metric('state_changes')

    def select_message(self, message, identifier):
        self.selected_message = message
        self.selected_identifier = identifier
        logger.info(f"Message selected: {message} with ID: {identifier}")

# 5. Initialize system monitor and badge state
system_monitor = SystemMonitor()
badge_state = BadgeState()

# 6. Initialize hardware
display = badger2040.Badger2040()
display.led(128)
display.update_speed(badger2040.UPDATE_NORMAL)

lora = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

# Global Variables for messages
messages = []
message_identifiers = ["AA", "BB", "CC", "DD", "EE"]  # Two-letter identifiers for each message
current_message_index = 0
current_downlink_message = None
selected_message_index = 0
is_menu_active = False
is_downlink_displayed = False  # Track if downlink message is being displayed
selected_message = None  # Variable to store the selected message
selected_identifier = None  # Variable to store the identifier to be sent

# Add these constants at the top with other constants
MENU_REGION = (0, 30, WIDTH, HEIGHT - 40)  # Region for menu items
STATUS_REGION = (0, HEIGHT // 2 - 15, WIDTH, 30)  # Region for status messages
BUTTON_REGION = (0, HEIGHT - 20, WIDTH, 20)  # Region for button labels

# ------------------------------
#      Display Functions
# ------------------------------

def is_on_battery():
    return not os.uname().machine.startswith("USB")

def turn_on_led():
    display.led(128)  # Set LED brightness to mid-level

def turn_off_led():
    display.led(0)    # Turn off the LED

def fit_text(text, max_width, min_size=0.5, max_size=2.0):
    """Adjusts the font size so the text fits within max_width."""
    size = max_size
    while size >= min_size:
        if display.measure_text(text, size) <= max_width:
            return size
        size -= 0.1
    return min_size

def bytes_to_hex(b):
    """Convert bytes or string to hex string for MicroPython"""
    if isinstance(b, str):
        b = b.encode('utf-8')
    return ''.join('{:02x}'.format(x) for x in b)

def display_message(message):
    display.pen(15)
    display.clear()
    display.pen(0)
    display.font("sans")
    display.thickness(2)
    size = fit_text(message, WIDTH - 2 * LEFT_PADDING)
    display.text(message, LEFT_PADDING, HEIGHT // 2, size)
    display.update()

def display_main_screen():
    """Display the main screen"""
    display.update_speed(badger2040.UPDATE_NORMAL)
    display.pen(15)
    display.clear()
    display.pen(0)
    display.font("sans")
    
    # Draw title
    display.thickness(3)
    display.text("COMMS", LEFT_PADDING, 25, 1.8)
    
    # Display last sent message status if exists
    y_position = 50
    if selected_message:
        display.thickness(1)
        display.text("Sent:", LEFT_PADDING, y_position, 0.5)
        
        # Show the message details
        preview_text = f"{selected_identifier}: {selected_message}"
        size = fit_text(preview_text, WIDTH - 2 * LEFT_PADDING - 40, min_size=0.4, max_size=0.5)
        display.text(preview_text, LEFT_PADDING + 40, y_position, size)
        y_position += 30  # Space for separator line
    
    # Draw separator line if we have messages to separate
    if selected_message and current_downlink_message:
        display.thickness(1)
        display.line(LEFT_PADDING, y_position - 10, WIDTH - LEFT_PADDING, y_position - 10)
    
    # Display received message if exists
    if current_downlink_message:
        display.thickness(1)
        display.text("Received:", LEFT_PADDING, y_position, 0.5)
        
        size = fit_text(current_downlink_message, WIDTH - 2 * LEFT_PADDING - 40, min_size=0.4, max_size=0.5)
        display.text(current_downlink_message, LEFT_PADDING + 65, y_position, size)
    
    # Draw button labels
    display.thickness(1)
    display.text("Check", WIDTH // 2 - 20, HEIGHT - 10, 0.5)
    display.text("Choose", WIDTH - 55, HEIGHT - 10, 0.5)
    
    display.update()
    turn_off_led()

def show_message_menu():
    """Display the message menu"""
    logger.debug(f"Showing menu - Current selection: {badge_state.selected_index}")
    
    display.update_speed(badger2040.UPDATE_FAST)
    display.pen(15)
    display.clear()
    display.pen(0)
    display.font("sans")
    
    # Draw title - higher up to avoid overlap
    display.thickness(2)
    display.text("Select Message", LEFT_PADDING, 10, 0.7)
    
    # Draw messages with proper spacing
    y_position = 35
    for i, message in enumerate(messages):
        menu_text = f"{message_identifiers[i]}: {message}"
        if i == badge_state.selected_index:
            display.pen(0)
            display.rectangle(0, y_position - 4, WIDTH, 13)
            display.pen(15)
            display.text(menu_text, LEFT_PADDING + 5, y_position, MENU_FONT_SIZE)
        else:
            display.pen(0)
            display.text(menu_text, LEFT_PADDING + 5, y_position, MENU_FONT_SIZE)
        y_position += 17
    
    # Update button labels - changed Info to Back
    display.pen(0)
    display.thickness(1)
    display.text("Back", LEFT_PADDING + 24, HEIGHT - 10, 0.5)
    display.text("Send", WIDTH - 45, HEIGHT - 10, 0.5)
    
    display.update()
    turn_off_led()

def display_downlink_message(message):
    """Display the downlink message with Return button."""
    display.pen(15)
    display.clear()
    display.pen(0)
    display.font("sans")
    display.thickness(2)
    size = fit_text(message, WIDTH - 2 * LEFT_PADDING)
    display.text(message, LEFT_PADDING, HEIGHT // 2 - 5, size)
    display.text("Return", WIDTH // 2 - 20, HEIGHT - 10, 0.5)
    display.update()

# ------------------------------
#        Sigfox functions
# ------------------------------

class SigfoxCommands:
    RESET_CHANNELS = "AT$RC"
    SEND_FRAME = "AT$SF"
    GET_ID = "AT$I=10"
    GET_TEMP = "AT$T?"
    GET_RX_FREQ = "AT$DR?"
    GET_TX_FREQ = "AT$IF?"
    DOWNLINK = "AT$DR=1"

class SigfoxComm:
    # Update expected responses to include error cases
    EXPECTED_RESPONSES = {
        'AT': 'OK',
        'AT$RC': {'format': r'(OK|ERR_SET_STD_CONFIG_SET)', 'example': 'OK'},  # Accept both responses
        'AT$SF': 'OK',
        'AT$QS?': {'format': r'(ERROR: parse error|-?\d+)', 'example': '-90'},  # Accept error or dBm value
        'AT$I=10': {'format': r'[0-9A-F]{6,8}', 'example': '003B4028'},
        'AT$I=11': {'format': r'[0-9A-F]{8,16}', 'example': '42F122345ABC9876'},
        'AT$T?': {'format': r'\d{1,3}', 'example': '197'},  # Raw temp value before conversion
    }

    def __init__(self, uart, logger):
        self.uart = uart
        self.logger = logger
        # Add initialization status
        self.initialized = False
        try:
            self._init_device()
            self.initialized = True
        except Exception as e:
            self.logger.error(f"Failed to initialize Sigfox: {e}")

    def _init_device(self):
        """Initialize and check Sigfox device status"""
        self.logger.debug("Starting Sigfox device initialization...")
        
        # Add delay for device initialization
        time.sleep(1)
        
        # Test basic AT command first
        at_response = self._send_command("AT")
        if not at_response:
            raise Exception("Device not responding to AT command")
        self.logger.debug(f"AT command response: {at_response}")
            
        # Get device ID (required)
        device_id = self._send_command(SigfoxCommands.GET_ID)
        if not device_id:
            raise Exception("Could not get device ID")
        self.logger.info(f"Sigfox Device ID: {device_id}")
        
        # Check temperature (optional)
        temp = self._send_command("AT$T?")
        if temp:
            self.logger.debug(f"Raw temperature response: {temp}")
            converted_temp = self._convert_raw_temperature(temp)
            if converted_temp is not None:
                self.logger.info(f"Device temperature: {converted_temp:.1f}°C")
            else:
                self.logger.warning(f"Could not interpret temperature: {temp}")
        
        # Check signal quality (optional)
        signal = self._send_command("AT$QS?")
        if signal and "ERROR" not in signal:
            try:
                signal_dbm = int(signal)
                quality = self._interpret_signal_quality(signal_dbm)
                self.logger.info(f"Signal quality: {signal_dbm} dBm ({quality})")
            except ValueError:
                self.logger.debug(f"Could not parse signal quality: {signal}")

        self.logger.info("Device initialization completed")

    def _validate_response(self, command, response):
        """Validate response format and provide detailed error info"""
        if not response:
            self.logger.error(f"No response received for command: {command}")
            return False

        # Strip command to base form for matching
        base_command = command.split('=')[0] if '=' in command else command
        
        if base_command in self.EXPECTED_RESPONSES:
            expected = self.EXPECTED_RESPONSES[base_command]
            if isinstance(expected, str):
                if expected not in response:
                    self.logger.warning(f"Unexpected response for {command} - Got: '{response}', Expected: '{expected}'")
                    return True  # More lenient validation
            elif isinstance(expected, dict):
                import re
                pattern = expected['format']
                if re.match(pattern, response):
                    # Valid response, convert temperature if it's a temp command
                    if base_command == 'AT$T?':
                        temp = int(response)
                        converted = (temp - 128) / 2
                        self.logger.debug(f"Temperature: raw={temp}, converted={converted}°C")
                    return True
                else:
                    self.logger.warning(f"Response format mismatch for {command} - Got: '{response}'")
                    return True  # More lenient validation
        return True

    def _send_command(self, command, read_size=64, timeout=2):
        """Send AT command and read response with detailed logging"""
        # Use longer timeout for send frame commands
        if command.startswith(SigfoxCommands.SEND_FRAME):
            timeout = 12  # Give more time for transmission
            self.logger.debug(f"Using extended timeout ({timeout}s) for send frame")
        
        self.logger.debug(f"Sending command: {command}")
        
        try:
            # Clear any pending data
            pending_data = []
            while self.uart.any():
                data = self.uart.read()
                if data:
                    pending_data.append(data)
                    self.logger.debug(f"Cleared pending data: {data}, Hex: {bytes_to_hex(data)}")
            
            # Send command
            full_command = f"{command}\r\n"
            bytes_written = self.uart.write(full_command)
            self.logger.debug(f"Command sent - ASCII: {full_command.strip()}")
            self.logger.debug(f"Command hex: {bytes_to_hex(full_command.encode())}")
            self.logger.debug(f"Bytes written: {bytes_written}")
            
            # Wait for response with detailed timing
            start_time = time.time()
            response = bytearray()
            
            while (time.time() - start_time) < timeout:
                if self.uart.any():
                    chunk = self.uart.read(read_size)
                    if chunk:
                        response.extend(chunk)
                        self.logger.debug(f"Received chunk at {time.time() - start_time:.1f}s:")
                        self.logger.debug(f"  ASCII: {chunk}")
                        self.logger.debug(f"  Hex: {bytes_to_hex(chunk)}")
                        self.logger.debug(f"  Bytes: {list(chunk)}")
                    if b'\r\n' in response:
                        self.logger.debug("Found end of response")
                        break
                time.sleep(0.1)
            
            if response:
                try:
                    decoded = response.decode().strip()
                    self.logger.debug("Final response:")
                    self.logger.debug(f"  Decoded: {decoded}")
                    self.logger.debug(f"  Raw bytes: {response}")
                    self.logger.debug(f"  Hex: {bytes_to_hex(response)}")
                    
                    if self._validate_response(command, decoded):
                        return decoded
                    return None
                    
                except UnicodeDecodeError as e:
                    self.logger.error(f"Failed to decode response: {str(e)}")
                    self.logger.error(f"Raw bytes: {response}")
                    self.logger.error(f"Hex: {bytes_to_hex(response)}")
                    return None
            else:
                self.logger.warning(f"No response after {timeout}s")
                self.logger.debug(f"Command was: {command}")
                return None
                
        except Exception as e:
            self.logger.error(f"Command failed: {command}")
            self.logger.error(f"Error type: {type(e).__name__}")
            self.logger.error(f"Details: {str(e)}")
            return None

    def send_message(self, identifier):
        if not self.initialized:
            self.logger.error("Sigfox not properly initialized")
            return False
        
        try:
            msg_id = int(identifier)
            msg_type = "HELP" if msg_id <= 3 else "INFO"
            
            # Format payload with detailed logging
            id_bytes = bytes([msg_id])
            type_bytes = msg_type.encode()
            msgid_bytes = bytes([msg_id])
            
            self.logger.debug("Payload components:")
            self.logger.debug(f"  ID bytes: {id_bytes}, hex: {bytes_to_hex(id_bytes)}")
            self.logger.debug(f"  Type bytes: {type_bytes}, hex: {bytes_to_hex(type_bytes)}")
            self.logger.debug(f"  MsgID bytes: {msgid_bytes}, hex: {bytes_to_hex(msgid_bytes)}")
            
            payload = bytes_to_hex(id_bytes + type_bytes + msgid_bytes)
            self.logger.debug(f"Combined payload: {payload}")
            self.logger.debug(f"Payload length: {len(payload)} chars")
            
            command = f"{SigfoxCommands.SEND_FRAME}={payload}"
            self.logger.debug(f"Starting transmission (this can take up to 6 seconds)")
            self.logger.debug(f"Full command: {command}")
            
            response = self._send_command(command, timeout=12)
            self.logger.debug(f"Transmission complete, response: {response}")
            
            if response is None:
                self.logger.warning("No response - module likely busy with successful transmission")
                return "UNKNOWN"
            elif "OK" in response:
                self.logger.info("Message confirmed sent")
                return True
            else:
                self.logger.error(f"Send failed with response: {response}")
                return False
            
        except Exception as e:
            self.logger.error(f"Error sending message: {str(e)}")
            self.logger.error(f"Stack trace: ", exc_info=True)
            return False

    def check_downlink(self):
        """Check for downlink messages with proper error handling"""
        self.logger.debug("Checking downlink messages")
        
        response = self._send_command(SigfoxCommands.DOWNLINK, timeout=6)
        
        if not response:
            self.logger.error("No downlink response")
            return None
            
        if response in ["OK", "OK OK"]:
            self.logger.info("No new downlink messages")
            return None
            
        self.logger.info(f"Received downlink message: {response}")
        return response

    def _convert_raw_temperature(self, raw_temp):
        """Convert raw temperature value to actual Celsius"""
        try:
            temp = int(raw_temp)
            # Based on common Sigfox module temperature conversion
            return (temp - 128) / 2
        except ValueError:
            self.logger.error(f"Could not convert temperature value: {raw_temp}")
            return None

    def _interpret_signal_quality(self, dbm):
        """Interpret signal quality from dBm value"""
        try:
            dbm = int(dbm)
            if dbm >= -90: return "Excellent"
            elif dbm >= -100: return "Good"
            elif dbm >= -110: return "Fair"
            else: return "Poor"
        except ValueError:
            return "Unknown"

    def _log_transmission_stats(self, identifier, rssi=None, freq=None):
        """Log detailed transmission statistics"""
        stats = {
            'timestamp': time.time(),
            'message_id': identifier,
            'rssi': rssi,
            'frequency': freq,
            'retries': self.metrics.get('retries', 0)
        }
        self.logger.info("Transmission stats: {}".format(stats))

# Initialize Sigfox communication
sigfox = SigfoxComm(lora, logger)

def send_predefined_message():
    global selected_identifier
    logger.debug(f"Starting message send. Selected ID: {selected_identifier}")
    try:
        turn_on_led()
        if selected_identifier is None:
            logger.error("No message selected to send.")
            display_message("No Message Selected")
            return

        result = sigfox.send_message(selected_identifier)
        if result is True:
            display_message("Message Sent")
            system_monitor.log_metric('message_sends')
        elif result == "UNKNOWN":
            display_message("Message Status Unknown")
            system_monitor.log_metric('message_sends')  # Still count it as we see it in emails
        else:
            display_message("Send Failed")
            system_monitor.log_metric('failed_sends')
            
    except Exception as e:
        logger.error(f"Error sending message: {str(e)}")
        display_message("Error Sending")
        system_monitor.log_metric('failed_sends')
    finally:
        turn_off_led()

def check_downlink_message():
    global current_downlink_message, is_downlink_displayed
    try:
        turn_on_led()  # LED indicates checking activity
        
        response = sigfox.check_downlink()
        system_monitor.log_metric('downlink_checks')
        
        if response:
            # Store the received message and update display
            current_downlink_message = response
            display_message("Message Received")
            time.sleep(1)
            display_main_screen()
        else:
            display_message("No New Messages")
            time.sleep(2)
            display_main_screen()
            
    except Exception as e:
        logger.error(f"Error in downlink check: {str(e)}")
        display_message("Error Checking")
        time.sleep(2)
        display_main_screen()
        system_monitor.log_metric('errors')
    finally:
        turn_off_led()

def select_message():
    """Select message and return directly to main screen"""
    global selected_message, selected_identifier
    selected_message = messages[badge_state.selected_index]
    selected_identifier = message_identifiers[badge_state.selected_index]
    logger.info(f"Selected message: {selected_message} with identifier {selected_identifier}")
    badge_state.select_message(selected_message, selected_identifier)
    # Remove the intermediate display and go straight to main screen
    badge_state.transition_to(DisplayStates.MAIN_SCREEN)
    display_main_screen()

# ------------------------------
#        Program setup
# ------------------------------

# Load messages from comms.txt
try:
    with open("comms.txt", "r") as f:
        messages = [line.strip() for line in f.readlines() if line.strip()]
except OSError:
    print("Failed to read comms.txt file")
    messages = ["Message 1", "Message 2", "Message 3", "Message 4", "Message 5"]  # Default messages

# Generate numerical identifiers (01, 02, etc.) based on number of messages
message_identifiers = [f"{i+1:02d}" for i in range(len(messages))]  # Creates ["01", "02", "03", etc.]

# Draw the main screen initially
display_main_screen()

# ------------------------------
#       Main program
# ------------------------------

# Add this helper function for button debugging
def check_button_state():
    """Debug helper to check all button states"""
    button_states = {
        "UP": display.pressed(badger2040.BUTTON_UP),
        "DOWN": display.pressed(badger2040.BUTTON_DOWN),
        "A": display.pressed(badger2040.BUTTON_A),
        "B": display.pressed(badger2040.BUTTON_B),
        "C": display.pressed(badger2040.BUTTON_C)
    }
    
    for button, state in button_states.items():
        if state:
            print(f"DEBUG: {button} button is pressed")  # Use print for immediate feedback
            logger.debug(f"{button} button state: pressed")
    return button_states

# Update the main loop to use state management
while True:
    # Check button states at the start of each loop
    button_states = check_button_state()

    if badge_state.current_state == DisplayStates.DOWNLINK:
        if button_states["B"]:
            logger.debug("Button B pressed - clearing downlink message")
            badge_state.transition_to(DisplayStates.MAIN_SCREEN)
            is_downlink_displayed = False
            display_main_screen()
            time.sleep(BUTTON_PRESS_DELAY)

    elif badge_state.current_state == DisplayStates.MAIN_SCREEN:
        if button_states["A"]:
            logger.debug("Button A pressed - sending message")
            badge_state.transition_to(DisplayStates.SENDING)
            send_predefined_message()
            badge_state.transition_to(DisplayStates.MAIN_SCREEN)
            display_main_screen()
            time.sleep(BUTTON_PRESS_DELAY)

        elif button_states["B"]:
            logger.debug("Button B pressed - checking downlink")
            check_downlink_message()
            time.sleep(BUTTON_PRESS_DELAY)

        elif button_states["C"]:
            logger.debug("Button C pressed - showing menu")
            badge_state.transition_to(DisplayStates.MESSAGE_MENU)
            show_message_menu()
            time.sleep(BUTTON_PRESS_DELAY)

    elif badge_state.current_state == DisplayStates.MESSAGE_MENU:
        if button_states["A"]:
            logger.debug("Button A pressed - returning to main screen")
            badge_state.transition_to(DisplayStates.MAIN_SCREEN)
            display_main_screen()
            time.sleep(BUTTON_PRESS_DELAY)

        elif button_states["UP"]:
            print("DEBUG: Processing UP button press")
            current_index = badge_state.selected_index
            badge_state.selected_index = (current_index - 1) % len(messages)
            print(f"DEBUG: Index changed from {current_index} to {badge_state.selected_index}")
            show_message_menu()
            time.sleep(BUTTON_PRESS_DELAY)

        elif button_states["DOWN"]:
            print("DEBUG: Processing DOWN button press")
            current_index = badge_state.selected_index
            badge_state.selected_index = (current_index + 1) % len(messages)
            print(f"DEBUG: Index changed from {current_index} to {badge_state.selected_index}")
            show_message_menu()
            time.sleep(BUTTON_PRESS_DELAY)

        elif button_states["C"]:
            print("DEBUG: Processing C button press - sending message")
            # Select and send the message directly
            selected_message = messages[badge_state.selected_index]
            selected_identifier = message_identifiers[badge_state.selected_index]
            logger.info(f"Selected and sending message: {selected_message} with identifier {selected_identifier}")
            badge_state.select_message(selected_message, selected_identifier)
            
            # Send the message
            badge_state.transition_to(DisplayStates.SENDING)
            send_predefined_message()
            
            # Return to main screen
            badge_state.transition_to(DisplayStates.MAIN_SCREEN)
            display_main_screen()
            time.sleep(BUTTON_PRESS_DELAY)

    if not is_on_battery():
        display.halt()
