from pathlib import Path
from organizer import get_files


def main():

  # Locate the sample_files folder
  project_folder = Path(__file__).parent
  sample_folder = project_folder / "sample_files"

  # Retrieve files
  files = get_files(sample_folder)

  # Display results
  print("\nFILE ORGANIZER")
  print("----------------------------")

  for file in files:
    print(file.name)

  print("----------------------------")
  print(f"Total files found: {len(files)}")

if __name__ == "__main__":
  main()
