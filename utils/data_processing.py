import pandas as pd

def parse_file(uploaded_file, required_columns=None, optional_columns=None):
    """
    Parse the uploaded file into a Pandas DataFrame.
    Supports Excel and CSV formats. Handles required and optional columns dynamically.
    
    Args:
        uploaded_file: File object (Excel or CSV).
        required_columns: List of mandatory column names (optional).
        optional_columns: List of additional column names to handle (optional).
    
    Returns:
        dict: A dictionary containing:
              - 'data': DataFrame with parsed and validated data.
              - 'missing_columns': List of missing required columns (if any).
              - 'detected_columns': List of detected optional/relevant columns.
    """
    try:
        # Load the file based on format
        if uploaded_file.name.endswith(".xlsx"):
            excel_file = pd.ExcelFile(uploaded_file)
            if len(excel_file.sheet_names) > 1:
                # If multiple sheets, select the first by default
                sheet_to_use = excel_file.sheet_names[0]
                print(f"Multiple sheets found. Defaulting to the first sheet: {sheet_to_use}")
                data = pd.read_excel(uploaded_file, sheet_name=sheet_to_use)
            else:
                data = pd.read_excel(uploaded_file)
        elif uploaded_file.name.endswith(".csv"):
            data = pd.read_csv(uploaded_file)
        else:
            raise ValueError("Unsupported file format. Please upload .xlsx or .csv files.")
        
        # Initialize results
        missing_columns = []
        detected_columns = []

        # Validate required columns
        if required_columns:
            missing_columns = [col for col in required_columns if col not in data.columns]
            if missing_columns:
                print(f"Missing required columns: {missing_columns}")

        # Detect optional/relevant columns
        if optional_columns:
            detected_columns = [col for col in optional_columns if col in data.columns]

        # Handle missing values and data types
        data = data.fillna(0)  # Fill NaN values with 0
        for col in data.columns:
            if data[col].dtype == "object":
                try:
                    data[col] = pd.to_numeric(data[col], errors="coerce").fillna(0)
                except:
                    pass  # Leave as-is if not convertible

        # Add missing additional input columns as placeholders
        if optional_columns:
            for col in optional_columns:
                if col not in data.columns:
                    data[col] = 0  # Add missing columns with default value 0

        # Summarize results
        result = {
            "data": data,
            "missing_columns": missing_columns,
            "detected_columns": detected_columns,
        }
        return result
    except Exception as e:
        raise ValueError(f"Error processing file: {e}")
