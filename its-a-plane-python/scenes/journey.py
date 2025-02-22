from utilities.animator import Animator
from setup import colours, fonts
from rgbmatrix import graphics
from config import DISTANCE_UNITS

# Attempt to load config data
try:
    from config import JOURNEY_CODE_SELECTED

except (ModuleNotFoundError, NameError, ImportError):
    # If there's no config data
    JOURNEY_CODE_SELECTED = "GLA"

try:
    from config import JOURNEY_BLANK_FILLER

except (ModuleNotFoundError, NameError, ImportError):
    # If there's no config data
    JOURNEY_BLANK_FILLER = " ? "

# Setup
JOURNEY_POSITION = (17, 0)
JOURNEY_HEIGHT = 10
JOURNEY_WIDTH = 48
JOURNEY_SPACING = 5
JOURNEY_FONT = fonts.regularplus
JOURNEY_FONT_SELECTED = fonts.regularplus_bold
ARROW_COLOUR = colours.GREY
DISTANCE_ORIGIN_COLOUR = colours.LIGHT_GREEN
DISTANCE_DESTINATION_COLOUR = colours.LIGHT_LIGHT_RED
DISTANCE_COLOUR = colours.LIGHT_TEAL
DISTANCE_MEASURE = colours.LIGHT_DARK_TEAL
DISTANCE_POSITION = (17, 16)
DISTANCE_WIDTH = 48
DISTANCE_FONT = fonts.extrasmall

# Element Positions
ARROW_POINT_POSITION = (42, 5)
ARROW_WIDTH = 5
ARROW_HEIGHT = 8


