# EMI Calculator & Export Tool

A comprehensive loan amortization calculator with a user-friendly graphical interface built with Python and tkinter. Calculate monthly EMI, check loan affordability, view detailed amortization schedules, and export data to CSV.

## Features

### 🎯 Core Functionality
- **EMI Calculation**: Calculates monthly Equated Monthly Installment (EMI) using the standard amortization formula
- **Loan Affordability Check**: Ensures the monthly EMI doesn't exceed 50% of the monthly salary
- **Amortization Schedule**: Generates a detailed month-by-month breakdown of payments, including:
  - Monthly payment amount
  - Interest portion
  - Principal portion
  - Remaining balance
- **CSV Export**: Export the complete amortization schedule to a CSV file for further analysis

### 🖥️ User Interface
- Clean, intuitive tkinter GUI matching modern design standards
- Real-time EMI calculation
- Color-coded affordability status:
  - 🟢 **SAFE (Affordable)**: When EMI ≤ 50% of monthly salary
  - 🔴 **NOT AFFORDABLE**: When EMI > 50% of monthly salary
- Easy-to-use buttons for calculation, viewing schedules, exporting, and clearing data

### 📊 Input Parameters
- **Monthly Salary (₹)**: Your monthly income
- **Loan Amount (₹)**: The principal loan amount
- **Interest Rate (%)**: Annual interest rate
- **Tenure (Years)**: Loan repayment period in years (supports decimal values)

## Installation

### Requirements
- Python 3.6 or higher
- tkinter (usually comes with Python by default)

### Setup
1. Clone or download the project files
2. Navigate to the project directory:
   ```bash
   cd FM_assignment
   ```
3. Run the application:
   ```bash
   python FM_assignment_EAC22009.py
   ```

## Usage

### GUI Mode (Recommended)
1. **Enter Loan Details**:
   - Input your monthly salary
   - Enter the loan amount you want to borrow
   - Specify the annual interest rate
   - Set the loan tenure in years

2. **Calculate EMI**:
   - Click the "Calculate EMI" button
   - View the monthly EMI amount and affordability status

3. **View Schedule**:
   - Click "View Schedule" to see the complete amortization table
   - Scroll through all months to see principal and interest breakdown
   - View total paid and total interest at the bottom

4. **Export Data**:
   - Click "Export CSV" to save the amortization schedule
   - Choose a location and filename to save the CSV file

5. **Clear Fields**:
   - Click "Clear" to reset all input fields to default values

### Example Calculation
Given:
- Monthly Salary: ₹2,000,000
- Loan Amount: ₹20,000,000
- Interest Rate: 10%
- Tenure: 10 years

Result:
- Monthly EMI: ₹264,301.47
- EMI as % of Salary: 13.22%
- Status: ✅ SAFE (Affordable)

## Mathematical Formula

The EMI is calculated using the following formula:

```
EMI = P × r × (1 + r)^n / ((1 + r)^n - 1)

Where:
P = Principal loan amount
r = Monthly interest rate (annual rate / 12 / 100)
n = Total number of months
```

## File Structure

```
FM_assignment/
├── FM_assignment_EAC22009.py    # Main application file
├── README.md                      # This file
└── loan_amortization.csv         # Sample exported schedule (generated)
```

## Functions

### `monthly_payment(principal, annual_rate_percent, n_months)`
Calculates the fixed monthly EMI amount.

**Parameters:**
- `principal` (float): Loan amount
- `annual_rate_percent` (float): Annual interest rate
- `n_months` (int): Loan tenure in months

**Returns:** Monthly payment amount (float)

### `amortization_schedule(principal, annual_rate_percent, n_months)`
Generates a detailed amortization schedule.

**Parameters:**
- Same as `monthly_payment()`

**Returns:** List of dictionaries containing month-by-month details

### `write_csv(schedule, filename)`
Exports the amortization schedule to a CSV file.

**Parameters:**
- `schedule` (List[Dict]): Amortization schedule from `amortization_schedule()`
- `filename` (str): Output CSV filename

## CSV Export Format

The exported CSV file contains the following columns:
- **month**: Month number (1 to n)
- **payment**: Monthly EMI amount
- **interest**: Interest portion of the payment
- **principal**: Principal portion of the payment
- **balance**: Remaining loan balance

Example:
```
month,payment,interest,principal,balance
1,264301.47,166666.67,97634.8,19902365.2
2,264301.47,165685.44,98616.03,19803749.17
...
```

## Command Line Usage (Legacy)

The application also supports command-line arguments:

```bash
python FM_assignment_EAC22009.py -p 20000000 -r 10 --years 10 --csv output.csv
```

Options:
- `-p, --principal`: Loan principal amount (required)
- `-r, --rate`: Annual interest rate in percent (required)
- `--years`: Loan term in years (fractional values allowed)
- `-m, --months`: Loan term in months (alternative to --years)
- `--csv`: Optional output CSV filename

## Affordability Guidelines

The tool uses the following criteria to determine loan affordability:

| EMI to Salary Ratio | Status | Recommendation |
|---|---|---|
| ≤ 30% | Very Safe | Comfortable repayment |
| 30% - 50% | Safe | Manageable with careful budgeting |
| > 50% | Not Affordable | Reconsider loan amount or tenure |

## Error Handling

The application includes validation for:
- Non-numeric input values
- Negative or zero principal amount
- Negative interest rate
- Zero or negative tenure
- Invalid loan tenure in months

## Technical Details

- **Language**: Python 3
- **GUI Framework**: tkinter
- **Data Export**: CSV format
- **Currency**: Indian Rupees (₹)
- **Calculation Precision**: 10 decimal places (rounded for display)

## Troubleshooting

### GUI doesn't start
- Ensure Python is installed: `python --version`
- Verify tkinter is installed: `python -m tkinter`
- If tkinter is missing, install it using your package manager

### CSV export fails
- Check write permissions in the selected directory
- Ensure the filename doesn't contain invalid characters

### Calculation errors
- Verify all input values are positive numbers
- Ensure tenure is greater than 0
- Check that interest rate is reasonable (typically 0-30%)

## License

This project is provided as-is for educational and commercial use.

## Author

**Name**: EAC22009
**Purpose**: Financial Management Assignment - Loan Amortization Calculator

## Version History

### v1.0 (Current)
- Initial GUI implementation
- EMI calculation with affordability check
- Amortization schedule generation
- CSV export functionality
- Command-line interface support

## Future Enhancements

Potential improvements for future versions:
- Support for multiple loan types (home, auto, personal)
- Prepayment calculation
- Comparison tool for different loan scenarios
- Graph visualization of interest vs principal over time
- Support for different currencies
- Data persistence and history

## Support

For issues, questions, or suggestions, please review the code comments or contact the project author.

---

**Created**: February 2026
**Last Updated**: February 18, 2026
