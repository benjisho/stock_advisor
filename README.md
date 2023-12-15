# Stock Advisor

This is a simple stock advisor program that provides buy or short recommendations for A stock based on technical indicators.
It is intended for educational purposes and serves as an example of how to apply technical analysis to stock trading.
Please note that this program does not guarantee any financial success, and you should exercise caution and seek professional financial advice when making real investment decisions.

![image](https://github.com/benjisho/stock_advisor/assets/97973081/4f1d60b4-2618-4274-9810-94ebce355c68)

# Table of Contents
- [Getting Started](#getting-started)
  * [Running using Docker](#running-using-docker)
    + [Clone repository to your local machine](#clone-repository-to-your-local-machine)
    + [Get the Docker Image](#get-the-docker-image)
      - [Option 1 - Pull the image from DockerHub](#option-1---pull-the-image-from-dockerhub)
      - [Option 2 - Build the Dockerimage](#option-2---build-the-dockerimage)
    + [Run the Docker container](#run-the-docker-container)
  * [Running Manually](#running-manually)
    + [Clone repository to your local machine](#clone-repository-to-your-local-machine-1)
    + [Ensure you have Python installed on your system](#ensure-you-have-python-installed-on-your-system)
    + [Install the required Python packages - Create a virtual environment](#install-the-required-python-packages---create-a-virtual-environment)
  * [File Structure](#file-structure)
  * [Contributing](#contributing)
  * [Disclaimer](#disclaimer)
  * [License](#license)

## Getting Started
To get started with the Stock Advisor, follow these steps:

### Running using Docker
You can easily run the stock_advisor application using the Docker image hosted on Docker Hub.

#### 1. Clone repository to your local machine
```bash
git clone https://github.com/benjisho/stock_advisor.git
```

#### Get the Docker Image
##### Option 1 - Pull the image from DockerHub
To pull the image from Docker Hub, use the following command:
```bash
docker pull benjisho/stock_advisor

```
##### Option 2 - Build the Dockerimage:

```bash
docker build -t benjisho/stock_advisor .
```

#### 2. Run the Docker container
```bash
docker run -it --rm --name my_stock_advisor_app benjisho/stock_advisor
```

### Running Manually
#### 1. Clone repository to your local machine
```bash
git clone https://github.com/benjisho/stock_advisor.git
```

#### 2. Ensure you have Python installed on your system
```bash
python --version
```
If Python is not installed, you can download and install it from the official Python website (https://www.python.org/downloads/).

#### 3. Install the required Python packages - Create a virtual environment
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
    ├── .dockerignore
    ├── Dockerfile
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
