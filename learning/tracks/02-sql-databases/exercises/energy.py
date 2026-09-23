""" Build a database of energy sources in the US. """


from argparse import ArgumentParser
import sqlite3
import sys


class EnergyDB():
    """ An in-memory SQLite database that stores electricity production records.

    Attributes:
        conn (sqlite3.Connection): An in-memory SQLite database connection
            to query energy production data.
    """
    def __init__(self, filename):
        """ Initializes the database connection and loads data from a file.

        Args:
            filename (str): Path to the CSV file containing energy production
                data.

        Side effects:
            Initializes an SQLite connection and populates the database
            through invoking the read() method.
        """
        self.conn = sqlite3.connect(':memory:')
        self.read(filename)
       
    def __del__(self):
        """ Clean up the database connection. """
        try:
            self.conn.close()
        except:
            pass
        
    def read(self, filename):
        """ Read energy data from a CSV file and insert it into the SQLite table.

        Args:
            filename (str): Path to the CSV file to read.

        Side effects:
            Creates the 'production' table, inserts rows from
            the file, and commits the changes to self.conn.
        """
        cur = self.conn.cursor()
        cur.execute('CREATE TABLE production (year integer, state text, source text, mwh real)')
        
        with open (filename, 'r', encoding = 'utf-8') as file:
            file.readline()
            
            for line in file: 
                cleaned = line.strip().split(',')
                Year = int(cleaned[0])
                State = cleaned[1]
                Energy_Source = cleaned[2]
                Megawatthours = float(cleaned[3])
                
                cur.execute('INSERT INTO production VALUES (?,?,?,?)',
                            (Year, State, Energy_Source, Megawatthours))
        
        self.conn.commit()
                
    def production_by_source(self, source, year):
        """ Calculate total electricity production for a given source and year.

        Args:
            source (str): An energy source name.
            year (int): The production year.

        Returns:
            float: Total megawatt-hours produced across all states for the
            specified source and year.
        """
        cursor = self.conn.cursor()   
        cursor.execute('SELECT mwh FROM production WHERE source=? AND year=?',
                        (source, year))
        
        all_rows = cursor.fetchall()
    
        return sum(row[0] for row in all_rows)   

def main(filename):
    """ Build a database of energy sources and calculate the total production
    of solar and wind energy.
    
    Args:
        filename (str): path to a CSV file containing four columns:
            Year, State, Energy Source, Megawatthours.
    
    Side effects:
        Writes to stdout.
    """
    e = EnergyDB(filename)
    sources = [("solar", "Solar Thermal and Photovoltaic"),
               ("wind", "Wind")]
    for source_lbl, source_str in sources:
       print(f"Total {source_lbl} production in 2017: ",
             e.production_by_source(source_str, 2017))


def parse_args(arglist):
    """ Parse command-line arguments. """
    parser = ArgumentParser()
    parser.add_argument("file", help="path to energy CSV file")
    return parser.parse_args(arglist)


if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    main(args.file)
