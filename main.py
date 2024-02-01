import subprocess
import csv
import graphviz

def read_csv(filename):
    with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            yield row

def main():
    
    # Setup Graphviz
    dot = graphviz.Digraph('round-table', comment='The Round Table', filename='internet-map.gv', strict=True)
    
    old_address = '96.60.179.81'
    dot.node(old_address, old_address)
    edges = set()
    
    loop = 20
    i = 1
    
    for row in read_csv("urls.csv"):
        if i <= loop:
            i += 1
        else:
            print("Completed")
            break
        url = row[2].strip()
        print("Traceroute: " + url)
        tr = subprocess.Popen(["traceroute", url], stdout=subprocess.PIPE)
        while True:
            line = tr.stdout.readline().decode().strip()
            if not line:
                dot.node(url, url)
                dot.edge(old_address, url)
                edges.add((url, old_address))
                break
            # read the line based on traceroute's output
            line_parts = line.split(" ")
            try:
                int(line_parts[0]) # check if the line is a valid traceroute line
                address = line_parts[3].replace("(", "").replace(")", "")
                dot.node(address, address)
                if address == '*' or not edges.issubset((old_address, address)):
                    dot.edge(old_address, address)
                    edges.add((old_address, address))
                old_address = address
            except ValueError:
                continue
        print()
        dot.render('internet-map.gv', view=False)
        old_address = '96.60.179.81'
    
if __name__ == "__main__":
    main()