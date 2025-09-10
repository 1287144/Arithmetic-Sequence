import streamlit as st

def calculate_arithmetic_sequence(first_term, common_difference, num_terms):
    """
    Calculate arithmetic sequence given first term, common difference, and number of terms.
    
    Args:
        first_term (float): The first term of the sequence
        common_difference (float): The common difference between consecutive terms
        num_terms (int): The number of terms to generate
    
    Returns:
        list: List of terms in the arithmetic sequence
    """
    sequence = []
    for i in range(num_terms):
        term = first_term + (i * common_difference)
        sequence.append(term)
    return sequence

def calculate_geometric_sequence(first_term, common_ratio, num_terms):
    """
    Calculate geometric sequence given first term, common ratio, and number of terms.
    
    Args:
        first_term (float): The first term of the sequence
        common_ratio (float): The common ratio between consecutive terms
        num_terms (int): The number of terms to generate
    
    Returns:
        list: List of terms in the geometric sequence
    """
    sequence = []
    for i in range(num_terms):
        term = first_term * (common_ratio ** i)
        sequence.append(term)
    return sequence

def format_arithmetic_display(sequence, first_term, common_difference):
    """
    Format the arithmetic sequence for display with additional information.
    
    Args:
        sequence (list): The arithmetic sequence
        first_term (float): The first term
        common_difference (float): The common difference
    
    Returns:
        tuple: (sequence_str, formula)
    """
    # Create the sequence string
    sequence_str = ", ".join([str(term) for term in sequence])
    
    # Add formula information
    formula = f"aₙ = {first_term}"
    if common_difference > 0:
        formula += f" + {common_difference}(n-1)"
    elif common_difference < 0:
        formula += f" - {abs(common_difference)}(n-1)"
    else:
        formula += " + 0(n-1)"
    
    return sequence_str, formula

def format_geometric_display(sequence, first_term, common_ratio):
    """
    Format the geometric sequence for display with additional information.
    
    Args:
        sequence (list): The geometric sequence
        first_term (float): The first term
        common_ratio (float): The common ratio
    
    Returns:
        tuple: (sequence_str, formula)
    """
    # Create the sequence string
    sequence_str = ", ".join([str(term) for term in sequence])
    
    # Add formula information
    if common_ratio == 1:
        formula = f"aₙ = {first_term}"
    else:
        formula = f"aₙ = {first_term} × {common_ratio}^(n-1)"
    
    return sequence_str, formula