class JourneyScene(object):
    def __init__(self):
        super().__init__()

    @Animator.KeyFrame.add(0)
    def journey(self):
        # Guard against no data
        if len(self._data) == 0:
            return
            
        # Retrieve distance values from the Overhead scene and round to the nearest integer
        distance_origin = int(self._data[self._data_index]["distance_origin"])
        distance_destination = int(self._data[self._data_index]["distance_destination"])

        # Convert distance to either miles or kilometers based on UNITS configuration
        if DISTANCE_UNITS == "imperial":
            distance_units = "mi"
        elif DISTANCE_UNITS == "metric":
            distance_units = "KM"
        else:
            distance_units = "Units"

        # Format distance text
        distance_origin_text = f'{self._data[self._data_index]["distance_origin"]:.0f}{distance_units}'
        distance_destination_text = f'{self._data[self._data_index]["distance_destination"]:.0f}{distance_units}'

        # Grab Airport codes
        origin = self._data[self._data_index]["origin"]
        destination = self._data[self._data_index]["destination"]
        
        # Additional time-related data
        time_scheduled_departure = self._data[self._data_index]["time_scheduled_departure"]
        time_real_departure = self._data[self._data_index]["time_real_departure"]
        time_scheduled_arrival = self._data[self._data_index]["time_scheduled_arrival"]
        time_estimated_arrival = self._data[self._data_index]["time_estimated_arrival"]
        
        # Calculate departure and arrival delays in minutes
        departure_delay_minutes = (
            (time_real_departure - time_scheduled_departure) / 60
            if time_real_departure is not None and time_scheduled_departure is not None
            else 0
        )
        arrival_delay_minutes = (
            (time_estimated_arrival - time_scheduled_arrival) / 60
            if time_estimated_arrival is not None and time_scheduled_arrival is not None
            else 0
        )
        
        # Print time differences for debugging
        #print("Departure Delay (minutes):", departure_delay_minutes)
        #print("Arrival Delay (minutes):", arrival_delay_minutes)
        
        # Set colors based on departure and arrival delays
        if departure_delay_minutes <= 20:
            origin_color = colours.LIGHT_MID_GREEN
        elif 20 < departure_delay_minutes <= 40:
            origin_color = colours.LIGHT_YELLOW
        elif 40 < departure_delay_minutes <= 60:
            origin_color = colours.LIGHT_MID_ORANGE
        elif 60 < departure_delay_minutes <= 240:
            origin_color = colours.LIGHT_RED
        elif 240 < departure_delay_minutes <= 480:
            origin_color = colours.LIGHT_PURPLE
        else:
            origin_color = colours.LIGHT_DARK_BLUE
        
        # Adjust colors for arrival delays
        if arrival_delay_minutes <= 0:
            destination_color = colours.LIGHT_MID_GREEN
        elif 0 < arrival_delay_minutes <= 30:
            destination_color = colours.LIGHT_YELLOW
        elif 30 < arrival_delay_minutes <= 60:
            destination_color = colours.LIGHT_MID_ORANGE
        elif 60 < arrival_delay_minutes <= 240:
            destination_color = colours.LIGHT_RED
        elif 240 < arrival_delay_minutes <= 480:
            destination_color = colours.LIGHT_PURPLE
        else:
            destination_color = colours.LIGHT_DARK_BLUE
        
        # Draw background with the chosen color
        self.draw_square(
            JOURNEY_POSITION[0],
            JOURNEY_POSITION[1],
            JOURNEY_POSITION[0] + JOURNEY_WIDTH - 1,
            JOURNEY_POSITION[1] + JOURNEY_HEIGHT - 1,
            colours.BLACK,
        )

        # Draw origin with the chosen color
        text_length = graphics.DrawText(
            self.canvas,
            JOURNEY_FONT_SELECTED if origin == JOURNEY_CODE_SELECTED else JOURNEY_FONT,
            JOURNEY_POSITION[0],
            JOURNEY_HEIGHT,
            origin_color,
            origin if origin else JOURNEY_BLANK_FILLER,
        )

        # Draw destination with the chosen color
        _ = graphics.DrawText(
            self.canvas,
            JOURNEY_FONT_SELECTED
            if destination == JOURNEY_CODE_SELECTED
            else JOURNEY_FONT,
            JOURNEY_POSITION[0] + text_length + JOURNEY_SPACING + 1,
            JOURNEY_HEIGHT,
            destination_color,
            destination if destination else JOURNEY_BLANK_FILLER,
        )
        # Calculate the center of the available area
        center_x = (16 + 64) // 2

        # Calculate the width of each half
        half_width = (64 - 16) // 2

        # Calculate the width of the text using the font's character width (including space)
        font_character_width = 4
        distance_origin_text_width = len(distance_origin_text) * font_character_width
        distance_destination_text_width = len(distance_destination_text) * font_character_width

        # Calculate the adjusted positions for drawing the text
        distance_origin_x = center_x - half_width + (half_width - distance_origin_text_width) // 2
        distance_destination_x = center_x + (half_width - distance_destination_text_width) // 2
        
      # Iterate through each character in distance_origin_text
        distance_origin_text_length = 0
        for ch in distance_origin_text:
            ch_length = graphics.DrawText(
                self.canvas,
                DISTANCE_FONT,
                distance_origin_x + distance_origin_text_length,
                DISTANCE_POSITION[1],  # Keep the same vertical position
                DISTANCE_COLOUR if ch.isnumeric() else DISTANCE_MEASURE,
                ch,
            )
            distance_origin_text_length += ch_length

        # Iterate through each character in distance_destination_text
        distance_destination_text_length = 0
        for ch in distance_destination_text:
            ch_length = graphics.DrawText(
                self.canvas,
                DISTANCE_FONT,
                distance_destination_x + distance_destination_text_length,
                DISTANCE_POSITION[1],  # Keep the same vertical position
                DISTANCE_COLOUR if ch.isnumeric() else DISTANCE_MEASURE,
                ch,
            )
            distance_destination_text_length += ch_length

    @Animator.KeyFrame.add(0)
    def journey_arrow(self):
        # Guard against no data
        if len(self._data) == 0:
            return

        # Black area before arrow (clears previous arrow)
        self.draw_square(
            ARROW_POINT_POSITION[0] - ARROW_WIDTH,
            ARROW_POINT_POSITION[1] - (ARROW_HEIGHT // 2),
            ARROW_POINT_POSITION[0],
            ARROW_POINT_POSITION[1] + (ARROW_HEIGHT // 2),
            colours.BLACK,
        )

        # Starting positions for filled-in arrow
        x = ARROW_POINT_POSITION[0] - ARROW_WIDTH + 1
        y1 = ARROW_POINT_POSITION[1] - (ARROW_HEIGHT // 2)
        y2 = ARROW_POINT_POSITION[1] + (ARROW_HEIGHT // 2)

        # Retrieve distances
        distance_origin = int(self._data[self._data_index]["distance_origin"])
        distance_destination = int(self._data[self._data_index]["distance_destination"])

        # Handle cases where both or either distance is zero
        if distance_origin == 0 and distance_destination == 0:
            # Both distances are 0, draw all with ARROW_COLOUR
            for _ in range(ARROW_WIDTH):  # ARROW_WIDTH is now defined as 5
                graphics.DrawLine(
                    self.canvas,
                    x,
                    y1,
                    x,
                    y2,
                    ARROW_COLOUR,
                )
                x += 1
                y1 += 1
                y2 -= 1
        elif distance_origin == 0 or distance_destination == 0:
            # Either distance is 0, draw all with ARROW_COLOUR
            for _ in range(ARROW_WIDTH):  # ARROW_WIDTH is still 5
                graphics.DrawLine(
                    self.canvas,
                    x,
                    y1,
                    x,
                    y2,
                    ARROW_COLOUR,
                )
                x += 1
                y1 += 1
                y2 -= 1
        else:
            # Calculate the total distance and the percentage
            total_distance = distance_origin + distance_destination
            origin_ratio = distance_origin / total_distance
            destination_ratio = distance_destination / total_distance
            
            # Total number of pixels for the arrow (5 pixels wide)
            total_pixels = ARROW_WIDTH  # Ensure this is set to 5

            # Allocate pixels based on 10% increments
            if origin_ratio <= 0.10:
                origin_pixels = 0
            elif origin_ratio <= 0.30:
                origin_pixels = 1
            elif origin_ratio <= 0.50:
                origin_pixels = 2
            elif origin_ratio <= 0.70:
                origin_pixels = 3
            elif origin_ratio <= 0.90:
                origin_pixels = 4
            else:
                origin_pixels = 5  # Maximum pixels for origin when ratio > 0.90

            destination_pixels = total_pixels - origin_pixels  # Ensure total equals ARROW_WIDTH

            # Debugging prints for ratios and pixel allocation
            #print(f"Origin ratio: {origin_ratio:.2f}, Destination ratio: {destination_ratio:.2f}")
            #print(f"Origin pixels: {origin_pixels}, Destination pixels: {destination_pixels}")

            # Draw Color A (DISTANCE_ORIGIN_COLOUR) first, consecutively
            for _ in range(origin_pixels):
                graphics.DrawLine(
                    self.canvas,
                    x,
                    y1,
                    x,
                    y2,
                    DISTANCE_ORIGIN_COLOUR,
                )
                x += 1
                y1 += 1
                y2 -= 1

            # Then draw Color B (DISTANCE_DESTINATION_COLOUR) consecutively
            for _ in range(destination_pixels):
                graphics.DrawLine(
                    self.canvas,
                    x,
                    y1,
                    x,
                    y2,
                    DISTANCE_DESTINATION_COLOUR,
                )
                x += 1
                y1 += 1
                y2 -= 1
