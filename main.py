from src.processor import process_variance
import os

def main():
    """
    Primary function for the Budget Variance Engine.
    """
    print("--- Starting Budget Variance Analysis ---")
    
    # Define paths 
    input_dir = "data"
    output_dir = "output"
    
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created missing directory: {output_dir}")

    try:
        # Execution: Call the core logic
        results = process_variance(input_dir)
        
        # User Feedback
        print("Success: Variance calculations complete.")
        print(f"Master Records Processed: {len(results['data'])}")
        print("Reports saved to the /output folder.")
        
    except FileNotFoundError as e:
        print(f"Data Error: {e}")
    except Exception as e:
        print(f"An unexpected system error occurred: {e}")

if __name__ == "__main__":
    main()