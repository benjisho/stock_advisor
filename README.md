# Stock Advisor

This is a simple stock advisor program that provides buy or short recommendations for A stock based on technical indicators.
It is intended for educational purposes and serves as an example of how to apply technical analysis to stock trading.
Please note that this program does not guarantee any financial success, and you should exercise caution and seek professional financial advice when making real investment decisions.

# Table of Contents
- [Getting Started](#getting-started)
    - [Clone repository to your local machine](#1-clone-repository-to-your-local-machine)
    - [Ensure you have Python installed on your system](#2-ensure-you-have-python-installed-on-your-system)
    - [Install the required Python packages](#3-install-the-required-python-packages)
        - [Option 1 - install on the host machine](#option-1---install-on-the-host-machine)
        - [Option 2 - Create a virtual environment](#option-2---create-a-virtual-environment)
    - [Customize the technical indicators and strategy](#4-customize-the-technical-indicators-and-strategy)
    - [Run your Python program](#5-run-your-python-program)
- [File Structure](#file-structure)
- [Contributing](#contributing)
- [Disclaimer](#disclaimer)
- [License](#license)

## Getting Started
To get started with the QYLD Stock Advisor, follow these steps:

### 1. Clone repository to your local machine
```bash
git clone https://github.com/benjisho/stock_advisor.git
```
### 2. Ensure you have Python installed on your system
```bash
python --version
```
If Python is not installed, you can download and install it from the official Python website (https://www.python.org/downloads/).

### 3. Install the required Python packages:
#### Option 1 - install on the host machine
```bash
apt install python3-pandas
apt install python3-requests
apt install python3-numpy
```
#### Option 2 - Create a virtual environment
1. Create a virtual environment (if you haven't already):
```bash
python3 -m venv venv
```
This command will create a virtual environment named venv in your project directory.

2. Activate the virtual environment:

On Linux or macOS:
```bash
source venv/bin/activate
```
On Windows (in Command Prompt):
```bash
venv\Scripts\activate
```
3. Once your virtual environment is activated, you can install the required packages using pip:
```bash
pip3 install -r requirements.txt
```
This will install the necessary packages in your virtual environment.

4. Customize the technical indicators and strategy in the indicators and strategy directories as per your requirements.
`strategy/stock_strategy.py` and `indicators/moving_averages.py`

5. Run your Python program within the virtual environment:
```bash
python3 main.py
```
This will install the necessary packages specified in the requirements.txt file.

## File Structure
The repository follows the following file structure:

```css
stock_advisor/
    ├── indicators/
    │   ├── moving_averages.py
    ├── strategy/
    │   ├── stock_strategy.py
    ├── requirements.txt
    ├── main.py
```

`indicators`: Contains code for technical indicators.

`strategy`: Includes the main stock strategy logic.

`main.py`: The entry point of the program.

## Contributng
Contributions to improve and extend this simple stock advisor project are welcome. If you have ideas, bug fixes, or improvements, feel free to submit a pull request.

## Disclaimer
This stock advisor is for educational purposes only and should not be used for real investment decisions. It does not guarantee any financial success, and the author is not responsible for any losses incurred while using this program.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

For any questions or clarifications, please feel free to contact the project owner.
