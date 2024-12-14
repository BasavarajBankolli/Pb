
import csv
import json


def compare_attendance(start_file, end_file):
    """
    Compare the IDs from start and end files and return the IDs present in both.
    """
    try:
        # Read IDs from start_frame.csv
        with open(start_file, "r") as f1:
            start_ids = {row[0] for row in csv.reader(f1) if row}

        # Read IDs from end_frame.csv
        with open(end_file, "r") as f2:
            end_ids = {row[0] for row in csv.reader(f2) if row}

        # Find common IDs present in both frames
        present_ids = start_ids & end_ids  # Intersection of sets

        print(f"IDs present in both frames: {present_ids}")
        return present_ids

    except FileNotFoundError as e:
        print(f"Error: {e}")
        return None


if __name__ == "__main__":
    # File names
    start_file = "start_frame.csv"
    end_file = "end_frame.csv"

    # Compare IDs and find those present in both files
    present_ids = compare_attendance(start_file, end_file)

    # Save the result to a new CSV file if IDs were found
    if present_ids:
        with open("dat/attendance.csv", "w", newline="") as f:
            writer = csv.writer(f)
            res = []
            for student_id in present_ids:
                res.append(student_id)

            with open(r"C:\Users\pvb02\Desktop\mini pro\smart\attendance.json","r+") as file:

                data = json.load(file)

                data["id"] = res

                file.seek(0)

                json.dump(data,file,indent=4)


                file.truncate()

        print("Attendance saved to 'attendance.json'.")
    else:
        print("No IDs to save. Please check the input files.")
