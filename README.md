# Raspberry Pi Pico Interactive Weather Display
## Report Overview
1. Project Outline
    1. Overview
    2. Key components
    3. Networking Overview
3. Design Decisions
4. Evaluation
5. Conclusion
## Project Outline
### Overview
The core idea behind this project was to create an interactive weather display that could be configured through an external webpage. The user could submit their location through the webpage and the display would show information about the weather at the selected location. Alongside this, through the use of interactive buttons, the user could select a status message, which when confirmed, could be displayed on a webpage of their choice.
Key Components

#### 1.3” OLED Display
The main component in the display is the OLED screen that provides the user with a visual representation of the weather data as well as a separate menu to interact with.
### Interactive Buttons
The system features 3 buttons which can be interacted with to change display options and confirm data selection. This provides an interactive element to what would otherwise be a static display.
#### Buzzer
Finally, the system features a buzzer. This provides audio confirmation to the user when they have chosen and submitted a status option.


### Networking Overview
The project utilises networking functionalities such as sending and receiving data via an API, as well as hosting a html webpage. Specifically, it receives location specific weather data from https://openweathermap.org/ and sends data to a private https://jsonbin.io/ bin that can then be accessed by another webpage using a read-only API key. This allows the user to have choice in where they display this information as it can be displayed anywhere that accepts html and javascript. Obviously there are some security concerns in having an API key in frontend and visible javascript, but for the scope of the prototype it was decided that based on the nature of the data and the use of a read-only API key, this was a suitable solution to show functionality. Alongside this, the Pico hosts a html webpage that allows the user to submit their location via a html form that is then used to display weather data for that location. The use of the webpage means the user is not required to submit any data directly via the terminal which makes the system more user-friendly for non technical users.
## Design Decisions
During the design phase, multiple decisions were made that were key to the project's development. Firstly, it was decided to output information to a 1.3” OLED display instead of in a purely text format as it allows for the use of visual aids and icons to support the displayed information as well as providing a more tangible output for the system.
	Secondly, the button layout was also specifically chosen to be intuitive to use by splitting the buttons by which display view they interacted with. Within the code, the buttons are labelled alphabetically, and in a non-prototype system they would preferably be colour coded, but within the constraints of a breadboard based prototype this was not easily achievable.
	Thirdly, the use of a buzzer was chosen to provide an audio cue for the user when they have chosen to submit a status using the button interface. Having an audio cue is important because it provides the user with a confirmation of their action which would not otherwise be clear.
	Finally, when setting up the networking, it was chosen to connect directly to a mobile phone hotspot rather than a specific network. This allows the system to be much more portable as the connection details are hardcoded, being able to connect to a mobile hotspot means the user can be in various different locations without having to change the networking details in the code.
## Evaluation
While the system meets all of its current requirements, If it were to be developed further it would be interesting to consider expanding on the current features such as allowing the user to select a location anywhere in the world (as opposed to just within the united kingdom) or expand the display options to show more comprehensive data such as wind speed or a more long-term weather forecast.
## Conclusion
In conclusion, the system provides a small but interactive and portable interface that is both user friendly but comprehensive enough to provide useful data. It contains networking ability both for receiving data and also improving the user experience through a web interface. Alongside this, the display and buzzer provide an audio and visual experience for the user to interact with which completes the systems functionality.
