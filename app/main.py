from services.pdf_to_csv import main as pdf_to_csv
from services.push_csv import main as push_csv

def main():
    pdf_to_csv()
    push_csv()

if __name__ == "__main__":
  main()