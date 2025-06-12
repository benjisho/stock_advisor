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
  * [Testing](#testing)
    + [Running Tests](#running-tests)
    + [Test Categories](#test-categories)
  * [Data Source Management](#data-source-management)
    + [Available Data Sources](#available-data-sources)
    + [Decommission Procedure](#decommission-procedure)
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

#### 2. Get the Docker Image
##### Option 1 - Pull the image from DockerHub
To pull the image from Docker Hub, use the following command:
```bash
docker pull benjisho/stock_advisor

```
##### Option 2 - Build the Dockerimage:

```bash
docker build -t benjisho/stock_advisor .
```

#### 3. Run the Docker container
```bash
docker run -it --rm --name my_stock_advisor_app benjisho/stock_advisor
```
---

### Running with Docker Compose

1. Pull the image from Docker Hub, use the following command:
```bash
docker pull benjisho/stock_advisor

```

2. Run the `stock_advisor` application using Docker Compose and automatically remove the container after it exits, use the following command:

```bash
docker-compose run --rm stock_advisor
```

This command runs the application in an interactive mode and cleans up the container after the application finishes.

---

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

The application fetches historical prices using `yfinance` first. If that
fails, it will attempt the following free data sources in order:

1. **Stooq** via `pandas_datareader`
2. **FinanceDataReader**
3. **InvestPy**

The program prints the current price along with the name of the data source so
you know where the prices came from.
The historical data is sorted by date so the latest close reflects the most
recent trading day even when using these alternative sources.

4. Customize the technical indicators and strategy in the indicators and strategy directories as per your requirements.
`strategy/stock_strategy.py` and `indicators/moving_averages.py`

5. Run your Python program within the virtual environment:
```bash
python3 main.py
```
This will install the necessary packages specified in the requirements.txt file.

## Testing

The Stock Advisor includes a comprehensive test suite built with pytest to ensure data source reliability and functionality.

### Test Structure

```
tests/
├── __init__.py
├── conftest.py                              # Shared fixtures and utilities
├── unit/                                    # Unit tests for individual components
│   ├── test_indicators.py                   # Tests for technical indicators
│   ├── test_strategy.py                     # Tests for stock strategy logic
│   └── test_data_processing.py              # Tests for data processing functions
├── integration/                             # Integration tests
│   ├── test_data_sources.py                 # Tests for data source fallback mechanisms
│   └── test_comprehensive_data_sources.py   # Comprehensive integration tests
└── data_sources/                           # Data source specific tests
    └── test_financedata_reader_comprehensive.py # Comprehensive FinanceDataReader tests
```

### Running Tests

To run all tests:
```bash
pytest
```

To run tests with verbose output:
```bash
pytest -v
```

To run specific test categories:
```bash
# Run only unit tests (fast)
pytest tests/unit/ -v

# Run only integration tests
pytest tests/integration/ -v

# Run only data source tests
pytest tests/data_sources/ -v

# Run tests by markers
pytest -m "unit" -v                    # Unit tests only
pytest -m "integration" -v             # Integration tests only
pytest -m "smoke" -v                   # Quick smoke tests
pytest -m "data_source" -v             # All data source tests
pytest -m "not slow" -v                # Skip slow network tests
```

To run tests with coverage:
```bash
# Generate coverage report
pytest --cov=. --cov-report=html --cov-report=term-missing

# View HTML coverage report
open htmlcov/index.html  # On macOS
# or
xdg-open htmlcov/index.html  # On Linux
```

### Test Categories

Our test suite includes several categories organized by pytest markers:

- **Unit Tests** (`@pytest.mark.unit`): Fast tests for individual components
  - Technical indicators testing
  - Strategy logic validation
  - Data processing functions
  
- **Integration Tests** (`@pytest.mark.integration`): Tests for data source fallback mechanisms
  - End-to-end workflow validation
  - Cross-component interaction tests
  - System behavior under failure conditions
  
- **Smoke Tests** (`@pytest.mark.smoke`): Quick functionality verification tests
  - Basic import and connectivity tests
  - Essential health checks
  
- **Data Source Tests** (`@pytest.mark.data_source`): Specific tests for each data provider
  - Yahoo Finance tests
  - Stooq tests  
  - FinanceDataReader tests
  - InvestPy tests
  
- **Slow Tests** (`@pytest.mark.slow`): Network-dependent tests that may take longer
  - Comprehensive data fetching tests
  - Large dataset processing tests

### Continuous Integration

The project includes automated testing via GitHub Actions:

- **CI Pipeline** (`.github/workflows/ci.yml`): Runs comprehensive test suite
  - Tests across multiple Python versions (3.9, 3.10, 3.11)
  - Parallel test execution for faster feedback
  - Code coverage reporting
  - Code quality checks (flake8, black, isort)
  - Security scanning with safety

- **Docker Testing**: Validates containerized deployments
- **Integration Testing**: Tests data source fallback mechanisms

### Test Configuration

Test configuration is managed through `pytest.ini`:

```ini
[tool:pytest]
testpaths = tests
addopts = -v --tb=short --strict-markers --strict-config
markers =
    unit: Unit tests for individual components - fast and isolated
    integration: Integration tests - may require network
    smoke: Quick smoke tests - essential health checks
    slow: Tests that may take longer to run
    data_source: Tests specific to data source functionality
    # ... additional markers for specific data sources
```

## Data Source Management

The Stock Advisor uses multiple data sources in a fallback hierarchy to ensure reliability.

### Available Data Sources

The application attempts to fetch data in the following order:

1. **Yahoo Finance** (via `yfinance`) - Primary source
2. **Stooq** (via `pandas_datareader`) - First fallback
3. **FinanceDataReader** - Second fallback
4. **InvestPy** - Final fallback

Each source is tested independently and as part of the fallback chain.

### Decommission Procedure

If a data source needs to be decommissioned due to reliability issues, API changes, or discontinuation, follow this comprehensive procedure:

#### Step 1: Identify the Failing Source

Before decommissioning, thoroughly investigate the issue:

```bash
# Run comprehensive data source tests
pytest tests/data_sources/ -v --tb=long

# Test specific data source in isolation
pytest tests/data_sources/test_financedata_reader_comprehensive.py -v

# Run integration tests to see fallback behavior
pytest tests/integration/ -m "data_source" -v

# Manual testing with the main application
echo "AAPL" | python3 main.py
echo "GOOGL" | python3 main.py
```

Document the specific failures:
- Error messages and stack traces
- Affected symbols or markets
- Frequency of failures
- Impact on application functionality

#### Step 2: Plan the Decommission

**Assess Impact:**
- Determine which data source in the fallback chain is failing
- Identify alternative sources that can provide coverage
- Estimate the impact on data availability and quality

**Timeline:**
- **Immediate** (API broken/crashing): Emergency disable
- **Planned** (deprecation notice): Gradual phase-out over 2-4 weeks
- **Permanent** (service discontinued): Complete removal

#### Step 3: Code Changes

**3.1 Emergency Disable (Immediate)**

For urgent issues causing application crashes:

```python
# In main.py, wrap the problematic source in a try-catch
# Example for FinanceDataReader:
try:
    # Temporarily disable FinanceDataReader
    raise Exception("FinanceDataReader temporarily disabled due to API issues")
    
    # [Original FinanceDataReader code commented out]
    # import FinanceDataReader as fdr
    # data = fdr.DataReader(symbol, '2000')
    # ...
except Exception as e:
    print(f"FinanceDataReader disabled: {e}. Trying InvestPy...")
```

**3.2 Planned Removal (Complete Decommission)**

1. **Remove from main.py:**
```python
# Remove or comment out the entire data source block
# Example - removing FinanceDataReader section (lines 52-66):

# # Attempt FinanceDataReader
# try:
#     import FinanceDataReader as fdr
#     data = fdr.DataReader(symbol, '2000')
#     if not data.empty:
#         data_source = "FinanceDataReader"
#         data = data.reset_index().rename(columns={'index': 'Date'})
#         print(f"Successfully fetched historical data for {symbol} from {data_source}")
#         print("----------------------------------------------------------------")
#         data = process_data(data)
#         return data, data_source
# except Exception as e:
#     print(f"FinanceDataReader retrieval failed: {e}. Trying InvestPy...")
```

2. **Update requirements.txt:**
```bash
# Remove the decommissioned package
# Example: Remove finance-datareader==0.9.96
sed -i '/finance-datareader/d' requirements.txt
```

3. **Update error messages:**
```python
# Update fallback messages to skip decommissioned source
print(f"Stooq retrieval failed: {e}. Trying InvestPy...")  # Skip FDR mention
```

#### Step 4: Test Updates

**4.1 Mark affected tests:**

```python
# In test files, mark decommissioned source tests as skipped
@pytest.mark.skip(reason="FinanceDataReader decommissioned - API discontinued")
class TestFinanceDataReaderBasic:
    # ... existing tests
```

**4.2 Update integration tests:**

```python
# Update fallback sequence tests
def test_fallback_without_fdr(self):
    """Test fallback sequence without FinanceDataReader"""
    # Test: Yahoo -> Stooq -> InvestPy (skipping FDR)
    # ...
```

**4.3 Add decommission documentation test:**

```python
@pytest.mark.unit
def test_decommissioned_sources_documented(self):
    """Ensure decommissioned sources are properly documented"""
    # Check that README reflects current data sources
    # Check that code comments explain removal
    # ...
```

#### Step 5: Documentation Updates

**5.1 Update README.md:**

```markdown
### Available Data Sources

The application attempts to fetch data in the following order:

1. **Yahoo Finance** (via `yfinance`) - Primary source
2. **Stooq** (via `pandas_datareader`) - First fallback  
3. ~~**FinanceDataReader** - DECOMMISSIONED (2025-06-12) - API discontinued~~
4. **InvestPy** - Final fallback

### Decommissioned Data Sources

- **FinanceDataReader** (Decommissioned: 2025-06-12)
  - Reason: API reliability issues and service discontinuation
  - Replacement: Enhanced Stooq integration and InvestPy fallback
  - Impact: Minimal - covered by remaining sources
```

**5.2 Add changelog entry:**

```markdown
## Changelog

### [Version X.X.X] - 2025-06-12

#### Removed
- **FinanceDataReader data source** 
  - Reason: API discontinued by provider
  - Migration: Automatic fallback to remaining sources
  - Tests: Marked as skipped, integration tests updated
```

#### Step 6: Deployment and Validation

**6.1 Test the changes:**

```bash
# Run full test suite
pytest tests/ -v

# Test main application functionality
echo "AAPL" | python3 main.py
echo "GOOGL" | python3 main.py
echo "MSFT" | python3 main.py

# Test with various symbols to ensure coverage
for symbol in AAPL GOOGL MSFT TSLA AMZN; do
    echo "Testing $symbol..."
    echo "$symbol" | timeout 60 python3 main.py
done
```

**6.2 Update CI/CD:**

```yaml
# Update .github/workflows/ci.yml if needed
# Remove any specific data source testing jobs
# Update dependency installation steps
```

**6.3 Update Docker:**

```bash
# Rebuild Docker images without decommissioned dependencies
docker build -t benjisho/stock_advisor:latest .

# Test Docker deployment
docker run -it --rm benjisho/stock_advisor:latest
```

#### Step 7: Monitor and Communicate

**7.1 Monitor application health:**
- Watch for any new failures or degraded performance
- Monitor data coverage and quality metrics
- Track fallback usage patterns

**7.2 Communicate changes:**
- Update project documentation
- Notify users through appropriate channels
- Document lessons learned for future decommissions

#### Emergency Rollback Procedure

If decommissioning causes unexpected issues:

```bash
# 1. Revert code changes
git revert <commit-hash>

# 2. Restore dependencies
git checkout HEAD~1 requirements.txt

# 3. Reinstall packages
pip install -r requirements.txt

# 4. Test restoration
pytest tests/ -m "smoke" -v
```

#### Post-Decommission Cleanup

After successful decommission (wait 1-2 weeks):

```bash
# 1. Remove test files for decommissioned source
rm tests/data_sources/test_financedata_reader_comprehensive.py

# 2. Clean up any remaining references
grep -r "FinanceDataReader" . --exclude-dir=.git

# 3. Update version numbers
# Update pyproject.toml or setup.py version

# 4. Tag release
git tag -a v2.1.0 -m "Remove FinanceDataReader data source"
```

## File Structure
The repository follows the following file structure:

```css
stock_advisor/
├── .github/
│   └── workflows/
│       ├── ci.yml                          # Main CI pipeline with pytest
│       ├── docker-publish.yml              # Docker image publishing
│       ├── docker_test_run.yml             # Docker testing
│       ├── docker_compose_test_run.yml     # Docker Compose testing
│       └── python_venv_test_run.yml        # Python virtual environment testing
├── indicators/
│   └── moving_averages.py                  # Technical indicators implementation
├── strategy/
│   └── stock_strategy.py                   # Main stock strategy logic
├── tests/                                  # Comprehensive pytest test suite
│   ├── __init__.py
│   ├── conftest.py                         # Shared fixtures and test utilities
│   ├── unit/                               # Unit tests for individual components
│   │   ├── README.md
│   │   ├── test_indicators.py              # Tests for technical indicators
│   │   ├── test_strategy.py                # Tests for stock strategy logic
│   │   └── test_data_processing.py         # Tests for data processing functions
│   ├── integration/                        # Integration and end-to-end tests
│   │   ├── README.md
│   │   ├── test_data_sources.py            # Data source fallback mechanism tests
│   │   └── test_comprehensive_data_sources.py # Comprehensive integration tests
│   └── data_sources/                       # Data source specific tests
│       ├── README.md
│       └── test_financedata_reader_comprehensive.py # FinanceDataReader tests
├── .dockerignore
├── Dockerfile
├── docker-compose.yml
├── pytest.ini                              # Pytest configuration and markers
├── requirements.txt                        # Python dependencies including test packages
├── main.py                                 # The entry point of the program
├── README.md                               # This file
└── FINANCEDATA_READER_TEST_SUMMARY.md      # Detailed test results documentation
```

### Directory Organization

- **`.github/workflows/`**: CI/CD pipelines for automated testing and deployment
- **`docs/`**: Detailed documentation including test results and technical specifications
- **`indicators/`**: Contains code for technical indicators and market analysis
- **`strategy/`**: Includes the main stock strategy logic and recommendation engine
- **`tests/`**: Comprehensive pytest test suite organized by test type:
  - **`unit/`**: Fast, isolated tests for individual functions and components
  - **`integration/`**: Tests for component interactions and data flow
  - **`data_sources/`**: Specific tests for external API integrations
- **`main.py`**: The entry point of the program with data fetching and prediction logic
- **`pytest.ini`**: Configuration for pytest test runner with custom markers

## Contributing
Contributions to improve and extend this simple stock advisor project are welcome. If you have ideas, bug fixes, or improvements, feel free to submit a pull request.

## Disclaimer
This stock advisor is for educational purposes only and should not be used for real investment decisions. It does not guarantee any financial success, and the author is not responsible for any losses incurred while using this program.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

For any questions or clarifications, please feel free to contact the project owner.
