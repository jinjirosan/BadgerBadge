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
    
    # Display currently selected message
    display.thickness(2)
    if selected_message:
        preview_text = f"{selected_identifier}: {selected_message}"
        size = fit_text(preview_text, WIDTH - 2 * LEFT_PADDING, min_size=0.4, max_size=0.7)
        display.text(preview_text, LEFT_PADDING, HEIGHT // 2, size)
    else:
        display.text("No message selected", LEFT_PADDING, HEIGHT // 2, 0.6)
    
    # Draw button labels - removed Send, changed Menu to Choose
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
        'AT$T?': {'format': r'\d{1,3}', 'example': '25'},  # Expect integer temperature
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
                    msg = f"Unexpected response for {command} - Received: '{response}', Expected: '{expected}' (Continuing anyway...)"
                    self.logger.warning(msg)
                    return True  # More lenient validation
            elif isinstance(expected, dict):
                import re
                if not re.match(expected['format'], response):
                    msg = f"Unexpected format for {command} - Received: '{response}', Format: {expected['format']}, Example: {expected['example']} (Continuing anyway...)"
                    self.logger.warning(msg)
                    return True  # More lenient validation
        return True

    def _send_command(self, command, read_size=64, timeout=2):
        """Send AT command and read response with detailed logging"""
        self.logger.debug(f"Sending command: {command}")
        
        try:
            # Clear any pending data
            pending_data = []
            while self.uart.any():
                data = self.uart.read()
                if data:
                    pending_data.append(data)
            if pending_data:
                self.logger.warning("Cleared pending data: {}".format(b''.join(pending_data)))
            
            # Send command
            full_command = f"{command}\r\n"
            bytes_written = self.uart.write(full_command)
            self.logger.debug("Command sent: {}, Bytes written: {}, Raw bytes: {}".format(
                full_command.strip(), bytes_written, bytes_to_hex(full_command.encode('utf-8'))))
            
            # Wait for response with timeout
            start_time = time.time()
            response = bytearray()
            
            while (time.time() - start_time) < timeout:
                if self.uart.any():
                    chunk = self.uart.read(read_size)
                    if chunk:
                        response.extend(chunk)
                        self.logger.debug("Received chunk - ASCII: {}, Hex: {}, Bytes: {}".format(
                            chunk, bytes_to_hex(chunk), list(chunk)))
                    if b'\r\n' in response:  # Complete response received
                        break
                time.sleep(0.1)
            
            if response:
                try:
                    decoded = response.decode().strip()
                    self.logger.debug("Response received - Decoded: {}, Raw bytes: {}, Hex: {}".format(
                        decoded, response, bytes_to_hex(response)))
                    
                    # Validate response
                    if self._validate_response(command, decoded):
                        return decoded
                    return None
                    
                except UnicodeDecodeError as e:
                    self.logger.error("Failed to decode response - Raw bytes: {}, Hex: {}, Error: {}".format(
                        response, bytes_to_hex(response), str(e)))
                    return None
            else:
                self.logger.warning("No response after {}s for command: {}, Expected format: {}".format(
                    timeout, command, self.EXPECTED_RESPONSES.get(command.split('=')[0], 'Unknown')))
                return None
                
        except Exception as e:
            self.logger.error("Command failed: {}, Error type: {}, Details: {}".format(
                command, type(e).__name__, str(e)))
            return None

    def send_message(self, identifier):
        """Send message with retries and proper channel reset"""
        if not self.initialized:
            self.logger.error("Sigfox not properly initialized")
            return False
            
        MAX_RETRIES = 3
        self.logger.info("Preparing to send message - ID: {}, Length: {} bytes, Hex: {}".format(
            identifier, len(identifier), bytes_to_hex(identifier)))
        
        # Check signal quality before sending (but don't fail if we can't get it)
        signal = self._send_command("AT$QS?")
        if signal:
            if "ERROR" in signal:
                self.logger.warning("Signal quality unavailable - continuing anyway")
            else:
                try:
                    signal_dbm = int(signal)
                    quality = 'Good' if signal_dbm > -100 else 'Poor'
                    self.logger.info(f"Signal quality: {signal_dbm} dBm ({quality})")
                except ValueError:
                    self.logger.warning(f"Could not parse signal quality: {signal}")
        
        # Reset channels - continue even if it returns ERR_SET_STD_CONFIG_SET
        reset_response = self._send_command(SigfoxCommands.RESET_CHANNELS, timeout=3)
        if reset_response:
            if "ERR_SET_STD_CONFIG_SET" in reset_response:
                self.logger.debug("Channel reset returned expected error - continuing")
            elif "OK" not in reset_response:
                self.logger.warning(f"Unexpected channel reset response: {reset_response}")
        else:
            self.logger.warning("No response from channel reset - continuing anyway")

        # Try sending with retries
        for attempt in range(MAX_RETRIES):
            self.logger.debug(f"Send attempt {attempt + 1}/{MAX_RETRIES}")
            
            # Send the message
            command = f"{SigfoxCommands.SEND_FRAME}={identifier}"
            response = self._send_command(command, timeout=8)
            
            if response:
                self.logger.debug(f"Raw response for attempt {attempt + 1}: {response}")
                if "OK" in response:
                    self.logger.info("Message sent successfully")
                    return True
                else:
                    self.logger.warning(f"Send attempt {attempt + 1} failed: {response}")
            else:
                self.logger.warning(f"No response for attempt {attempt + 1}")
            
            if attempt < MAX_RETRIES - 1:
                self.logger.debug("Waiting before retry...")
                time.sleep(2)
                
        self.logger.error("All send attempts failed")
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

        if sigfox.send_message(selected_identifier):
            display_message("Message Sent")
            system_monitor.log_metric('message_sends')
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
        turn_on_led()
        # Show checking status
        display.pen(15)
        display.rectangle(WIDTH // 2 - 20, HEIGHT - 10, 50, 10)
        display.pen(0)
        display.text("Checking", WIDTH // 2 - 20, HEIGHT - 10, 0.5)
        display.update()
        
        response = sigfox.check_downlink()
        system_monitor.log_metric('downlink_checks')
        
        if response:
            # Show message with Return button
            display.pen(15)
            display.clear()
            display.pen(0)
            display.font("sans")
            display.thickness(2)
            size = fit_text(response, WIDTH - 2 * LEFT_PADDING)
            display.text(response, LEFT_PADDING, HEIGHT // 2 - 5, size)
            display.text("Return", WIDTH // 2 - 20, HEIGHT - 10, 0.5)
            display.update()
            is_downlink_displayed = True
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

# Ensure the number of identifiers matches the number of messages
message_identifiers = message_identifiers[:len(messages)]

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
