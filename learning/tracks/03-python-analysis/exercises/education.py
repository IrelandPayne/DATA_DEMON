# educational-attainment-county
import argparse
import sys
import pandas as pd

def most_educated(path, state):
    df = pd.read_csv(path)
    
    condensed_df = df[df["State"] == state]
    
    percent_degree = condensed_df["Percent of adults with a bachelor's degree or higher"].max()
    highest_df = condensed_df[condensed_df["Percent of adults with a bachelor's degree or higher"] == percent_degree]
    
    area = highest_df["Area name"].iloc[0]
    
    return (area, percent_degree)

def parse_arg(cli):
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    parser.add_argument("state")
    
    return parser.parse_args(cli)

if __name__ == "__main__":
    args = parse_arg(sys.argv[1:])
    county, percent = most_educated(args.path, args.state)
    print(f"{percent}% of adults in {county} have at least a bachelor’s degree")