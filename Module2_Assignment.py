import logging

# Set up basic logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class MandalModel:
    def __init__(self):
        """
        Initialize an empty list to store the stages of the Waterfall model.
        """
        self.stages = []
        logging.info("Initialized MandalModel with an empty stages list.")

    def prompt_user(self):
        """
        Prompts the user to input each stage name and adds it to the stages list.
        Logs each addition and informs when user input is finished.
        """
        print("Enter the stages of your Mandal Waterfall Model.")
        print("Type 'done' when you have finished entering all stages.\n")

        while True:
            stage = input("Enter a stage name: ").strip()

            if stage.lower() == 'done':
                logging.info("User has finished entering stages.")
                break

            if stage:  # Only add non-empty input
                self.stages.append(stage)
                logging.info(f"Stage '{stage}' added to the stages list.")
            else:
                logging.warning("Empty input detected and ignored.")

    def display_model(self):
        """
        Displays the collected stages in an organized list.
        Logs the display action.
        """
        if not self.stages:
            logging.warning("No stages available to display.")
            print("\nNo stages entered.")
            return

        print("\nYour Mandal Waterfall Model Stages:")
        for idx, stage in enumerate(self.stages, 1):
            print(f"{idx}. {stage}")

        logging.info(f"Displayed {len(self.stages)} stages.")


# Entry point for running the script
if __name__ == "__main__":
    model = MandalModel()  # Create an instance of the model
    model.prompt_user()  # Prompt user to enter stages
    model.display_model()  # Display the stages entered
