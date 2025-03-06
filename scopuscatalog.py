import os
import traceback
from pybliometrics.scopus import ScopusSearch, AbstractRetrieval
import json
from tqdm import tqdm
import pybliometrics
import time
import pandas as pd

pybliometrics.scopus.init()

# NOTE: config file for pybliometrics is stored in $HOME/.config/pybliometrics.cfg

if __name__ == "__main__":
    # Define the file path
    csv_file = "datascopus.csv"  # Change the file name as needed

    # Check if the file exists
    if not os.path.exists(csv_file):
        # Create an empty DataFrame with column headers
        df = pd.DataFrame(columns=["Title", "DOI", "PublicationName", "Year", "Country", "Abstract"])  
        df.to_csv(csv_file, index=False)

    df = pd.read_csv(csv_file)

    for year in range(2025, 2026):
        print(year)
        # make the folder to store the data for the year
        current_path = os.getcwd()
        folder_path = os.path.join(current_path, "output", str(year))
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # get the results
        x=ScopusSearch(
            f'ABS ( "corn" OR "maize" AND "weed" AND "detection" OR "recognition" OR "segmentation" AND "image" OR "imagery") '
            f'OR TITLE ( "weed" AND "corn" OR "maize" ) '
            f'AND KEY ( "corn" OR "maize" )'
            # f'AND SUBJAREA ( agri OR engi OR envi OR comp OR bioc ) '
            # f'AND DOCTYPE ( "AR" OR "CP" OR "CR" OR "RE" OR "DP" OR "BC") '
            f'AND PUBYEAR = {year} ',
            # f'AND NOT SUBJAREA ( medi OR immu OR busi OR soci OR econ OR psyc )',
            view="STANDARD"
        )

        print(f"Year: {year} , Results count: {len(x.results)}")
        
        for doc in x.results:
            doc_dict = doc._asdict()
            dd=list(doc_dict.keys())
            title=doc_dict['title']
            doi=doc_dict['doi']

            publicationname=doc_dict['publicationName']
            authornames = doc_dict['author_names']
            country=doc_dict['affiliation_country']
            # print(doi)
            # time.sleep(3)  # Wait for page to load
            if (doi != None):
                try:
                    time.sleep(2)
                    abstract_doc = AbstractRetrieval("10.1094/PDIS-05-23-0844-PDN", view="FULL")
                    abstract=abstract_doc.abstract
                except:
                    abstract="No access"
                # print(abstract_doc.abstract)
            else:
                abstract=None
            time.sleep(2)
            # # abstract = abstract_doc.abstract if abstract_doc.abstract else "No abstract available"
            new_item = {"Title": title, "DOI": doi ,"PublicationName": publicationname, "Year": year,"Country": country, "Abstract": abstract}  # Modify as needed
            
            if not ((df == pd.Series(new_item)).all(axis=1)).any():
                new_row = pd.DataFrame([new_item])

                # Use pd.concat() to add the new row
                df = pd.concat([df, new_row], ignore_index=True)
            df.to_csv(csv_file, index=False)
            print(title, '|',doi,'|', publicationname)
            # print(abstract)
            print('-----------------------------------------------------------')
            # print(doc_dict)
    
    # print(dd)

        # store the results and add the ref_docs key to store each reference
        # for doc in tqdm(x.results):
        #     try:
        #         # store each result in a file labeled by its Scopus EID
        #         doc_dict = doc._asdict()
        #         eid = doc_dict["eid"]
        #         file_path = os.path.join(folder_path, f"{eid}.json")
        #         if not os.path.exists(file_path):
        #             # Look up the references / citations for that document
        #             document = AbstractRetrieval(eid, view="REF")
        #             refs = []
        #             # Store the references
        #             for ref in document.references:
        #                 ref_doc = {"doi": ref.doi, "title": ref.title,
        #                            "id": ref.id,
        #                            "sourcetitle": ref.sourcetitle}
        #                 refs.append(ref_doc)
        #             doc_dict["ref_docs"] = refs
        #             # Dump the dictionary to the JSON file
        #             with open(file_path, "w") as json_file:
        #                 json.dump(doc_dict, json_file)
        #         else:
        #             print("SKIP (File already exists)")

        #     # we're not going to try too hard to fix any of the rare errors
        #     except Exception as e:
        #         pass
        #         # print(f"An error occurred: {e}")
        #         # traceback.print_exc()
