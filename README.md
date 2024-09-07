<h1>Sailing Display - Weather API</h1>
<p>This repository includes all of the code that was used in order to make the Sailing display work properly. Please note that when I was completing this project, I was not as proficient in C, so I decided to flash the firmware for micropython onto the board to make the coding experience simpler for myself</p>
<p>Below is the list of the steps that I went through in order to complete this project on a software level</p>
<ol>
  <li>Flashing Firmware for micropython onto the esp32 and testing to see the results using serial monitors</li>
  <li>Utilizing esp libraries to connect the board to my home wifi network and making requests to google</li>
  <li>Creating a file that sends a request to an open source weather API and organizes the data to see if the conditions are right for sailing</li>
  <li>Displaying the results of the API call on the SPI-controlled ili9341 by connecting necessary pins and driving the display</li>
</ol>
<p>Thank you for checking out this project of mine! As always, if you have any questions, feel free to ask!</p>
