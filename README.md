# E-PACERR Statistical Analysis App

The E-PACERR Statistical Analysis App is a Python application built using Tkinter, Matplotlib, and Pandas. This app is designed to analyze the system usability of the E-PACERR program based on user feedback provided at the completion of each module. It follows the standard system usability scoring and provides box and whisker plots to score the user's answers, along with calculating the overall system usability score.

## Table of Contents
1. [Key Features](#key-features)
2. [Dependencies](#dependencies)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Qualtrics](#qualtrics)
6. [Example](#example)
7. [License](#license)
8. [Contact Information](#contact-information)

## Key Features

- Preliminary Questions Analysis
- System Usability Questions Analysis
- System Usability Score Calculation
- Generation of Box and Whisker Plots
- User-friendly Tkinter GUI

## Dependencies

Make sure you have the following dependencies installed:

- [Python](https://www.python.org/)
- [Tkinter](https://docs.python.org/3/library/tkinter.html)
- [Matplotlib](https://matplotlib.org/)
- [Pandas](https://pandas.pydata.org/)

## Installation

To run the app, follow these steps:

1. **Download the code:**
   ```bash
   git clone https://github.com/lukeirwin03/epacerr-statistics-app.git
   cd epacerr-statistics-app

2. **Ensure you have Python installed.**
3. **If the dependencies haven't been installed yet, install them. The following example uses pip, but you can use any prefered package manager:**
   ```bash
   pip install tk pandas matplotlib

## Usage

1. Launch the app by running `main.py`.
2. Ensure that you have a correctly formatted [Qualtrics Survey.](#Qualtrics)
3. Select the module for analysis (or skip to analyze all modules).
4. Choose the Qualtrics survey file matching the required format.

## Qualtrics
Link to Survey: https://unomaha.az1.qualtrics.com/jfe/form/SV_0B9VoRnswJX8qxg

### Introductory Questions
- Question 1 (type-field): Please enter your first and last name.
- Question 2 (type-field): Please enter your email address.
  
### Module Selection
- Question 1 (multiple choice): Please select the module that this feedback is for.

### User Satisfaction
The following questions refer to the user satisfaction with the content.
- Question 1 (matrix-table): Overall, I am satisfied with the ease of completing tasks in this module.
- Question 2 (matrix-table): Overall, I am satisfied with the amount of time it took to complete the tasks in this module.
- Question 3 (matrix-table): Overall, I am satisfied with the support information (online help, messages, documentation) when completing this task.

### System Usability Questions
- Question 1 (matrix-table): I think that I would like to use this module frequently.
- Question 2 (matrix-table): I found the module unnecessarily complex.
- Question 3 (matrix-table): I thought the module layout was easy to use.
- Question 4 (matrix-table): I think that I would need the support of a technical person to be able to use the module layout.
- Question 5 (matrix-table): I found the various lessons in the module were well integrated.
- Question 6 (matrix-table): I thought there was too much inconsistency in the module layout.
- Question 7 (matrix-table): I would imagine that most people would learn to traverse the module independently very quickly.
- Question 8 (matrix-table): I found the module layout very cumbersome to use.
- Question 9 (matrix-table): I felt very confident using the module layout.
- Question 10 (matrix-table): I needed to learn a lot of things before I could get going with the module.

### Saving the Results
To properly export the data from Qualtrics, perform the following steps from the `Survey` page:
1. Navigate to the `Data & Analysis` Tab
2. Click on `Export & Import`
3. Click `Export...`
4. Select the `Use numeric values` radio button
5. Click `Download`

## Example

![Include screenshots or code snippets demonstrating app usage]

## License

[Choose an appropriate license for your project. You can find licenses on [ChooseALicense.com](https://choosealicense.com/)]

## Contact Information

For questions or issues, please contact:
- Luke Irwin at lukemirwin@gmail.com or lukeirwin@unomaha.edu
- Dr. Kate Cooper at email@email.email
