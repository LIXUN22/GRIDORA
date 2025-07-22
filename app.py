import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
if "history" not in st.session_state:
    st.session_state.history = []



st.title("GRIDORA")
st.write("This is a simple Matrix Operations Tool.")
# Sidebar Inputs
st.sidebar.header("Matrix Dimensions")
rows_A = st.sidebar.number_input("Rows of Matrix A", min_value=1, value=2)
cols_A = st.sidebar.number_input("Columns of Matrix A", min_value=1, value=2)

operation = st.sidebar.selectbox(
    "Choose Operation",
    (
        "Addition",
        "Subtraction",
        "Multiplication",
        "Transpose A",
        "Determinant A",
        "Inverse A",
    )
)

# Matrix B only for binary operations
if operation in ("Addition", "Subtraction", "Multiplication"):
    rows_B = st.sidebar.number_input("Rows of Matrix B", min_value=1, value=2)
    cols_B = st.sidebar.number_input("Columns of Matrix B", min_value=1, value=2)

# Matrix Input Function
def get_matrix_input(name, rows, cols):
    st.markdown(f"### Enter values for Matrix {name}")
    matrix = []
    for i in range(rows):
        cols_input = st.columns(cols)
        row = []
        for j in range(cols):
            val = cols_input[j].number_input(f"{name}[{i+1}][{j+1}]", key=f"{name}_{i}_{j}", value=0.0)
            row.append(val)
        matrix.append(row)
    return np.array(matrix)

# Visualization Function
def visualize_matrix(matrix, title="Matrix Visualization"):
    fig, ax = plt.subplots()
    cax = ax.matshow(matrix, cmap='coolwarm')
    fig.colorbar(cax)
    ax.set_title(title)
    st.pyplot(fig)

# CSV Download Button
def download_matrix_csv(matrix, label="Download CSV", filename="matrix_result.csv"):
    df = pd.DataFrame(matrix)
    csv = df.to_csv(index=False)
    st.download_button(
        label=label,
        data=csv,
        file_name=filename,
        mime='text/csv',
    )
def log_history(op_type, matrix_A, matrix_B, result):
    entry = {
        "operation": op_type,
        "A": matrix_A.tolist(),
        "B": matrix_B.tolist() if matrix_B is not None else None,
        "result": result.tolist() if isinstance(result, np.ndarray) else result
    }
    st.session_state.history = [entry]

# Step-by-step multiplication explanation
def show_step_by_step_multiplication(A, B):
    st.markdown("### Step-by-step Multiplication")
    result = A @ B
    rows, cols = result.shape

    for i in range(rows):
        for j in range(cols):
            explanation = f"**Result[{i+1}][{j+1}] =** "
            terms = []
            for k in range(A.shape[1]):
                a_val = A[i][k]
                b_val = B[k][j]
                terms.append(f"({a_val} × {b_val})")
            explanation += " + ".join(terms)
            explanation += f" = **{result[i][j]}**"
            st.markdown(f"- {explanation}")

# Input Matrix A (always required)
A = get_matrix_input("A", rows_A, cols_A)

# Input Matrix B if required
if operation in ("Addition", "Subtraction", "Multiplication"):
    B = get_matrix_input("B", rows_B, cols_B)

# Perform Operation
st.markdown("---")
st.subheader("📊 Result")

try:
    if operation == "Addition":
        if A.shape != B.shape:
            st.error("Addition requires both matrices to have the same shape.")
        else:
            result = A + B
            st.dataframe(result)
            visualize_matrix(result, "Heatmap: A + B")
            download_matrix_csv(result, "⬇️ Download A + B as CSV")
            log_history("Addition", A, B, result)

    elif operation == "Subtraction":
        if A.shape != B.shape:
            st.error("Subtraction requires both matrices to have the same shape.")
        else:
            result = A - B
            st.dataframe(result)
            visualize_matrix(result, "Heatmap: A - B")
            download_matrix_csv(result, "⬇️ Download A - B as CSV")
            log_history("Subtraction", A, B, result)

    elif operation == "Multiplication":
        if A.shape[1] != B.shape[0]:
            st.error("Multiplication requires A.columns == B.rows.")
        else:
            result = A @ B
            st.dataframe(result)
            visualize_matrix(result, "Heatmap: A × B")
            download_matrix_csv(result, "⬇️ Download A × B as CSV")
            show_step_by_step_multiplication(A, B)
            log_history("Multiplication", A, B, result)

    elif operation == "Transpose A":
        result = A.T
        st.dataframe(result)
        visualize_matrix(result, "Heatmap: Transpose of A")
        download_matrix_csv(result, "⬇️ Download Transpose as CSV")
        log_history("Transpose", A, B, result)


    elif operation == "Determinant A":
        if A.shape[0] != A.shape[1]:
            st.error("Determinant requires a square matrix.")
        else:
            det = np.linalg.det(A)
            st.success(f"Determinant of A: {det:.4f}")

    elif operation == "Inverse A":
        if A.shape[0] != A.shape[1]:
            st.error("Inverse requires a square matrix.")
        elif np.linalg.det(A) == 0:
            st.error("Matrix A is singular (non-invertible).")
        else:
            result = np.linalg.inv(A)
            st.dataframe(result)
            visualize_matrix(result, "Heatmap: Inverse of A")
            download_matrix_csv(result, "⬇️ Download Inverse as CSV")

except Exception as e:
    st.error(f"Unexpected Error: {str(e)}")

# Show History
if st.session_state.history:
    st.markdown("---")
    st.subheader("History")

    for i, item in enumerate(reversed(st.session_state.history), 1):
        with st.expander(f"{i}. {item['operation']}"):
            st.markdown("**Matrix A:**")
            st.dataframe(np.array(item["A"]))

            if item["B"] is not None:
                st.markdown("**Matrix B:**")
                st.dataframe(np.array(item["B"]))

            st.markdown("**Result:**")
            st.dataframe(np.array(item["result"]))

