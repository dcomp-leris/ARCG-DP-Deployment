import re

# Function to extract variable values from the conditions
def extract_values(condition, variable):
    # Regular expression to capture numeric values following the variable
    pattern = rf"\({variable} (<=|>) ([0-9.]+)\)"
    return [float(value) for _, value in re.findall(pattern, condition)]

# Function to add unique values to a list
def add_values(lst, new_values):
    for value in new_values:
        if value not in lst:
            lst.append(value)

# Function to create lists of unique values for FS, PS, and IPI
def create_lists(lines):
    fs_values = []   # List for values of variable FS
    ps_values = []   # List for values of variable PS
    ipi_values = []  # List for values of variable IPI
    ifi_values = []  # List for values of variable IPI

    for line in lines:
        # Extract the condition part
        condition = line.split("->")[0].strip()

        # Extract and add the values of variables 'FS', 'PS', and 'IPI' to the respective lists
        add_values(fs_values, extract_values(condition, "FS"))
        add_values(ps_values, extract_values(condition, "PS"))
        add_values(ipi_values, extract_values(condition, "IPI"))
        add_values(ifi_values, extract_values(condition, "IFI"))
    
    for i, value in enumerate(fs_values):
        fs_values[i] = int(fs_values[i])
        #print(fs_values[i])

    for i, value in enumerate(ps_values):
        ps_values[i] = int(ps_values[i])
        #print(ps_values[i])
    
    for i, value in enumerate(ipi_values):
        ipi_values[i] = int(ipi_values[i])
        #print(ipi_values[i])

    for i, value in enumerate(ifi_values):
        ifi_values[i] = int(ifi_values[i])
        #print(ipi_values[i])      

    # Convert to lists and sort the values
    return sorted(fs_values), sorted(ps_values), sorted(ipi_values), sorted (ifi_values)

# Function to transform rules into the new format
def transform_rules(lines):
    transformed_rules = []
    
    for line in lines:
        # Separate the condition and the class
        condition, class_label = line.split("->")
        class_label = class_label.strip()

        # Set the class value based on the specifications
        #class_value = 1 if class_label == "Other" else 2
        if class_label == "CG":
            class_value = 2
        elif class_label == "AR":
            class_value = 3
        else:
            class_value = 1

        # Generate the new condition
        # new_condition = transform_conditions(condition.strip())
        condition = condition.replace("&", "and")
        condition = condition.replace("(", "")
        condition = condition.replace(")", "")
        condition = condition.lower()
        condition = condition.replace(" < ", "<")
        condition = condition.replace(" > ", ">")
        condition = condition.replace(" <= ", "<=")
        condition = condition.replace(" >= ", ">=")
        
        # Generate the line in "when" format
        formatted_rule = f"when {condition}then {class_value};"
        transformed_rules.append(formatted_rule)
    
    return transformed_rules

# Example input (you can insert the contents of your file here)
file_content = """
Rule: (FS <= 109.5) -> Predicted class: Other
Rule: (FS > 109.5) & (IPI <= 8228.5) & (IPI <= 1601.5) & (FS <= 140.5) & (IFI <= 120.5) -> Predicted class: Other
Rule: (FS > 109.5) & (IPI <= 8228.5) & (IPI <= 1601.5) & (FS <= 140.5) & (IFI > 120.5) -> Predicted class: CG
Rule: (FS > 109.5) & (IPI <= 8228.5) & (IPI <= 1601.5) & (FS > 140.5) & (IPI <= 515.5) & (IFI <= 5801867.0) & (IPI <= 26.5) -> Predicted class: CG
Rule: (FS > 109.5) & (IPI <= 8228.5) & (IPI <= 1601.5) & (FS > 140.5) & (IPI <= 515.5) & (IFI <= 5801867.0) & (IPI > 26.5) -> Predicted class: CG
Rule: (FS > 109.5) & (IPI <= 8228.5) & (IPI <= 1601.5) & (FS > 140.5) & (IPI <= 515.5) & (IFI > 5801867.0) -> Predicted class: AR
Rule: (FS > 109.5) & (IPI <= 8228.5) & (IPI <= 1601.5) & (FS > 140.5) & (IPI > 515.5) -> Predicted class: CG
Rule: (FS > 109.5) & (IPI <= 8228.5) & (IPI > 1601.5) & (IFI <= 6931456.0) -> Predicted class: CG
Rule: (FS > 109.5) & (IPI <= 8228.5) & (IPI > 1601.5) & (IFI > 6931456.0) -> Predicted class: AR
Rule: (FS > 109.5) & (IPI > 8228.5) & (FS <= 1162.0) & (IFI <= 14212795.0) & (IPI <= 8624.5) -> Predicted class: CG
Rule: (FS > 109.5) & (IPI > 8228.5) & (FS <= 1162.0) & (IFI <= 14212795.0) & (IPI > 8624.5) -> Predicted class: Other
Rule: (FS > 109.5) & (IPI > 8228.5) & (FS <= 1162.0) & (IFI > 14212795.0) & (IFI <= 20457180.0) -> Predicted class: AR
Rule: (FS > 109.5) & (IPI > 8228.5) & (FS <= 1162.0) & (IFI > 14212795.0) & (IFI > 20457180.0) -> Predicted class: Other
Rule: (FS > 109.5) & (IPI > 8228.5) & (FS > 1162.0) & (IFI <= 4554875.0) -> Predicted class: CG
Rule: (FS > 109.5) & (IPI > 8228.5) & (FS > 1162.0) & (IFI > 4554875.0) -> Predicted class: AR
"""

# Remove not necessary words
file_content = file_content.replace("Rule: ", "")
file_content = file_content.replace("Predicted class: ", "")

# Split the lines
lines = file_content.strip().split("\n")

# Get lists of threshold values
fs, ps, ipi, ifi = create_lists(lines)

print(f"fs = {fs};")
print(f"ps = {ps};")
print(f"ipi = {ipi};")
print(f"ifi = {ifi};")

# Transform the rules
transformed_rules = transform_rules(lines)

# Display the transformed rules
for rule in transformed_rules:
    print(rule)
