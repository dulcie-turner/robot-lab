# Robot Lab 2023
This code was written as part of the Robot Lab coursework, in which an automated production line was developed. Data loggers are assembled and the three sensors within are tested and replaced as needed. The three sensors detect temperature, pressure, and acceleration. This code handles the operation and testing of the data loggers.

## Raspberry Pi
The code in this section runs on a central Raspberry Pi and tests the data loggers. The file `main.py` runs continually and handles both data capture and logger testing. For the first task, the code checks for received data packets and writes these to the database. (This is an InfluxDB database, accessed through a Grafana dashboard hosted locally on the Pi.) It then checks to see if it has received a testing signal from the control PLC for this cell. If this is the case, it tests all three sensors for the relevant logger. The test results are sent to both the PLC and the database afterwards. If all three tests pass, the logger is allowed to continue. Otherwise, if at least one test passes, the faulty sensors are replaced and the logger is retested until all tests pass. If all tests fail, the logger is assumed to be faulty and is therefore discarded.

### Testing Logic

#### Identifying Loggers
Identifying the logger to be tested posed a challenge during development, since there was no way to keep track of a specific logger's progression through the assembly line. To solve this issue, some assumptions were made. Firstly, all loggers are assumed to be powered on and continually sending data (even ones without sensors attached, which are  sending null values.) At the testing station, a single logger has all three sensors inserted and is then tested. Therefore, the key assumption here is that the latest logger to send data is the one that should be tested. Once the test has finished, a working logger is added to the list of 'loggers to ignore' (and will not be tested again). Partial failures are not added to this list as they are due to be retested next, and complete failures are also not added as they generally send no data and are therefore unidentifiable. Although this logic is functional, it could be reconsidered in future iterations to create a more robust system.

#### Testing Temperature and Pressure
These two tests are done by collecting a specified number of samples from both the logger to be tested and a reference logger (which should be placed nearby.) The two averages of these datasets are taken and their percentage difference compared to a prespecified threshold.

#### Testing Acceleration
During this test, the Raspberry Pi requests 'shaking' from the PLC. As part of this shaking, the logger is picked up by the robot and taken through a prespecified set of motions. The data is collected and an algorithm used to determine whether acceleration has been detected correctly in the x, y and z directions.

## Pico Code
This code runs on each data logger, on a Raspberry Pi Pico microcontroller. Data from all of the three sensors is sent in packets using the MQTT protocol to the Raspberry Pi.

## Credits
The testing procedure was developed by Leopold Dai, Edison Li and Dulcie Turner, with help from Zhengyang Ling and Alan Thorne.
