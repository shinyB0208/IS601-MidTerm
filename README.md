# IS601-MidTerm
# Python Calculator with Modular Arithmetic Operations and Plugin System

## Project Overview

The PythonCalculatorMidterm project is a comprehensive Python application designed for arithmetic calculations, featuring a modular architecture with a dynamic plugin system. It offers essential arithmetic operations such as addition, subtraction, multiplication, and division, while also providing a mechanism for easy scalability through the addition of new plugins.

## Key Components

### 1. App Class
- The central orchestrator responsible for loading plugins and executing commands through a CommandHandler mechanism.
- Utilizes a factory method pattern to dynamically create Command objects without specifying their exact class.
- Offers a flexible structure allowing seamless integration of additional functionalities.

### 2. CommandHandler Class
- Implements the command pattern, encapsulating requests as objects and allowing parameterization of clients with queues, requests, and operations.
- Facilitates the execution of arithmetic operations and other commands by routing requests to the appropriate Command objects.

### 3. Arithmetic Operation Plugins
- Each arithmetic operation (addition, subtraction, multiplication, division) is encapsulated within its own plugin.
- These plugins extend the Command abstract class, enabling seamless integration into the CommandHandler mechanism.

### 4. CalculationHistory Class
- Manages the history of calculations performed by the user.
- Utilizes the singleton pattern to ensure a single instance throughout the application's lifecycle.
- Implements functionality for loading, saving, clearing, and deleting calculation records.
- Persistently stores calculation history in a .csv file for future reference using the pandas library.

### 5. LoggingUtility Class
- Provides comprehensive logging capabilities across the application.
- Contains static methods for logging information, warnings, and errors, ensuring consistent logging practices throughout the project.

## Configuration

### 1. logging.conf
- Configures basic logging settings such as format and date format.
- Sets up a console handler for displaying log messages.

### 2. .env File
- Utilized for managing environment variables, ensuring flexibility and portability.
- Allows customization of settings such as file paths and configurations.

### 3. pytest.ini
- Specifies pytest configurations, including minimum version requirements and test file directories.

## Environment Variables
- Environment variables such as HISTORY_FILE_PATH are utilized to customize the behavior of the application.
- Loaded using the dotenv library, ensuring easy configuration management.

## Error Handling Strategies
- Employing the "Easier to Ask for Forgiveness than Permission" (EAFP) principle, the project prioritizes exception handling over pre-checking conditions.
- This approach enhances readability and simplifies code logic, promoting a more concise and robust error handling mechanism.

Overall, the PythonCalculatorMidterm project exemplifies best practices in modular design, pattern implementation, and error handling, offering a flexible and extensible solution for arithmetic calculations in Python.
