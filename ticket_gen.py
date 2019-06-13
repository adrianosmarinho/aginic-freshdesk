import sys

def parse_arguments():
    arguments = {}
    try:
        if (len(sys.argv) != 5):
            print("ERROR: Invalid arguments. Please type: py ticket_gen.py -n <number_of_activites> -o <output_file.json>")
        else:
            number_of_activities = parse_number_of_activities()
            arguments["number_of_activities"] = number_of_activities
            output_filename = parse_output_filename()
            arguments["output_filename"] = output_filename
    except ValueError as error:
            print("ERROR: " + error.args[0])
            print("You informed: " + error.args[1])
            raise
    finally:
        return arguments
            

def parse_number_of_activities():
    if sys.argv[1] != "-n":
        raise ValueError("The flag '-n' is not present.", sys.argv[1])

    if int(sys.argv[2]) > 0:
        number_of_activities = int(sys.argv[2])
        return number_of_activities
    else:
        raise ValueError("The number of activities must be a positive integer.", sys.argv[2])


def parse_output_filename():
    if sys.argv[3] != "-o":
        raise ValueError("The flag '-o' is not present.", sys.argv[3])

    if(sys.argv[4].endswith(".json")):
        output_filename = sys.argv[4]
        return output_filename
    else:
        raise ValueError("Incorrect file type.", sys.argv[4])

    


if __name__ == "__main__":
    arguments = parse_arguments()

    if ("number_of_activities" in arguments) and ("output_filename" in arguments):
        print("arguments complete")
        print(arguments)
    else:
        print("something went wrong with your arguments")