def main():
    # Set page configuration
    st.set_page_config(
        page_title="Sequence Calculator",
        page_icon="🔢",
        layout="centered"
    )
    
    # Main title
    st.title("🔢 Arithmetic & Geometric Sequence Calculator")
    st.markdown("Calculate and display arithmetic or geometric sequences with custom parameters.")
    
    # Sequence type selection
    st.header("Select Sequence Type")
    sequence_type = st.radio(
        "Choose the type of sequence to calculate:",
        ("Arithmetic Sequence", "Geometric Sequence"),
        help="Arithmetic: constant difference between terms. Geometric: constant ratio between terms."
    )
    
    # Create input section
    st.header("Input Parameters")
    
    # Create columns for better layout
    col1, col2 = st.columns(2)
    
    with col1:
        first_term = st.number_input(
            "First Term (a₁)",
            value=1.0,
            step=1.0,
            help="The first term of the sequence"
        )
        
        if sequence_type == "Arithmetic Sequence":
            second_param = st.number_input(
                "Common Difference (d)",
                value=1.0,
                step=1.0,
                help="The constant difference between consecutive terms"
            )
        else:
            second_param = st.number_input(
                "Common Ratio (r)",
                value=2.0,
                step=0.1,
                help="The constant ratio between consecutive terms"
            )
    
    with col2:
        num_terms = st.number_input(
            "Number of Terms (n)",
            min_value=1,
            max_value=1000,
            value=10,
            step=1,
            help="How many terms to display in the sequence"
        )
    
    # Add some spacing
    st.markdown("---")
    
    # Input validation and calculation
    if st.button("Calculate Sequence", type="primary"):
        try:
            # Validate inputs
            if num_terms <= 0:
                st.error("Number of terms must be a positive integer.")
                return
            
            if num_terms > 1000:
                st.error("Number of terms cannot exceed 1000 for performance reasons.")
                return
            
            if sequence_type == "Geometric Sequence" and second_param == 0:
                st.error("Common ratio cannot be zero for geometric sequences.")
                return
            
            # Calculate the sequence
            if sequence_type == "Arithmetic Sequence":
                sequence = calculate_arithmetic_sequence(first_term, second_param, num_terms)
                sequence_str, formula = format_arithmetic_display(sequence, first_term, second_param)
                param_name = "Common Difference"
            else:
                sequence = calculate_geometric_sequence(first_term, second_param, num_terms)
                sequence_str, formula = format_geometric_display(sequence, first_term, second_param)
                param_name = "Common Ratio"
            
            # Display results
            st.header("Results")
            
            # Show the formula
            st.subheader("General Formula")
            st.latex(formula.replace("aₙ", "a_n").replace("₁", "_1"))
            
            # Show sequence information
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("First Term", first_term)
            
            with col2:
                st.metric(param_name, second_param)
            
            with col3:
                st.metric("Number of Terms", num_terms)
            
            # Display the sequence
            st.subheader(f"{sequence_type}")
            
            # Show sequence in a nice format
            st.code(sequence_str, language=None)
            
            # Show additional information
            st.subheader("Additional Information")
            
            info_col1, info_col2 = st.columns(2)
            
            with info_col1:
                st.metric("Last Term", sequence[-1])
                
            with info_col2:
                # Calculate sum
                if sequence_type == "Arithmetic Sequence":
                    # Sum of arithmetic sequence: n/2 * (first_term + last_term)
                    sequence_sum = (num_terms / 2) * (first_term + sequence[-1])
                else:
                    # Sum of geometric sequence: a(r^n - 1)/(r - 1) for r ≠ 1
                    if second_param == 1:
                        sequence_sum = first_term * num_terms
                    else:
                        sequence_sum = first_term * (second_param**num_terms - 1) / (second_param - 1)
                
                st.metric("Sum of Sequence", f"{sequence_sum:.2f}")
            
            # Show step-by-step calculation for first few terms
            if num_terms >= 3:
                st.subheader("Step-by-Step Calculation (First 3 Terms)")
                
                for i in range(min(3, num_terms)):
                    term_value = sequence[i]
                    if i == 0:
                        calculation = f"a₁ = {first_term}"
                    else:
                        if sequence_type == "Arithmetic Sequence":
                            calculation = f"a{i+1} = {first_term} + {second_param} × {i} = {term_value}"
                        else:
                            calculation = f"a{i+1} = {first_term} × {second_param}^{i} = {term_value}"
                    
                    st.write(f"**Term {i+1}:** {calculation}")
        
        except Exception as e:
            st.error(f"An error occurred during calculation: {str(e)}")
    
    # Add information section
    st.markdown("---")
    st.subheader("About Sequences")
    
    with st.expander("Learn More"):
        st.markdown("""
        ## Arithmetic Sequences
        An **arithmetic sequence** is a sequence of numbers where the difference between 
        consecutive terms is constant. This difference is called the **common difference**.
        
        **General Formula:** aₙ = a₁ + (n-1)d
        **Sum Formula:** S = n/2 × (a₁ + aₙ)
        
        **Examples:**
        - 2, 4, 6, 8, 10... (first term = 2, common difference = 2)
        - 10, 7, 4, 1, -2... (first term = 10, common difference = -3)
        
        ## Geometric Sequences
        A **geometric sequence** is a sequence of numbers where each term after the first 
        is found by multiplying the previous term by a fixed number called the **common ratio**.
        
        **General Formula:** aₙ = a₁ × r^(n-1)
        **Sum Formula:** S = a₁(r^n - 1)/(r - 1) for r ≠ 1
        
        **Examples:**
        - 2, 4, 8, 16, 32... (first term = 2, common ratio = 2)
        - 100, 50, 25, 12.5... (first term = 100, common ratio = 0.5)
        - 3, 3, 3, 3, 3... (first term = 3, common ratio = 1)
        """)

if __name__ == "__main__":
    main()