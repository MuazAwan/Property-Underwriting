import matplotlib.pyplot as plt
import streamlit as st

def plot_metrics(metrics, chart_type="bar"):
    """
    Plot financial metrics as a chart.
    
    Args:
        metrics: A dictionary of metrics (key-value pairs).
        chart_type: Type of chart to display ("bar", "pie", "line").
    """
    if not metrics or all(value == 0 for value in metrics.values()):
        st.warning("No meaningful data to plot.")
        return

    try:
        # Debugging: Display the chart type and metrics
        st.write(f"Selected Chart Type: {chart_type}")
        st.write(f"Metrics: {metrics}")

        # Create the figure
        fig, ax = plt.subplots(figsize=(12, 7))  # Adjust figure size for better readability

        if chart_type == "bar":
            # Bar chart customization
            ax.bar(metrics.keys(), metrics.values(), color='skyblue', edgecolor='black')
            ax.set_title("Financial Metrics", fontsize=16, fontweight='bold')
            ax.set_ylabel("Value ($)", fontsize=12)
            ax.set_xlabel("Metrics", fontsize=12)
            ax.set_xticks(range(len(metrics.keys())))
            ax.set_xticklabels(metrics.keys(), rotation=45, fontsize=10)
            ax.grid(axis='y', linestyle='--', alpha=0.7)

        elif chart_type == "pie":
            # Pie chart customization
            if len(metrics) > 10:
                st.warning("Too many metrics for a pie chart. Consider using a bar or line chart.")
                return
            colors = plt.cm.Paired.colors[:len(metrics)]  # Ensure enough colors
            ax.pie(
                metrics.values(), 
                labels=metrics.keys(), 
                autopct='%1.1f%%', 
                startangle=90, 
                colors=colors,
                textprops={'fontsize': 10}
            )
            ax.set_title("Financial Metrics Distribution", fontsize=16, fontweight='bold')
        
        elif chart_type == "line":
            # Line chart customization
            ax.plot(
                list(metrics.keys()), 
                list(metrics.values()), 
                marker='o', 
                linestyle='-', 
                color='skyblue',
                linewidth=2,
                label="Financial Metrics"
            )
            ax.set_title("Financial Metrics Over Time", fontsize=16, fontweight='bold')
            ax.set_ylabel("Value ($)", fontsize=12)
            ax.set_xlabel("Metrics", fontsize=12)
            ax.set_xticks(range(len(metrics.keys())))
            ax.set_xticklabels(metrics.keys(), rotation=45, fontsize=10)
            ax.legend(fontsize=10)
            ax.grid(axis='both', linestyle='--', alpha=0.7)

        else:
            st.error(f"Unsupported chart type: {chart_type}. Please choose 'bar', 'pie', or 'line'.")
            return

        # Display the plot
        st.pyplot(fig)

    except ValueError as ve:
        st.error(f"Value error while plotting metrics: {ve}")
    except Exception as e:
        st.error(f"Unexpected error plotting metrics: {e}")
